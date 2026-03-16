from logic_utils import check_guess, get_range_for_difficulty, parse_guess

# --- Starter tests ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

# --- Bug 1 fix: hint direction ---
# Verifies that "Too High" and "Too Low" are never swapped.

def test_hint_not_backwards_too_high():
    # Guess of 99 against secret of 64 must be "Too High", not "Too Low"
    result = check_guess(99, 64)
    assert result == "Too High"

def test_hint_not_backwards_too_low():
    # Guess of 1 against secret of 64 must be "Too Low", not "Too High"
    result = check_guess(1, 64)
    assert result == "Too Low"

# --- Bug 3 fix: Hard difficulty range ---
# Verifies that Hard has a larger range than Normal.

def test_hard_range_larger_than_normal():
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert (hard_high - hard_low) > (normal_high - normal_low), (
        "Hard difficulty should have a larger number range than Normal"
    )

def test_easy_range_smaller_than_normal():
    normal_low, normal_high = get_range_for_difficulty("Normal")
    easy_low, easy_high = get_range_for_difficulty("Easy")
    assert (easy_high - easy_low) < (normal_high - normal_low), (
        "Easy difficulty should have a smaller number range than Normal"
    )

# --- Edge case tests ---

def test_parse_guess_rejects_out_of_range():
    ok, _, err = parse_guess("200", 1, 100)
    assert ok is False
    assert err is not None

def test_parse_guess_rejects_text():
    ok, _, err = parse_guess("abc", 1, 100)
    assert ok is False

def test_parse_guess_accepts_valid():
    ok, value, err = parse_guess("50", 1, 100)
    assert ok is True
    assert value == 50
    assert err is None

def test_parse_guess_handles_decimal():
    ok, value, err = parse_guess("42.9", 1, 100)
    assert ok is True
    assert value == 42

def test_parse_guess_rejects_negative():
    ok, _, err = parse_guess("-5", 1, 100)
    assert ok is False
