import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / 'data' / 'sample_posts.json'


def main():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    print(f'Seed data ready with {len(posts)} sample posts at {DATA_PATH}')


if __name__ == '__main__':
    main()
