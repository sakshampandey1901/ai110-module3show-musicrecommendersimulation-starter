"""
CLI-first runner for the music recommender: load CSV, score, print top k.
"""

from pathlib import Path

from src.recommender import load_songs, recommend_songs

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    csv_path = _PROJECT_ROOT / "data" / "songs.csv"
    songs = load_songs(str(csv_path))
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("Top recommendations (pop / happy / energy 0.8)")
    print("=" * 52)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        title = song["title"]
        artist = song["artist"]
        print(f"\n{i}. {title}")
        print(f"   Artist: {artist}")
        print(f"   Score:  {score:.2f}")
        print("   Reasons:")
        for part in explanation.split("; "):
            print(f"     • {part.strip()}")
    print()


if __name__ == "__main__":
    main()
