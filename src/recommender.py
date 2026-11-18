import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dicts, converting numeric columns to int/float."""
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                value = value.strip()
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

# Weights for the Algorithm Recipe (see README: How The System Works).
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.5
ACOUSTIC_WEIGHT = 0.5

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Genre: exact match (case-insensitive) earns the full bonus.
    if song["genre"].strip().lower() == user_prefs["favorite_genre"].strip().lower():
        score += GENRE_WEIGHT
        reasons.append(f"genre match: {song['genre']} (+{GENRE_WEIGHT:.1f})")

    # Mood: exact match (case-insensitive) earns the full bonus.
    if song["mood"].strip().lower() == user_prefs["favorite_mood"].strip().lower():
        score += MOOD_WEIGHT
        reasons.append(f"mood match: {song['mood']} (+{MOOD_WEIGHT:.1f})")

    # Energy: the closer to the target, the more points.
    target_energy = float(user_prefs["target_energy"])
    energy_points = ENERGY_WEIGHT * (1 - abs(target_energy - song["energy"]))
    score += energy_points
    reasons.append(
        f"energy {song['energy']:.2f} vs. your target {target_energy:.2f} (+{energy_points:.2f})"
    )

    # Acousticness: reward acoustic songs if the user likes them, otherwise reward non-acoustic ones.
    if user_prefs.get("likes_acoustic", False):
        acoustic_points = ACOUSTIC_WEIGHT * song["acousticness"]
        label = "you prefer acoustic"
    else:
        acoustic_points = ACOUSTIC_WEIGHT * (1 - song["acousticness"])
        label = "you prefer non-acoustic"
    score += acoustic_points
    reasons.append(
        f"{label}, song acousticness {song['acousticness']:.2f} (+{acoustic_points:.2f})"
    )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return the top k as (song, score, explanation), highest first."""
    target = float(user_prefs["target_energy"])

    # 1. Score every song: (song, score, reasons)
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # 2. Rank: highest score first; on a tie, closer energy wins
    ranked = sorted(
        scored,
        key=lambda item: (item[1], -abs(target - item[0]["energy"])),
        reverse=True,
    )

    # 3. Keep the top k and join the reasons into one explanation string
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
