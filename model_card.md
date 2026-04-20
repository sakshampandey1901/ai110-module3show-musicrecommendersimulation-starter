# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**CatalogRank 0.1** — content-based scoring over `data/songs.csv`.

---

## 2. Intended Use  

Ranks up to five songs from a fixed classroom catalog given a small preference dict (genre, mood, target energy, acoustic taste). For exploration only; not trained on real listening data.

---

## 3. How the Model Works  

Each song is scored by adding points for genre match, mood match, energy closeness to the user’s target, and a binary acoustic “fit.” The catalog is sorted by total score; unused columns (valence, tempo, danceability) are not in the score. Optional **`RECOMMENDER_EXPERIMENT=1`** halves genre weight and doubles the energy multiplier to test sensitivity.

---

## 4. Data  

18 rows in `data/songs.csv`: multiple genres and moods; rock and metal are sparse (one rock track). No lyrics or audio waveforms.

---

## 5. Strengths  

Transparent reasons (e.g. `genre match (+2.0)`). Different profiles (pop vs lofi vs rock) yield different #1 tracks when the catalog contains a clear genre/mood fit (e.g. Storm Runner for “Deep Intense Rock”).

---

## 6. Limitations and Bias 

Genre is worth twice as much as mood, so a user who wants a contradictory mood can still see top results dominated by genre matches (e.g. pop + melancholic edge case: Gym Hero and Sunrise City stay on top because of `pop` and high energy, not because the mood fits). The energy term is `1 − |Δenergy|`; it does not model “wrong mood” as a hard penalty. The catalog is tiny, so the same high-energy electronic or hip-hop tracks can float near the top for many profiles on energy + acoustic alone. Valence and tempo are ignored, which can hide emotionally “sad” or “slow” tracks that match a melancholic user.

---

## 7. Evaluation  

Tested four CLI profiles: **High-Energy Pop** (Sunrise City first), **Chill Lofi** (tie at top between two lofi/chill tracks), **Deep Intense Rock** (Storm Runner first), and an **edge-case** pop + melancholic + high energy profile (Gym Hero edges Sunrise City; Cathedral Light appears third for mood match but low energy). Surprised that the lofi profile had a perfect tie at rank 1—scores only reflect stored features, not diversity. Ran **`RECOMMENDER_EXPERIMENT=1`**: genre lines show `+1.0` and energy contributions grow, so ordering changes without new data. Unit tests in `tests/test_recommender.py` lock basic ranking and explain behavior.

---

## 8. Future Work  

Add valence/tempo terms, tie-breakers, or a diversity penalty so top-5 is not repetitive.

---

## 9. Personal Reflection  

A short transparent score is easy to debug but can feel wrong when the user’s intent is contradictory—then the model is “doing the math” while the real goal is subjective.
