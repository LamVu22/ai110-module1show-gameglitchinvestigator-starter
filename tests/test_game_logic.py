from logic_utils import check_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Tests targeting Bug 1: hint messages were swapped ---

def test_too_high_hint_says_lower():
    # Bug 1 fix: when guess is too high, message should say "LOWER", not "HIGHER"
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in hint but got: {message}"


def test_too_low_hint_says_higher():
    # Bug 1 fix: when guess is too low, message should say "HIGHER", not "LOWER"
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint but got: {message}"


# --- Tests targeting Bug 2: secret must always be compared as int ---

def test_check_guess_with_int_secret():
    # Bug 2 fix: secret should always be an int, not a string
    # Passing an int secret should work correctly
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_check_guess_int_comparison_not_string():
    # Verify that 5 > 42 is False (int comparison), not True (string comparison)
    outcome, message = check_guess(5, 42)
    assert outcome == "Too Low", f"Expected 'Too Low' but got '{outcome}' — possible string comparison bug"
