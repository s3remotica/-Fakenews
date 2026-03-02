import asyncio
import json
from pathlib import Path

from .ml import classifier_service

DATA_FILE = Path(__file__).resolve().parent.parent / 'data' / 'sample_posts.json'


def load_posts() -> list[dict]:
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


async def live_post_generator(delay_seconds: float = 1.5):
    posts = load_posts()
    for item in posts:
        prediction = classifier_service.predict(item['text'])
        yield {
            'post_id': item['id'],
            'text': item['text'],
            'label': prediction.label,
            'confidence': prediction.confidence,
            'created_at': prediction.created_at.isoformat(),
        }
        await asyncio.sleep(delay_seconds)
