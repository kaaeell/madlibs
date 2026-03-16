# Mad Libs Game 🎉
A fun command-line Mad Libs game built with Python. You fill in random words and the program builds a silly story with them!
I built this just for fun while learning Python. No tutorial, no assignment — I just wanted to make something that actually makes me laugh.
---
## What it does
- Picks a random story from 3 different ones
- Asks you to fill in words (nouns, verbs, adjectives, etc.)
- Puts your words into the story and prints the result
- You can rate each story 1–5 stars
- You can play as many times as you want
### ✨ Multiplayer mode (2 players)
- Both players enter their names at the start
- Each player fills in the same story blanks separately — no peeking!
- Both completed stories are revealed side by side
- Players rate **each other's** story to keep it fair
- The scoreboard tracks ratings and picks an overall session winner

### 🙋 Single-player mode
- Choose 1 player at the start to play solo
- Fill in the blanks, read your story, then rate it yourself
- Personal scoreboard tracks all your rounds, your average rating, and your best story of the session

---
## What I learned
- Using `random.choice()` to pick random items
- Getting input from the user with `input()`
- String formatting and replacing text
- Loops and functions
- How `if __name__ == "__main__"` works
- Writing docstrings and keeping code readable
- Breaking repeated logic into reusable helper functions
---
## Ideas to improve it later
- [x] Add a rating system
- [x] Add multiplayer mode
- [x] Add single-player mode
- [ ] Add more stories
- [ ] Let user choose a story instead of random
- [ ] Save the generated story to a text file
- [ ] Add a GUI with tkinter
- [ ] Load stories from a JSON file
