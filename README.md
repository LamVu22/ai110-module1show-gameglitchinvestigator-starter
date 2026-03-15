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

- [x] **Fixes applied:**
  1. Swapped the hint message strings in `check_guess` so "Too High" → "Go LOWER!" and "Too Low" → "Go HIGHER!"
  2. Removed the `if attempts % 2 == 0` string casting block in `app.py` so the secret is always compared as an integer.
  3. Changed Hard mode's range from 1–50 to 1–200 in `get_range_for_difficulty`.
  4. Refactored all game logic from `app.py` into `logic_utils.py` for separation of concerns.
  5. Fixed and expanded `tests/test_game_logic.py` from 3 broken starter tests to 7 passing tests.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
