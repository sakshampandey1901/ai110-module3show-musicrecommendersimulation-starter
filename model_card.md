# Model Card: Music Recommender Simulation

## Model Name

**VibeFinder 1.0** — a tiny content-based song ranker for a classroom catalog.

---

## Goal / Task

The recommender suggests which songs from a fixed list best match a user’s taste. It does not learn from listening history. It scores each song with rules, then returns the top matches.

---

## Data Used

There are **18 songs** in `data/songs.csv`. Each row has a title, artist, genre, mood, and numbers for energy, tempo, valence, danceability, and acousticness. The list is small. Some genres appear only once or twice. There are no lyrics and no real audio files.

---

## Algorithm Summary

You get points if the song’s **genre** matches what the user asked for. You get points if the **mood** matches. You get points if the song’s **energy** is close to the user’s target energy (closer is better, not just “higher energy”). You get a small bonus if the song’s **acousticness** fits whether the user said they like acoustic sounds. Everything adds up to one score per song. The highest scores float to the top. Valence, tempo, and danceability are in the file but **not** used in the score yet.

---

## Observed Behavior / Biases

**Genre** counts more than **mood** in the default setup. So if someone asks for a sad mood but a happy genre, pop songs can still win because of genre and energy. A few high-energy tracks show up for many different users because energy and acoustic bonuses repeat. The catalog is uneven: some styles have more rows than others.

---

## Evaluation Process

I ran **four taste profiles** in the CLI (high-energy pop, chill lofi, intense rock, and a weird “pop + melancholic + high energy” mix). I compared the top five for each. I turned on **`RECOMMENDER_EXPERIMENT=1`** once to see if halving genre weight and doubling energy weight changed the order. I also ran the **unit tests** in `tests/test_recommender.py` to check basic ranking and explanations.

---

## Intended Use and Non-Intended Use

**Intended:** Learning how recommenders turn labels and numbers into an ordered list. Demos in class. Debugging a transparent score.

**Not intended:** Real product recommendations, fair representation of all music styles, or understanding what you “should” listen to. It should not be used to judge artists or to make decisions that affect people outside a school project.

---

## Ideas for Improvement

1. Add **valence** or **tempo** to the score so “sad” vs “happy” and speed matter more.
2. Add a **diversity** rule so the top five are not all the same vibe.
3. **Bigger or better-balanced data** so one genre does not crowd the list by accident.

---

## Personal Reflection

**Biggest learning moment:** Seeing that a clear formula can still feel “wrong” when a person’s taste is messy or contradictory. The code did exactly what we wrote; the hard part was deciding if that matched real listening.

**AI tools:** They sped up boilerplate and helped me think through edge cases. I still had to **run the program**, **read the CSV**, and **check the math** (weights, ties, and which columns actually affect the score). If I skipped that, bugs would hide in “reasonable-sounding” text.

**Surprise:** A few if-statements and additions can still produce an ordered list that *feels* like a recommendation app, even though there is no machine learning. The illusion breaks when you read the reasons line by line.

**What I’d try next:** Feed in **play history** or **skip** data, or add a second pass that picks diverse artists so the top list is not repetitive.
