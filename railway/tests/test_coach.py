import pytest
from unittest.mock import patch, MagicMock
from models.coach import Coach

# ---------- FIXTURES FOR SETUP ----------
@pytest.fixture
def setup_coach():
    coach = Coach("C1", 100, "General")
    return coach

# ---------- TEST CASES ----------
def test_find_empty_seat(setup_coach):
    coach = setup_coach
    assert coach.find_empty_seat() == 1

@patch('builtins.input', side_effect=["John Doe", "30", "Male", "1234567890"])
def test_book_seat(mock_input, setup_coach):
    coach = setup_coach
    seat_number, name = coach.book_seat()
    assert seat_number is not None
    assert seat_number == 1
    assert name == "John Doe"

@patch('builtins.input', side_effect=["John Doe", "30", "Male", "1234567890"])
def test_book_seat_no_empty_seat(mock_input, setup_coach):
    coach = setup_coach
    for _ in range(100):
        coach.book_seat()
    result=coach.book_seat()
    assert result is None

@patch('builtins.input', side_effect=["John Doe", "30", "Male", "1234567890"])
def test_cancel_booking(mock_input, setup_coach):
    coach = setup_coach
    coach.book_seat()
    assert coach.cancel_booking(1) is True

def test_cancel_nonexistent_booking(setup_coach):
    coach = setup_coach
    assert coach.cancel_booking(1) is False

@patch('builtins.input', side_effect=["John Doe", "30", "Male", "1234567890"])
def test_cancel_booking_invalid_seat_number(mock_input, setup_coach):
    coach = setup_coach
    coach.book_seat()
    assert coach.cancel_booking(101) is False

@patch('builtins.input', side_effect=["John Doe", "-1", "Male", "1234567890"])
def test_book_seat_invalid_age(mock_input, setup_coach):
    coach = setup_coach
    result = coach.book_seat()
    assert result is None

@patch('builtins.input', side_effect=["John Doe", "30", "Male", "invalid_contact"])
def test_book_seat_invalid_contact(mock_input, setup_coach):
    coach = setup_coach
    result = coach.book_seat()
    assert result is None

@patch('builtins.input', side_effect=["John Doe", "30", "Unknown", "1234567890"])
def test_book_seat_invalid_gender(mock_input, setup_coach):
    coach = setup_coach
    result = coach.book_seat()
    assert result is None