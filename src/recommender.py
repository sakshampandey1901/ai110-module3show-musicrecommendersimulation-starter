import csv
import os
from pathlib import Path
from typing import List, Dict, Tuple, Any

from dataclasses import dataclass

GENRE_MATCH_POINTS = 2.0
MOOD_MATCH_POINTS = 1.0
ENERGY_WEIGHT = 0.5
ACOUSTIC_MATCH_POINTS = 0.5


def _scoring_weights() -> Dict[str, float]:
    """Baseline weights; set RECOMMENDER_EXPERIMENT=1 for half genre / double energy contribution."""
    if os.environ.get("RECOMMENDER_EXPERIMENT", "").strip().lower() in ("1", "true", "yes"):
        return {
            "genre": GENRE_MATCH_POINTS / 2,
            "mood": MOOD_MATCH_POINTS,
            "energy": ENERGY_WEIGHT * 2,
            "acoustic": ACOUSTIC_MATCH_POINTS,
        }
    return {
        "genre": GENRE_MATCH_POINTS,
        "mood": MOOD_MATCH_POINTS,
        "energy": ENERGY_WEIGHT,
        "acoustic": ACOUSTIC_MATCH_POINTS,
    }


@dataclass
class Song:
    """One catalog row: metadata plus audio-style feature floats."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Target genre, mood, energy, and whether the user prefers acoustic mixes."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Scores and ranks `Song` rows for a `UserProfile` (used by tests)."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return up to k songs ranked by content-based score (highest first)."""
        scored = [(self._score_song_oop(user, s), s) for s in self.songs]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short explanation string for how the song was scored."""
        score, reasons = self._score_song_oop_with_reasons(user, song)
        return f"Score {score:.2f}: " + "; ".join(reasons)

    def _score_song_oop(self, user: UserProfile, song: Song) -> float:
        s, _ = self._score_song_oop_with_reasons(user, song)
        return s

    def _score_song_oop_with_reasons(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        prefs: Dict[str, Any] = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_d = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "acousticness": song.acousticness,
        }
        return _score_from_prefs(prefs, song_d)


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from CSV into dicts with numeric fields coerced for math."""
    path = Path(csv_path)
    if not path.is_file():
        raise FileNotFoundError(f"Song catalog not found: {csv_path}")

    rows: List[Dict[str, Any]] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            rows.append(row)
    return rows


def _normalize_prefs(user_prefs: Dict[str, Any]) -> Dict[str, Any]:
    genre = user_prefs.get("favorite_genre") or user_prefs.get("genre")
    mood = user_prefs.get("favorite_mood") or user_prefs.get("mood")
    energy = user_prefs.get("target_energy")
    if energy is None:
        energy = user_prefs.get("energy")
    if energy is None:
        raise ValueError("Preferences need target_energy or energy")
    likes = user_prefs.get("likes_acoustic")
    if likes is None:
        likes = False
    return {"genre": str(genre), "mood": str(mood), "energy": float(energy), "likes_acoustic": bool(likes)}


def _score_from_prefs(prefs: Dict[str, Any], song: Dict[str, Any]) -> Tuple[float, List[str]]:
    p = _normalize_prefs(prefs)
    w = _scoring_weights()
    reasons: List[str] = []
    score = 0.0

    if song["genre"].lower() == p["genre"].lower():
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")

    if song["mood"].lower() == p["mood"].lower():
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")

    e = float(song["energy"])
    energy_sim = 1.0 - abs(e - p["energy"])
    energy_pts = w["energy"] * energy_sim
    score += energy_pts
    reasons.append(f"energy similarity (+{energy_pts:.2f})")

    ac = float(song["acousticness"])
    wants_acoustic = p["likes_acoustic"]
    if wants_acoustic and ac >= 0.5:
        score += w["acoustic"]
        reasons.append(f"acoustic preference (+{w['acoustic']:.1f})")
    elif not wants_acoustic and ac < 0.5:
        score += w["acoustic"]
        reasons.append(f"acoustic preference (+{w['acoustic']:.1f})")
    else:
        reasons.append("acoustic taste mismatch (+0.0)")

    return score, reasons


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Compute total score and human-readable reasons for one song vs prefs."""
    song_min = {
        "genre": song["genre"],
        "mood": song["mood"],
        "energy": song["energy"],
        "acousticness": song["acousticness"],
    }
    return _score_from_prefs(user_prefs, song_min)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, return top k with explanations."""
    ranked: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        ranked.append((song, score, explanation))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked[:k]
