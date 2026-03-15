# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** A Streamlit number guessing game where the player picks a difficulty, guesses a secret number within a limited number of attempts, and receives directional hints ("Go HIGHER" / "Go LOWER") after each guess.

- [x] **Bugs found:**
  1. **Swapped hints** — `check_guess` returned "Go HIGHER!" when the guess was too high and "Go LOWER!" when too low, sending the player the wrong way.
  2. **String comparison on even attempts** — On even-numbered attempts, the secret was cast to `str`, breaking integer comparison. For example, `5 < 42` is correct, but `"5" > "42"` in string ordering, giving wrong outcomes.
  3. **Hard mode easier than Normal** — Hard mode used range 1–50 while Normal used 1–100, making Hard mode objectively easier.
  4. **Info text always said "1 and 100"** — The guess prompt was hardcoded to say "between 1 and 100" no matter what difficulty you picked.
  5. **Attempt counter off-by-one** — The game started counting attempts at 1 on first launch but reset to 0 on New Game, so the first game always showed one fewer attempt remaining.
  6. **Inconsistent wrong-guess penalty** — Guessing too high on even attempts secretly gave you +5 points instead of -5, while guessing too low always cost -5. The scoring was lopsided for no apparent reason.
  7. **New Game didn't fully reset** — Clicking New Game left the guess history, score, and game status from the previous round intact.

- [x] **Fixes applied:**
  1. Swapped the hint message strings in `check_guess` so "Too High" → "Go LOWER!" and "Too Low" → "Go HIGHER!"
  2. Removed the `if attempts % 2 == 0` string casting block in `app.py` so the secret is always compared as an integer.
  3. Changed Hard mode's range from 1–50 to 1–200 in `get_range_for_difficulty`.
  4. Made the info text use the actual difficulty range instead of hardcoded "1 and 100."
  5. Set the initial attempt counter to 0 so it's consistent with the New Game reset.
  6. Made wrong-guess penalties a flat -5 for both "Too High" and "Too Low" so scoring is fair and predictable.
  7. New Game now resets history, score, and status along with the secret and attempts.
  8. Refactored all game logic from `app.py` into `logic_utils.py` for separation of concerns.
  9. Fixed and expanded `tests/test_game_logic.py` from 3 broken starter tests to 7 passing tests.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
