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

**Game purpose:** A number-guessing game where the player tries to identify a secret number within a limited number of attempts. Hints tell you whether your guess was too high or too low, and your score changes based on how quickly you find the answer.

**Bugs found:**
1. **Backwards hints** — "Too High" displayed "Go HIGHER!" and "Too Low" displayed "Go LOWER!", sending the player in the wrong direction every turn.
2. **New game freeze** — clicking "New Game" after a game ended never reset `st.session_state.status`, so `st.stop()` blocked all input on the next render.
3. **Hard difficulty easier than Normal** — Hard was set to a range of 1–50 while Normal was 1–100, making Hard the easiest setting instead of the hardest.

**Fixes applied:**
1. Corrected the hint messages in `OUTCOME_MESSAGES` so "Too High" maps to "Go LOWER!" and "Too Low" maps to "Go HIGHER!"
2. Added `st.session_state.status = "playing"` inside the new-game handler in `app.py`.
3. Changed the Hard range in `get_range_for_difficulty` from `(1, 50)` to `(1, 200)`.
4. Refactored all game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) out of `app.py` and into `logic_utils.py`.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
