# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This is a content-based recommender. It compares the features of each song with a user's stated taste profile, scores every song, and returns the best matches. It doesn't use listening history or other users' behavior.

- **What features does each `Song` use in your system**

  Each song in `data/songs.csv` has genre, mood, energy, tempo_bpm, valence, danceability, and acousticness. The scoring formula uses four of them: genre, mood, energy, and acousticness.

  - tempo_bpm is left out because it mostly moves with energy and uses a different scale (BPM).
  - valence is left out because it mostly overlaps with mood.
  - danceability is left out to keep the first version simple; it's a candidate for a later experiment.

- **What information does your `UserProfile` store**

  `UserProfile` stores `favorite_genre`, `favorite_mood`, `target_energy` (a number from 0.0 to 1.0), and `likes_acoustic` (True/False). Example:

  ```python
  {"favorite_genre": "rock", "favorite_mood": "intense", "target_energy": 0.90, "likes_acoustic": False}
  ```

- **How does your `Recommender` compute a score for each song**

  Each song gets a score from a weighted sum (maximum 5.0):

  ```
  score = 2.0 * (genre match)
        + 1.0 * (mood match)
        + 1.5 * (1 - |target_energy - energy|)
        + 0.5 * (acousticness if likes_acoustic else 1 - acousticness)
  ```

  | Feature | Weight | How it's scored | Why this weight |
  |---|---|---|---|
  | Genre | 2.0 | Exact match: 2.0, otherwise 0 | Genre is the most stable part of a person's taste, so a mismatch is the most noticeable mistake. |
  | Energy | 1.5 | Closeness to the target: a perfect match earns 1.5 | It has the widest spread in the data and ranks songs in a graded way, not all-or-nothing. |
  | Mood | 1.0 | Exact match: 1.0, otherwise 0 | Mood matters but changes with the situation, and similar moods (chill, relaxed, focused) don't match as text. |
  | Acousticness | 0.5 | Rewards acoustic songs if `likes_acoustic`, non-acoustic songs if not | It overlaps heavily with energy, so a small weight avoids counting the same signal twice. |

  **Worked example:** for the profile above, *Storm Runner* (rock, intense, energy 0.91, acousticness 0.10) scores 2.0 + 1.0 + 1.48 + 0.45 = **4.93**. (Energy earns 1.5 × 0.99 = 1.485, which the program shows as 1.48 because of floating-point rounding.)

- **How do you choose which songs to recommend**

  The system keeps the scoring rule and the ranking rule separate:

  1. Score every song. `score_song()` applies the weighted formula above to each song in the catalog and returns a score along with the reasons behind it (e.g., "genre match (+2.0)", "energy close to your target (+1.43)").
  2. Rank the list. `recommend_songs()` sorts all songs by score, highest first. If two songs tie, the one whose energy is closer to the user's `target_energy` comes first.
  3. Return the top k. The top `k` songs (default 5) are returned, each with its score and an explanation built from its reasons.

  ```
  catalog ──► score_song() for each song ──► sort by score (high → low) ──► top k + explanations
  ```

  Because genre is worth the most points (2.0), songs in the user's favorite genre usually rank first. Genre doesn't automatically win, though: a song that matches the user's mood, energy, and acoustic preference can outrank a same-genre song that sounds very different. Since the catalog has only 1–3 songs per genre, the rest of the top 5 is mostly decided by energy and mood.

### Potential Biases

- **Over-prioritizing genre.** A genre match is worth 2.0 points, more than any other single feature. A song in a different genre that perfectly fits the user's mood and energy can rank below a same-genre song that sounds quite different.
- **Exact text matching.** `pop` doesn't match `indie pop`, and `chill` doesn't match `relaxed` or `focused`. Songs with closely related labels get no credit, so users whose favorites have related labels are penalized.
- **Uneven catalog.** Lofi has 3 songs, while most genres have only 1. Lofi fans get several genre matches; a metal or classical fan gets one, and the rest of their list is filled by energy alone.
- **Labels reflect the person who wrote them.** Genre and mood were assigned by hand, and broad labels like "latin" lump very different styles together. The recommender inherits those choices.
- **Simplified preferences.** `likes_acoustic` is yes/no, and one `target_energy` can't represent someone who likes both calm and intense music.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
Loaded 20 songs from ../data/songs.csv
Profile: genre=pop | mood=happy | energy=0.80 | likes acoustic=yes

Top 5 recommendations
==================================================

1. Sunrise City by Neon Echo
   Score: 4.56 / 5.00
   Why:
     - genre match: pop (+2.0)
     - mood match: happy (+1.0)
     - energy 0.82 vs. your target 0.80 (+1.47)
     - you prefer acoustic, song acousticness 0.18 (+0.09)

2. Gym Hero by Max Pulse
   Score: 3.33 / 5.00
   Why:
     - genre match: pop (+2.0)
     - energy 0.93 vs. your target 0.80 (+1.30)
     - you prefer acoustic, song acousticness 0.05 (+0.03)

3. Rooftop Lights by Indigo Parade
   Score: 2.61 / 5.00
   Why:
     - mood match: happy (+1.0)
     - energy 0.76 vs. your target 0.80 (+1.44)
     - you prefer acoustic, song acousticness 0.35 (+0.17)

4. Dusty Porch Swing by Willow Creek Band
   Score: 1.54 / 5.00
   Why:
     - energy 0.58 vs. your target 0.80 (+1.17)
     - you prefer acoustic, song acousticness 0.74 (+0.37)

5. Fiesta de Medianoche by Los Cometas
   Score: 1.54 / 5.00
   Why:
     - energy 0.86 vs. your target 0.80 (+1.41)
     - you prefer acoustic, song acousticness 0.25 (+0.12)
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



