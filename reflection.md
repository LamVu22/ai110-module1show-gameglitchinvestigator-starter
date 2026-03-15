# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

When I first ran the game, it appeared to be a normal, functional number guessing game, complete with difficulty settings, a guess input, and a scoring system. However, I quickly realized that something was off: the hints were pointing me in the wrong direction, and the game felt inconsistent between attempts.

- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").

The first bug I noticed was that the hints were backwards. When my guess was too high, the game told me to "Go HIGHER," and when it was too low, it said "Go LOWER," which made me go in the wrong direction every time. The second bug was that on even numbered attempts, the game compared my integer guess against a string version of the secret number, which caused the comparison logic to break and give unreliable results. I also noticed that "Hard" difficulty actually used a smaller range (1–50) than "Normal" (1–100), making it easier instead of harder. I fixed this by changing Hard mode's range to 1–200. As I kept playing, I caught more issues: the info text always said "between 1 and 100" even on Easy or Hard, the attempt counter started at 1 on the first game but reset to 0 on New Game, and the scoring penalized you -5 for guessing too low but sometimes gave you +5 for guessing too high, which made no sense. The New Game button also didn't clear the guess history or reset the score from the previous round.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude Code for this project. I asked it to run the app, read the source code, and identify bugs. I then used it to refactor the game logic from `app.py` into `logic_utils.py`, fix the bugs, and generate pytest cases as well.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

Claude Code correctly identified that the hint messages in the `check_guess` function were swapped: when the guess was too high, the code returned "Go HIGHER!" instead of "Go LOWER!" It suggested swapping the two hint strings. I verified this by opening the developer debug info expander to see the secret number, then guessing above it. Before the fix, the game said "Go HIGHER". After the fix it correctly said "Go LOWER." I also wrote a pytest (`test_too_high_hint_says_lower`) that asserts the message contains "LOWER" when the guess is too high, and it passed.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Claude Code flagged the scoring formula `100 - 10 * (attempt_number + 1)` in `update_score` as a bug, claiming the `+ 1` penalizes players for winning early. It suggested removing the `+ 1` so winning on attempt 1 gives 90 points instead of 80. However, without a design spec, this is ambiguous. It could be an intentional difficulty curve. I verified by manually computing scores: attempt 1 gives 80, attempt 2 gives 70, etc. The progression is consistent and reasonable, just slightly more aggressive than expected. I decided not to change it, since "different than expected" is not the same as "broken," and the AI was too confident in calling it a definitive bug.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I used two approaches: manual testing in the live Streamlit app and automated pytest cases. For manual testing, I opened the Developer Debug Info panel to see the secret number, then made deliberate guesses above and below it to confirm hints pointed the right direction. A bug was only "fixed" when both the manual playthrough and the automated tests agreed.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

I ran `pytest tests/test_game_logic.py -v` which included 7 tests. One key test, `test_too_high_hint_says_lower`, calls `check_guess(60, 50)` and asserts the returned message contains "LOWER." Before the fix this would have failed because the original code returned "Go HIGHER!" for a too-high guess. Another test, `test_check_guess_int_comparison_not_string`, calls `check_guess(5, 42)` and asserts the outcome is "Too Low" — this catches the string comparison bug because `"5" > "42"` is `True` in string ordering, which would have returned the wrong outcome. All 7 tests passed after the fixes.

- Did AI help you design or understand any tests? How?

Yes. I asked Claude Code to generate pytest cases targeting the two bugs I fixed. It wrote tests that checked both the outcome string ("Too High"/"Too Low") and the hint message content, which was more thorough than just checking one or the other. It also suggested the `check_guess(5, 42)` test case specifically because it exposes string vs. int comparison differences.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

Streamlit reruns the entire script from top to bottom every time the user interacts with the page (clicking a button, typing in a field, etc.). If you generate a random number with `random.randint()` outside of `st.session_state`, it gets regenerated on every rerun, so the secret changes after each interaction. The original app already used `st.session_state` to store the secret, so the number was stable during gameplay, but the "New Game" button reset it using `random.randint(1, 100)` with a hardcoded range instead of using the difficulty-based range.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Think of Streamlit like a whiteboard that gets erased and redrawn every time you click anything. Any variable you define normally gets wiped and recreated from scratch on each redraw. `st.session_state` is like a sticky note on the side of the whiteboard, it stays the same between redraws. If you want to remember something (like the secret number or the player's score), you have to put it in `session_state`, otherwise it resets every time the user does anything.

- What change did you make that finally gave the game a stable secret number?

The secret was already stored in `st.session_state.secret` with an `if "secret" not in st.session_state` guard, so it persisted between reruns. The main fix was ensuring the secret was always compared as an integer (removing the string casting on even attempts), which made the game behave consistently on every attempt.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

Writing targeted pytest cases immediately after fixing a bug. It forced me to think clearly about what "correct" behavior actually looks like, and it gave me confidence that my fix worked without having to manually replay the game every time. I also liked using the Debug Info panel for manual verification.

- What is one thing you would do differently next time you work with AI on a coding task?

I would be more skeptical of AI suggestions that label something as a "bug" without a clear spec to back it up. Claude Code confidently called the scoring formula a bug, but it was really just a design choice. Next time, I'll ask the AI to explain the its logic and compare to mine before accepting its suggestions.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

AI-generated code can look clean and production-ready while hiding subtle logic errors that only show up during actual gameplay. This project taught me that AI is a powerful starting point, but human review and testing are essential. The AI that wrote the bugs was just as confident as the AI that found them.
