from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, HttpUrl


class AnalyzeTextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    save_history: bool = False


class AnalyzeUrlRequest(BaseModel):
    url: HttpUrl
    save_history: bool = False


class AnalysisResponse(BaseModel):
    id: int | None = None
    label: str
    confidence: float
    explanation: str
    highlights: List[str]
    created_at: datetime
    model_notice: str


class LivePostResponse(BaseModel):
    post_id: int
    text: str
    label: str
    confidence: float
    created_at: datetime


class ErrorResponse(BaseModel):
    error: str
    detail: str
