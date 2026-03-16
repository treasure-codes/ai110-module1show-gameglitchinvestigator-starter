# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

---

## Bugs Found

### Bug 1: The Hint Direction is Backwards

In the `check_guess` function, the hint messages are swapped. When your guess is higher than the secret number, the code correctly identifies it as "Too High" — but then it tells you to "Go HIGHER!" instead of "Go LOWER!" The same is true in reverse: when your guess is too low, it tells you to go lower when it should tell you to go higher. This is why the secret being 64 led to guesses of 77, 87, 95, 99, and beyond — every time a guess was above 64, the game said to keep going higher. The labels "Too High" and "Too Low" are correct internally, but the user-facing hint messages point in the wrong direction.

### Bug 2: New Game Does Not Reset the Game Status

When you click the New Game button, the code resets your attempt count and picks a new secret number, but it never resets the game's status back to "playing." After a game ends (either by winning or running out of attempts), the status gets set to "won" or "lost." When you start a new game, that status stays stuck on the old value. The very next time the page loads, the code checks whether the status is "playing" and if it isn't, it stops the page from doing anything else. This means the guess input and submit button are completely blocked — no matter what you type, nothing happens — because the status was never cleared.

### Bug 3: Hard Difficulty Has a Smaller Range Than Normal

The `get_range_for_difficulty` function sets the number range for Hard mode to 1–50, which is actually a smaller range than Normal mode's 1–100. A smaller range means there are fewer possible numbers to guess from, which makes the game easier to win, not harder. Hard should have a larger range than Normal to increase difficulty, but right now it cuts the range in half. This means players who pick Hard are actually getting an easier guessing challenge than those who pick Normal.

---

## 1. What was broken when you started?

When I first ran the game, it looked functional on the surface — there was an input box, a submit button, and a hint checkbox — but playing it quickly revealed it was completely broken. No matter what number I guessed, the hint kept telling me to go higher, even when I was already at 99 and the secret number was 64. After losing a game and clicking "New Game," the input field stopped accepting guesses entirely, freezing the game in a dead state. Choosing "Hard" difficulty actually made the game easier because the number range shrank to 1–50 instead of expanding.

Concrete bugs noticed at the start:
- **The hints were backwards** — guessing 77 when the answer was 64 told me to "Go HIGHER!" instead of "Go LOWER!"
- **New game froze the app** — after any game ended, clicking "New Game" left the game in a broken state where submitting guesses did nothing.
- **Hard difficulty had a smaller range than Normal** — Hard was 1–50, Normal was 1–100, so Hard was actually the easiest setting.

---

## 2. How did you use AI as a teammate?

I used Claude (Claude Code) as my AI tool throughout this project, using it both for codebase analysis and for generating fixes and tests.

**Correct AI suggestion:** I asked the AI to explain why the hint was always wrong. It correctly identified that the `check_guess` function in `app.py` had the outcome labels right but the user-facing messages swapped — "Too High" was mapped to "Go HIGHER!" when it should say "Go LOWER!" The AI also spotted a second layer of the same bug: on every even-numbered attempt, the code secretly converted the secret number to a string, causing lexicographic comparisons where `"100" < "64"` because `"1" < "6"`. I verified this by adding `print` statements in a local test and confirming that guessing 100 against a secret of 64 returned "Too Low" instead of "Too High" in the original code.

**Incorrect or misleading AI suggestion:** When I first asked for a quick fix to the new-game freeze, the AI initially suggested clearing only `st.session_state.attempts` and `st.session_state.secret`. That fix was incomplete — it didn't reset `st.session_state.status`, so the game still hit the `st.stop()` block on the next render and remained frozen. I caught this by actually running the game after applying the partial fix, seeing it still freeze, and then reading the code carefully to find the `status` check that was blocking execution.

---

## 3. Debugging and testing your fixes

I decided a bug was truly fixed only when two things were both true: the pytest test targeting that bug passed, and I manually played the game in the browser and observed the correct behavior with my own eyes. Passing tests alone weren't enough — for the new-game freeze bug there was no automated test, so I had to play a full game to losing, click New Game, and confirm I could submit a guess on the new round.

For the hint direction bug, I wrote two targeted pytest tests in `tests/test_game_logic.py`:

```python
def test_hint_not_backwards_too_high():
    result = check_guess(99, 64)
    assert result == "Too High"

def test_hint_not_backwards_too_low():
    result = check_guess(1, 64)
    assert result == "Too Low"
```

Running `pytest` before the fix caused both tests to fail (or in the original code, `check_guess` raised errors because it wasn't implemented in `logic_utils.py` yet). After moving the corrected function into `logic_utils.py`, both tests passed, which confirmed the fix was real and not just masking the symptom. The AI helped design these tests by suggesting that a good regression test should use the exact values from the original failure — in this case, the guess of 99 against the secret of 64 from my actual play session.

---

## 4. What did you learn about Streamlit and state?

In the original app, the secret number was being generated with `random.randint(low, high)` at the top of the script without any guard. Every time you clicked Submit, Streamlit re-ran the entire `app.py` file from top to bottom, which called `random.randint` again and picked a brand-new secret. The number you were trying to guess was changing on every single click.

Streamlit "reruns" work like this: every button click or user interaction causes Streamlit to throw away the current page and re-execute your entire Python script as if it's starting fresh. This would lose everything — your score, your guess history, the secret number — except Streamlit provides `st.session_state`, a special dictionary that survives reruns. Anything you store in `st.session_state` stays in memory between reruns. Think of it like a notepad that Streamlit holds for you across page refreshes, while everything else on the page gets wiped and redrawn.

The fix that gave the game a stable secret number was wrapping the `random.randint` call in an `if "secret" not in st.session_state:` guard. This means the secret is only generated once — the very first time the page loads. Every subsequent rerun skips that line entirely and reads the already-stored value from session state.

---

## 5. Looking ahead: your developer habits

One habit I want to carry into future projects is writing a targeted regression test the moment I identify a bug, before writing the fix. In this project, writing `test_hint_not_backwards_too_high` before touching `check_guess` meant I had a clear, objective definition of "fixed" and I couldn't accidentally close the issue by changing unrelated code. It also meant that if the bug ever comes back, the test will catch it immediately.

Next time I work with AI on a coding task, I would give the AI a smaller, more specific scope for each question instead of asking it to "fix the bug." Vague prompts produced incomplete suggestions, like the partial new-game fix that missed the status reset. Focused prompts — "explain exactly why line 162 of app.py causes wrong comparisons on even attempts" — produced much more precise and useful answers.

This project changed the way I think about AI-generated code by showing me that AI can write code that looks completely reasonable and compiles without errors but contains subtle logic bugs that only appear during real gameplay. The original app was well-structured and readable — it just had wrong values in the wrong places — which means you can't trust AI-written code just because it looks professional or runs without crashing.
