# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

When I first ran the game, it appeared to be a normal, functional number guessing game, complete with difficulty settings, a guess input, and a scoring system. However, it quickly became clear that something was off: the hints were pointing me in the wrong direction, and the game felt inconsistent between attempts.

- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").

The first bug I noticed was that the hints were backwards. When my guess was too high, the game told me to "Go HIGHER," and when it was too low, it said "Go LOWER," which sent me in the wrong direction every time. The second bug was that on even-numbered attempts, the game compared my integer guess against a string version of the secret number, which caused the comparison logic to break and give unreliable results. I also noticed that "Hard" difficulty actually used a smaller range (1–50) than "Normal" (1–100), making it easier instead of harder.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude Code for this project. I asked it to run the app, read the source code, and identify bugs. I then used it to refactor the game logic from `app.py` into `logic_utils.py`, fix the bugs, and generate pytest cases.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

Claude Code correctly identified that the hint messages in the `check_guess` function were swapped: when the guess was too high, the code returned "Go HIGHER!" instead of "Go LOWER!" It suggested swapping the two hint strings. I verified this by opening the Developer Debug Info expander to see the secret number, then deliberately guessing above it. Before the fix, the game said "Go HIGHER" — after the fix it correctly said "Go LOWER." I also wrote a pytest (`test_too_high_hint_says_lower`) that asserts the message contains "LOWER" when the guess is too high, and it passed.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Claude Code flagged the scoring formula `100 - 10 * (attempt_number + 1)` in `update_score` as a bug, claiming the `+ 1` penalizes players for winning early. It suggested removing the `+ 1` so winning on attempt 1 gives 90 points instead of 80. However, without a design spec, this is ambiguous — it could be an intentional difficulty curve. I verified by manually computing scores: attempt 1 gives 80, attempt 2 gives 70, etc. The progression is consistent and reasonable, just slightly more aggressive than expected. I decided not to change it, since "different than expected" is not the same as "broken," and the AI was too confident in calling it a definitive bug.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I used two approaches: manual testing in the live Streamlit app and automated pytest cases. For manual testing, I opened the Developer Debug Info panel to see the secret number, then made deliberate guesses above and below it to confirm hints pointed the right direction. A bug was only "fixed" when both the manual playthrough and the automated tests agreed.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

I ran `pytest tests/test_game_logic.py -v` which included 7 tests. One key test, `test_too_high_hint_says_lower`, calls `check_guess(60, 50)` and asserts the returned message contains "LOWER." Before the fix this would have failed because the original code returned "Go HIGHER!" for a too-high guess. Another test, `test_check_guess_int_comparison_not_string`, calls `check_guess(5, 42)` and asserts the outcome is "Too Low" — this catches the string comparison bug because `"5" > "42"` is `True` in string ordering, which would have returned the wrong outcome. All 7 tests passed after the fixes.

- Did AI help you design or understand any tests? How?

Yes. I asked Claude Code to generate pytest cases targeting the two bugs I fixed. It wrote tests that checked both the outcome string ("Too High"/"Too Low") and the hint message content ("LOWER"/"HIGHER"), which was more thorough than just checking one or the other. It also suggested the `check_guess(5, 42)` test case specifically because it exposes string vs. int comparison differences — I wouldn't have thought of that edge case on my own.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
