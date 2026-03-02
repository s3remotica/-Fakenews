from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List

from transformers import pipeline

from .config import settings


@dataclass
class PredictionResult:
    label: str
    confidence: float
    explanation: str
    highlights: List[str]
    created_at: datetime


class MisinformationClassifier:
    def __init__(self):
        self.classifier = None

    def _ensure_model(self):
        if self.classifier is None:
            self.classifier = pipeline('text-classification', model=settings.model_name, top_k=None)

    def _map_to_three_class(self, raw_label: str, confidence: float) -> str:
        lower = raw_label.lower()
        likely_fake = any(x in lower for x in ['negative', 'fake', 'misinformation', 'false'])
        likely_true = any(x in lower for x in ['positive', 'true', 'reliable'])
        if confidence >= 70 and likely_fake:
            return 'Likely False'
        if confidence >= 70 and likely_true:
            return 'Likely True'
        return 'Uncertain'

    def _split_sentences(self, text: str) -> List[str]:
        normalized = text.replace('!', '.').replace('?', '.')
        return [s.strip() for s in normalized.split('.') if s.strip()][:12]

    def predict(self, text: str) -> PredictionResult:
        self._ensure_model()
        output = self.classifier(text[: settings.max_text_length])[0]
        top = max(output, key=lambda item: item['score'])
        confidence = round(float(top['score']) * 100, 2)

        highlights: List[str] = []
        for sentence in self._split_sentences(text):
            sentence_result = self.classifier(sentence[:512])[0]
            sentence_top = max(sentence_result, key=lambda item: item['score'])
            if sentence_top['score'] > 0.55:
                highlights.append(sentence)
            if len(highlights) >= 3:
                break
        if not highlights:
            highlights = self._split_sentences(text)[:2]

        mapped_label = self._map_to_three_class(top['label'], confidence)
        explanation = 'Highlighting key sentences with strongest model signal using per-sentence confidence.'
        return PredictionResult(mapped_label, confidence, explanation, highlights, datetime.now(timezone.utc))


classifier_service = MisinformationClassifier()
