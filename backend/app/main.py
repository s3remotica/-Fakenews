import json

from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .config import settings
from .database import Base, engine, get_db
from .live_feed import live_post_generator
from .ml import classifier_service
from .models import AnalysisRecord
from .schemas import AnalysisResponse, AnalyzeTextRequest, AnalyzeUrlRequest
from .security import rate_limit_dependency, validate_safe_url
from .url_extractor import fetch_and_extract_article

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(',')],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def to_response(record: AnalysisRecord) -> AnalysisResponse:
    return AnalysisResponse(
        id=record.id,
        label=record.label,
        confidence=record.confidence,
        explanation=record.explanation,
        highlights=json.loads(record.highlights),
        created_at=record.created_at,
        model_notice=settings.placeholder_model_notice,
    )


@app.post('/api/analyze/text', response_model=AnalysisResponse, dependencies=[Depends(rate_limit_dependency)])
def analyze_text(payload: AnalyzeTextRequest, db: Session = Depends(get_db)):
    prediction = classifier_service.predict(payload.text)

    record = AnalysisRecord(
        input_type='text',
        input_value=payload.text,
        label=prediction.label,
        confidence=prediction.confidence,
        explanation=prediction.explanation,
        highlights=json.dumps(prediction.highlights),
        save_history=payload.save_history and settings.enable_history,
    )

    if payload.save_history and settings.enable_history:
        db.add(record)
        db.commit()
        db.refresh(record)
    else:
        record.id = None
        record.created_at = prediction.created_at

    return AnalysisResponse(
        id=record.id,
        label=prediction.label,
        confidence=prediction.confidence,
        explanation=prediction.explanation,
        highlights=prediction.highlights,
        created_at=record.created_at,
        model_notice=settings.placeholder_model_notice,
    )


@app.post('/api/analyze/url', response_model=AnalysisResponse, dependencies=[Depends(rate_limit_dependency)])
async def analyze_url(payload: AnalyzeUrlRequest, db: Session = Depends(get_db)):
    if not settings.enable_url_analysis:
        raise HTTPException(status_code=403, detail='URL analysis disabled by admin.')

    validate_safe_url(str(payload.url))
    extracted_text = await fetch_and_extract_article(str(payload.url))
    if not extracted_text:
        raise HTTPException(status_code=422, detail='Could not extract readable article text.')

    prediction = classifier_service.predict(extracted_text)
    record = AnalysisRecord(
        input_type='url',
        input_value=str(payload.url),
        label=prediction.label,
        confidence=prediction.confidence,
        explanation=prediction.explanation,
        highlights=json.dumps(prediction.highlights),
        save_history=payload.save_history and settings.enable_history,
    )

    if payload.save_history and settings.enable_history:
        db.add(record)
        db.commit()
        db.refresh(record)
    else:
        record.id = None
        record.created_at = prediction.created_at

    return AnalysisResponse(
        id=record.id,
        label=prediction.label,
        confidence=prediction.confidence,
        explanation=prediction.explanation,
        highlights=prediction.highlights,
        created_at=record.created_at,
        model_notice=settings.placeholder_model_notice,
    )


@app.get('/api/history', response_model=list[AnalysisResponse], dependencies=[Depends(rate_limit_dependency)])
def get_history(db: Session = Depends(get_db)):
    rows = db.query(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).limit(100).all()
    return [to_response(row) for row in rows if row.save_history]


@app.get('/api/history/{item_id}', response_model=AnalysisResponse, dependencies=[Depends(rate_limit_dependency)])
def get_history_item(item_id: int, db: Session = Depends(get_db)):
    row = db.query(AnalysisRecord).filter(AnalysisRecord.id == item_id, AnalysisRecord.save_history.is_(True)).first()
    if not row:
        raise HTTPException(status_code=404, detail='History item not found.')
    return to_response(row)


@app.websocket('/ws/live')
async def websocket_live(websocket: WebSocket):
    await websocket.accept()
    try:
        async for item in live_post_generator():
            await websocket.send_json(item)
    except WebSocketDisconnect:
        return
