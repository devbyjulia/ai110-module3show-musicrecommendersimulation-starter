# 🎵 Music Recommender Simulation

## Project Summary

MoodMatcher v1 is a small command-line music recommender. It loads a catalog of 20 songs from a CSV file and takes a user taste profile: favorite genre, favorite mood, target energy (0 to 1), and whether the user likes acoustic music. It scores every song out of 5 using a weighted formula (genre 2.0, energy 1.5, mood 1.0, acousticness 0.5), then prints the top 5 songs, each with its score and the reasons behind it.

I also stress-tested the system with edge-case profiles, such as conflicting preferences and genres that aren't in the catalog. The tests showed that genre dominates the #1 spot, energy fills in the rest of the list, and the system never says when nothing really matched. The results and what they mean are in the sections below and in the [model card](model_card.md).

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

## Stress Testing with Diverse Profiles

### Conflicting preferences: high energy but a sad mood.

```
Loaded 20 songs from ../data/songs.csv
Profile: genre=folk | mood=sad | energy=0.90 | likes acoustic=yes

Top 5 recommendations
==================================================

1. Paper Boats by Harbor & Pine
   Score: 4.06 / 5.00
   Why:
     - genre match: folk (+2.0)
     - mood match: sad (+1.0)
     - energy 0.31 vs. your target 0.90 (+0.61)
     - you prefer acoustic, song acousticness 0.90 (+0.45)

2. Fiesta de Medianoche by Los Cometas
   Score: 1.56 / 5.00
   Why:
     - energy 0.86 vs. your target 0.90 (+1.44)
     - you prefer acoustic, song acousticness 0.25 (+0.12)

3. Storm Runner by Voltline
   Score: 1.53 / 5.00
   Why:
     - energy 0.91 vs. your target 0.90 (+1.48)
     - you prefer acoustic, song acousticness 0.10 (+0.05)

4. Gym Hero by Max Pulse
   Score: 1.48 / 5.00
   Why:
     - energy 0.93 vs. your target 0.90 (+1.46)
     - you prefer acoustic, song acousticness 0.05 (+0.03)

5. Sunrise City by Neon Echo
   Score: 1.47 / 5.00
   Why:
     - energy 0.82 vs. your target 0.90 (+1.38)
     - you prefer acoustic, song acousticness 0.18 (+0.09)
```

### Genre fights every other preference

```
Loaded 20 songs from ../data/songs.csv
Profile: genre=metal | mood=peaceful | energy=0.10 | likes acoustic=yes

Top 5 recommendations
==================================================

1. Still Water Nocturne by Elise Varga
   Score: 2.86 / 5.00
   Why:
     - mood match: peaceful (+1.0)
     - energy 0.18 vs. your target 0.10 (+1.38)
     - you prefer acoustic, song acousticness 0.97 (+0.48)

2. Iron Cathedral by Black Vane
   Score: 2.21 / 5.00
   Why:
     - genre match: metal (+2.0)
     - energy 0.97 vs. your target 0.10 (+0.20)
     - you prefer acoustic, song acousticness 0.03 (+0.01)

3. Spacewalk Thoughts by Orbit Bloom
   Score: 1.69 / 5.00
   Why:
     - energy 0.28 vs. your target 0.10 (+1.23)
     - you prefer acoustic, song acousticness 0.92 (+0.46)

4. Paper Boats by Harbor & Pine
   Score: 1.64 / 5.00
   Why:
     - energy 0.31 vs. your target 0.10 (+1.19)
     - you prefer acoustic, song acousticness 0.90 (+0.45)

5. Library Rain by Paper Lanterns
   Score: 1.55 / 5.00
   Why:
     - energy 0.35 vs. your target 0.10 (+1.12)
     - you prefer acoustic, song acousticness 0.86 (+0.43)
```

### Acoustic preference contradicts the genre

```
Loaded 20 songs from ../data/songs.csv
Profile: genre=metal | mood=angry | energy=0.97 | likes acoustic=yes

Top 5 recommendations
==================================================

1. Iron Cathedral by Black Vane
   Score: 4.51 / 5.00
   Why:
     - genre match: metal (+2.0)
     - mood match: angry (+1.0)
     - energy 0.97 vs. your target 0.97 (+1.50)
     - you prefer acoustic, song acousticness 0.03 (+0.01)

2. Neon Afterparty by Kiloglow
   Score: 1.48 / 5.00
   Why:
     - energy 0.95 vs. your target 0.97 (+1.47)
     - you prefer acoustic, song acousticness 0.02 (+0.01)

3. Gym Hero by Max Pulse
   Score: 1.47 / 5.00
   Why:
     - energy 0.93 vs. your target 0.97 (+1.44)
     - you prefer acoustic, song acousticness 0.05 (+0.03)

4. Storm Runner by Voltline
   Score: 1.46 / 5.00
   Why:
     - energy 0.91 vs. your target 0.97 (+1.41)
     - you prefer acoustic, song acousticness 0.10 (+0.05)

5. Fiesta de Medianoche by Los Cometas
   Score: 1.46 / 5.00
   Why:
     - energy 0.86 vs. your target 0.97 (+1.33)
     - you prefer acoustic, song acousticness 0.25 (+0.12)
```

### Genre and mood that don't exist in the catalog

```
Loaded 20 songs from ../data/songs.csv
Profile: genre=k-pop | mood=bittersweet | energy=0.50 | likes acoustic=no

Top 5 recommendations
==================================================

1. Velvet Hours by Nia Solace
   Score: 1.82 / 5.00
   Why:
     - energy 0.52 vs. your target 0.50 (+1.47)
     - you prefer non-acoustic, song acousticness 0.30 (+0.35)

2. Kitchen Floor Blues by Delta Mae
   Score: 1.62 / 5.00
   Why:
     - energy 0.47 vs. your target 0.50 (+1.46)
     - you prefer non-acoustic, song acousticness 0.66 (+0.17)

3. Island Time Again by Sunny Roots
   Score: 1.59 / 5.00
   Why:
     - energy 0.64 vs. your target 0.50 (+1.29)
     - you prefer non-acoustic, song acousticness 0.40 (+0.30)

4. Midnight Coding by LoRoom
   Score: 1.52 / 5.00
   Why:
     - energy 0.42 vs. your target 0.50 (+1.38)
     - you prefer non-acoustic, song acousticness 0.71 (+0.15)

5. Concrete Crown by Verse Theory
   Score: 1.52 / 5.00
   Why:
     - energy 0.78 vs. your target 0.50 (+1.08)
     - you prefer non-acoustic, song acousticness 0.12 (+0.44)
```

---

## Experiments You Tried

### Experiment 1: Different types of users

I ran four edge-case profiles (full output in [Stress Testing with Diverse Profiles](#stress-testing-with-diverse-profiles)) and compared them with the default pop/happy profile.

| Profile | #1 song (score) | What happened |
|---|---|---|
| Pop / happy / 0.80 (default) | Sunrise City (4.56) | Worked as expected: the only pop + happy song won, and the other pop song came #2. |
| Folk / sad / 0.90 | Paper Boats (4.06) | The user asked for high energy but got a quiet song (energy 0.31), because genre + mood (+3.0) outweigh the energy mismatch. |
| Metal / peaceful / 0.10 | Still Water Nocturne (2.86) | Genre did **not** win: the classical song matched mood, energy and acoustic, which together beat the metal song's genre bonus (2.21). |
| Metal / angry / 0.97 / acoustic | Iron Cathedral (4.51) | The acoustic preference changed nothing; at 0.5 points it is too weak to affect the ranking. |
| K-pop / bittersweet / 0.50 | Velvet Hours (1.82) | Nothing matched, so only energy decided the list. Scores were low, but the output looked like normal recommendations. |

**Pattern:** once the genre and mood matches run out, slots #2–5 are filled almost entirely by energy. For the folk/sad and metal/angry profiles, those slots were the same handful of high-energy songs (Fiesta de Medianoche, Storm Runner, Gym Hero, Neon Afterparty).

---

## Limitations and Risks

- Most genres have only one song
- Limited catalog of 20 songs
- Assumes users have one favorite genre and mood
- Uses only part of the song features

---

## Reflection

Building this showed me that a recommender doesn't really "understand" music. It turns each song into a few numbers and labels, compares them with what the user said they like, and adds up points. The ranking that comes out depends almost entirely on the weights I chose. Giving genre 2.0 points sounded reasonable when I designed it, but the stress tests showed it decides the #1 spot almost every time. Once the genre and mood matches run out, energy is the only thing ranking the rest of the list. Small design choices like these shape what every user sees, and nothing in the output tells the user those choices were made.

I also learned that bias can come from the data as much as from the formula. Lofi fans get three genre matches while most other genres get one, so some users simply get better recommendations because of what happened to be in the catalog. Exact label matching means "indie pop" gets nothing for a "pop" fan, and when nothing matches at all, the system still presents weak picks as confident recommendations. In a real app with millions of songs and users, the same kinds of problems could keep people in a filter bubble or quietly favor popular genres. That makes me think recommenders need diverse data, more flexible matching, and honest explanations.