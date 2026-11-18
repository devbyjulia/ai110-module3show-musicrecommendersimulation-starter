"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs

MAX_SCORE = 5.0  # Highest possible score from the Algorithm Recipe


def print_profile(user_prefs: dict) -> None:
    """Print the user's taste profile as a one-line summary."""
    acoustic = "yes" if user_prefs.get("likes_acoustic", False) else "no"
    print(
        f"Profile: genre={user_prefs['favorite_genre']} | "
        f"mood={user_prefs['favorite_mood']} | "
        f"energy={float(user_prefs['target_energy']):.2f} | "
        f"likes acoustic={acoustic}"
    )


def print_recommendations(recommendations: list) -> None:
    """Print each recommendation with its rank, score, and reasons."""
    print(f"\nTop {len(recommendations)} recommendations")
    print("=" * 50)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} / {MAX_SCORE:.2f}")
        print("   Why:")
        # recommend_songs() joins the reasons with "; ", so split them back apart.
        for reason in explanation.split("; "):
            print(f"     - {reason}")

    print()


def main() -> None:
    songs = load_songs("../data/songs.csv") 

    # Starter example profile
    user_prefs = {"favorite_genre": "pop", "favorite_mood": "happy", 
                  "target_energy": 0.8, "likes_acoustic": True}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_profile(user_prefs)
    print_recommendations(recommendations)


if __name__ == "__main__":
    main()
