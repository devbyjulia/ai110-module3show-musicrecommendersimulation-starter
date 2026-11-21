# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Model MoodMatcher v1.

---

## 2. Intended Use

The recommender is designed to suggest songs from a 20-song catalog based on a user profile. The recommender uses a weighted formula to calculate a score for each song, then returns the top 5 songs. The system assumes that the user will favor genre over every other feature (mood, energy, acousticness), meaning that songs matching the user's genre usually take the #1 spot. It also assumes that users have one favorite genre, one favorite mood, one target energy level, and a yes/no preference for acoustic music. This project is intended for classroom exploration, not real users.

---

## 3. How the Model Works  

The user tells the model four things: their favorite genre, their favorite mood, how energetic they want the music to be (from 0 to 1), and whether they like acoustic music. The model then gives every song in the catalog points out of 5:

- **Genre (up to 2 points):** full points if the song's genre matches the user's favorite, otherwise none.
- **Mood (up to 1 point):** full points if the song's mood matches, otherwise none.
- **Energy (up to 1.5 points):** the closer the song's energy is to what the user wants, the more points it gets.
- **Acoustic (up to 0.5 points):** if the user likes acoustic music, more acoustic songs get more points; if not, less acoustic songs do.

The model adds up the points, sorts the songs from highest to lowest, and shows the top 5. If two songs tie, the one with energy closer to the user's target goes first. Each recommendation also lists where its points came from, so the user can see why it was picked.

The starter code just returned the first 5 songs in the file, with a placeholder explanation. I replaced that with the point system above, the tie-breaker, and the explanations for each song.

---

## 4. Data  

The catalog has 20 songs. The starter file had 10, and I added 10 more to cover genres and moods it was missing. Each song has a title, artist, genre, mood, and number ratings for energy, tempo, valence, danceability, and acousticness. The model only uses genre, mood, energy, and acousticness.

The songs cover 17 genres (including pop, lofi, rock, metal, jazz, classical, folk, hip hop, edm, and latin) and 16 moods (including happy, chill, intense, sad, angry, and peaceful). Coverage is uneven: lofi has 3 songs and pop has 2, but every other genre has only 1. Fans of most genres therefore get just one genre match.

Some kinds of musical taste are missing. There are no high-energy acoustic songs and no high-energy sad songs, because none of the acoustic or sad songs in the catalog has an energy above 0.6. The data also has nothing about lyrics, language, era, or popularity, so it can't capture a taste for, say, 90s music or Spanish-language songs.

---

## 5. Strengths  

The system works best for users whose favorite genre and mood appear together in the catalog. For example, the acoustic metalhead profile (metal, angry, energy 0.97) got Iron Cathedral at #1 with 4.51 out of 5, far ahead of the next song at 1.48. That is the obvious right answer.

The energy score is a sensible fallback. Once there are no more genre or mood matches, the remaining slots fill with songs at a similar energy level. The metalhead's #2 to #5 were all high-energy songs (0.86 to 0.95), which a fan of loud music would probably enjoy even outside metal.

Some results matched my intuition even when preferences conflicted. In the metal-but-peaceful test, Still Water Nocturne (classical, peaceful, very acoustic, low energy) beat the only metal song, because it matched three of the four preferences. That felt like a reasonable choice for someone asking for calm music.

Finally, every recommendation explains where its points came from, so it is easy to see why a song was picked and to spot when the scoring is doing something odd.

These strengths come from the same design as the main weakness in section 6: the large genre bonus that gives the metalhead a clear #1 is also what locks genre matches into the top spot and keeps users from discovering anything new.

---

## 6. Limitations and Bias 

A weakness I discovered during the experiments is that genre locks in the top results. A genre match (+ 2.00) is worth as much as the best energy and acoustic scores combined (1.5 + 0.5). If the mood is also a match, a song with matching genre can never lose to one without a matching genre, so the user isn't pushed towards anything new.

---

## 7. Evaluation

I tested four different profiles:
- High energy with sad mood
- Genre fights every other preference
- Acoustic preference contradicts the genre
- Genre and mood that don't exist in the catalog

What surprised me about genre fighting every other preference was the #1 song without a matching genre.

For high energy + sad vs. acoustic metalhead, both profiles asked for very high energy (0.9 and 0.97) and both said they like acoustic music, but their #1 picks are opposites. The sad profile's top song is Paper Boats, a quiet acoustic folk song (energy 0.31), while the metalhead's is Iron Cathedral, a loud song with almost no acoustic sound (acousticness 0.03). This makes sense because in both cases the #1 song was the one that matched both genre and mood (+3.0 points), which is more than energy and acousticness can ever add up to (2.0 at most).

For acoustic metalhead vs. metal-but-peaceful, both profiles have metal as their favorite genre, but Iron Cathedral drops from #1 (4.51) to #2 (2.21) when the user asks for a peaceful mood and low energy. Still Water Nocturne, a classical song, takes #1 instead. This makes sense: it matches three of the four preferences (mood, energy and acoustic), and together those outweigh a genre match on its own. This was the only test where genre did not win.

For made-up genre and mood vs. everything else, when neither the genre (k-pop) nor the mood (bittersweet) exists in the catalog, the top score falls to 1.82, compared with 4+ when genre and mood both match. The list becomes mid-energy songs from unrelated genres (Velvet Hours, Kitchen Floor Blues, Island Time Again). This makes sense because only the energy and acoustic scores are left, so the system picks songs whose energy is close to 0.5. The problem is that it still presents these as normal recommendations and never tells the user that nothing actually matched.


---

## 8. Future Work  

- **Give partial credit for similar labels.** Right now "indie pop" gets nothing for a "pop" fan, and "melancholic" gets nothing for a "sad" fan. Grouping related genres and moods would fix this.
- **Improve diversity in the top 5.** Limiting each artist to one song and each genre to two would push users toward something new instead of locking in the same genre.
- **Rebalance the weights.** Lowering the genre bonus would let mood and energy matter more, so one matching label doesn't decide the #1 spot.
- **Be honest when nothing matches.** If no song matches the user's genre or mood, the system should say so instead of presenting weak picks as normal recommendations.


---

## 9. Personal Reflection

I learned that real-world recommendation systems combine two approaches: content-based filtering and collaborative filtering. Content-based filtering recommends items with features resembling what the user already likes. Collaborative filtering learns from the behavioral patterns of many users. Something that surprised me was how much a single label matters. "Rooftop Lights" is a happy, high-energy song a pop fan would probably enjoy, but because it's labeled "indie pop" instead of "pop," my system gave it no genre credit. However, for profiles with songs that matched the profile well, this relatively simple recommender gave solid #1 recommendations that were clear matches; the starter pop profile is an example. This has given me a greater appreciation for music recommendation apps and the engineering that recommends me my next favorite song. 

Using an AI assistant shaped my process in a few ways. It suggested adversarial and edge-case profiles I wouldn't have thought of on my own, such as conflicting preferences and genres that aren't in the catalog. I chose to run those tests myself and record the real output, so my evaluation is based on what my code actually did. When I had to pick a sensitivity experiment, it explained why a weight shift would reveal more than removing the mood check, which helped me understand how the weights balance against each other. It also pointed out biases in my scoring and data, like the uneven number of songs per genre, which I then checked against my own test results. Overall, the AI made me faster and pushed me to test more thoroughly, but I still had to verify its claims against my own code and results.
