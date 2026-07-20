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
    target_acoustic: float
    target_valence: float
    target_danceability: float
    target_tempo_bpm: float
    
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

userProfile = UserProfile(
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.75,
    target_acoustic=0.20,
    target_valence=0.75,
    target_danceability=0.75,
    target_tempo_bpm=120.0
)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Algorithm Recipe (Phase 2):
      - mood match:          +25 pts (categorical, strongest single signal)
      - genre match:         +15 pts (categorical, weaker than mood)
      - valence similarity:  up to 15 pts
      - energy similarity:   up to 15 pts
      - danceability sim.:   up to 10 pts
      - acousticness sim.:   up to 10 pts
      - tempo_bpm sim.:      up to 10 pts (normalized, since bpm isn't 0-1)
    Any preference key not present in user_prefs is simply skipped.
    """
    score = 0.0
    reasons: List[str] = []

    if "mood" in user_prefs and song.get("mood") == user_prefs["mood"]:
        score += 25.0
        reasons.append("mood match (+25.0)")

    if "genre" in user_prefs and song.get("genre") == user_prefs["genre"]:
        score += 15.0
        reasons.append("genre match (+15.0)")

    numeric_weights = {
        "valence": 15.0,
        "energy": 15.0,
        "danceability": 10.0,
        "acousticness": 10.0,
    }
    for key, weight in numeric_weights.items():
        if key in user_prefs and key in song:
            diff = abs(float(song[key]) - float(user_prefs[key]))
            similarity = max(0.0, 1 - diff)
            points = similarity * weight
            score += points
            reasons.append(f"{key} similarity (+{points:.1f})")

    if "tempo_bpm" in user_prefs and "tempo_bpm" in song:
        diff = abs(float(song["tempo_bpm"]) - float(user_prefs["tempo_bpm"])) / 120.0
        similarity = max(0.0, 1 - diff)
        points = similarity * 10.0
        score += points
        reasons.append(f"tempo similarity (+{points:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda entry: entry[1], reverse=True)
    return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked[:k]]
