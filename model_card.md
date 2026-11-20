# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

A weakness I discovered during the experiments is that genre locks in the top results. A genre match (+ 2.00) is worth as much as the best energy and acoustic scores combines (1.5 + 0.5). If the mood is also a match, a song with matching genre can never lose to one that doesn't match, so the user isn't pushed towards anything new.

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
