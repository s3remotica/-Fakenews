# Real-Time Fake News & Misinformation Detection System

A full-stack educational MVP that analyzes pasted text, article URLs, and simulated live posts using a HuggingFace Transformer pipeline.

## Safety & Ethics
- This app provides **probabilistic AI estimates** only.
- It does **not** claim certainty or legal truth.
- Always verify with trusted and official sources.
- User text is not persisted unless `save_history=true`.

## Model Note
This starter uses `cardiffnlp/twitter-roberta-base-sentiment-latest` as a **placeholder model**. Replace with a misinformation/fact-check tuned model for real deployments.

## File Tree

```text
.
├── backend
│   ├── app
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── live_feed.py
│   │   ├── main.py
│   │   ├── ml.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   └── url_extractor.py
│   ├── data/sample_posts.json
│   ├── tests/test_api.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── seed_sample_posts.py
├── frontend
│   ├── app
│   │   ├── analyze/page.tsx
│   │   ├── history/page.tsx
│   │   ├── live-feed/page.tsx
│   │   ├── globals.css
│   │   └── layout.tsx
│   ├── components
│   │   ├── DisclaimerBanner.tsx
│   │   └── NavBar.tsx
│   ├── lib/api.ts
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## API
- `POST /api/analyze/text`
- `POST /api/analyze/url`
- `GET /api/history`
- `GET /api/history/{id}`
- `WS /ws/live`

## Run with Docker Compose (Windows/Mac/Linux)
```bash
docker compose up --build
```
Frontend: http://localhost:3000  
Backend: http://localhost:8000/docs

## Run without Docker
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Tests
```bash
cd backend
pytest
```

## Confidence Calibration Rule
- If confidence >= 70% and model signal suggests fake -> `Likely False`
- If confidence >= 70% and model signal suggests true -> `Likely True`
- Otherwise -> `Uncertain`

## Notes for Students
- Replace `ml.py` model mapping with a true misinformation classifier.
- Add Captum or SHAP for more robust explainability if GPU resources are available.
