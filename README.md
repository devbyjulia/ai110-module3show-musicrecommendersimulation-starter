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

Explain your design in plain language.

Some prompts to answer:

- **What features does each `Song` use in your system**
  - For example: genre, mood, energy, tempo

  Each song contains the following features: genre, mood, energy, tempo_bpm, valence, danceability, and acousticness.

- **What information does your `UserProfile` store**
  
  `UserProfile` stores `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`.

- **How does your `Recommender` compute a score for each song**
  
  `Recommender` computes a score for each song with the weighted sum:
  ```
      score = 2.0 * (genre match)
      + 1.0 * (mood match)
      + 1.5 * (1 - |target_energy - energy|)
      + 0.5 * (acousticness if likes_acoustic else 1 - acousticness)
    ```

- **How do you choose which songs to recommend**

  The system keeps the scoring rule and the ranking rule separate:

  1. Score every song. `score_song()` applies the weighted formula above to each song in the catalog and returns a score along with the reasons behind it (e.g., "genre match (+2.0)", "energy close to your target (+1.43)").
  2. Rank the list. `recommend_songs()` sorts all songs by score, highest first. If two songs tie, the one whose energy is closer to the user's `target_energy` comes first.
  3. Return the top k. The top `k` songs (default 5) are returned, each with its score and an explanation built from its reasons.

  ```
  catalog ──► score_song() for each song ──► sort by score (high → low) ──► top k + explanations
  ```

  Because genre is worth the most points (2.0), songs in the user's favorite genre usually rank first. Genre doesn't automatically win, though: a song that matches the user's mood, energy, and acoustic preference can outrank a same-genre song that sounds very different. Since the catalog has only 1–3 songs per genre, the rest of the top 5 is mostly decided by energy and mood.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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



