"""
CLI runner: load CSV, score multiple taste profiles, print top k each.
"""

import os
from pathlib import Path

from src.recommender import load_songs, recommend_songs

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Baseline scoring unless RECOMMENDER_EXPERIMENT=1 (half genre weight, double energy weight).
PROFILES = [
    {
        "label": "High-Energy Pop",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.92,
        "likes_acoustic": False,
    },
    {
        "label": "Chill Lofi",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
    },
    {
        "label": "Deep Intense Rock",
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    {
        "label": "Edge case: upbeat genre + melancholic mood + high energy",
        "genre": "pop",
        "mood": "melancholic",
        "energy": 0.88,
        "likes_acoustic": False,
    },
]


def _print_block(title: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(title)
    print("=" * 56)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{i}. {song['title']}")
        print(f"   Artist: {song['artist']}")
        print(f"   Score:  {score:.2f}")
        print("   Reasons:")
        for part in explanation.split("; "):
            print(f"     • {part.strip()}")
    print()


def main() -> None:
    csv_path = _PROJECT_ROOT / "data" / "songs.csv"
    songs = load_songs(str(csv_path))
    print(f"Loaded songs: {len(songs)}")
    mode = os.environ.get("RECOMMENDER_EXPERIMENT", "").strip().lower() in ("1", "true", "yes")
    print(f"Scoring: {'experiment (half genre, double energy weight)' if mode else 'baseline'}")
    print()

    for p in PROFILES:
        label = p["label"]
        prefs = {k: v for k, v in p.items() if k != "label"}
        _print_block(f"Profile: {label}", prefs, songs, k=5)


if __name__ == "__main__":
    main()
