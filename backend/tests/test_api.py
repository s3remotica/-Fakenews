from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app
from app.ml import PredictionResult, classifier_service


def fake_prediction(_text: str):
    return PredictionResult(
        label='Uncertain',
        confidence=66.0,
        explanation='dummy explanation',
        highlights=['dummy highlight'],
        created_at=datetime.now(timezone.utc),
    )


def test_analyze_text(monkeypatch):
    monkeypatch.setattr(classifier_service, 'predict', fake_prediction)
    client = TestClient(app)
    response = client.post('/api/analyze/text', json={'text': 'Example text', 'save_history': False})
    assert response.status_code == 200
    data = response.json()
    assert data['label'] == 'Uncertain'
    assert 'highlights' in data


def test_history_list(monkeypatch):
    monkeypatch.setattr(classifier_service, 'predict', fake_prediction)
    client = TestClient(app)
    save_resp = client.post('/api/analyze/text', json={'text': 'save me', 'save_history': True})
    assert save_resp.status_code == 200
    hist_resp = client.get('/api/history')
    assert hist_resp.status_code == 200
    assert isinstance(hist_resp.json(), list)
