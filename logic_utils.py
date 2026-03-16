def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX: Was returning 1-50 which is a smaller range than Normal, making Hard actually easier.
    # Hard should have a larger range to make guessing harder.
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str, min_val: int, max_val: int):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < min_val or value > max_val:
        return False, None, f"Guess must be between {min_val} and {max_val}."

    return True, value, None


# FIX: Removed the on-every-other-turn string conversion that caused numeric comparisons
# to break (e.g. "100" < "64" lexicographically, so guess of 100 appeared lower than 64).
# FIX: Corrected hint direction — when guess > secret the outcome is "Too High" (go lower),
# and when guess < secret the outcome is "Too Low" (go higher). Previously the messages
# displayed to the player were swapped, sending them in the wrong direction.
def check_guess(guess, secret):
    """
    Compare guess to secret and return outcome string.

    outcome: "Win", "Too High", or "Too Low"
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
