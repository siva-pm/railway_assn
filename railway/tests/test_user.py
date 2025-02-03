import pytest
from unittest.mock import patch, MagicMock
from management.user import UserManagement, Users
from models.ticket import TrainTicket

# ---------- FIXTURES FOR SETUP ----------
@pytest.fixture
def setup_user_management():
    user_management = UserManagement()
    return user_management

@pytest.fixture
def setup_user():
    user = Users("U1", "John Doe", "1234567890")
    return user

# ---------- TEST CASES ----------
@patch('builtins.input', side_effect=["U1", "John Doe", "1234567890"])
def test_register_user(mock_input, setup_user_management):
    user_management = setup_user_management
    user_management.register_user()
    assert "U1" in user_management.users
    assert user_management.users["U1"].name == "John Doe"
    assert user_management.users["U1"].contact == "1234567890"

@patch('builtins.input', side_effect=["U1", "John Doe", "1234567890"])
def test_register_user_existing_id(mock_input, setup_user_management):
    user_management = setup_user_management
    user_management.register_user()
    with patch('builtins.input', side_effect=["U1", "Jane Doe", "0987654321"]):
        user_management.register_user()
    assert user_management.users["U1"].name == "John Doe"

@patch('builtins.input', side_effect=["U1", "John Doe", "1234567890"])
def test_login(mock_input, setup_user_management):
    user_management = setup_user_management
    user_management.register_user()
    with patch('builtins.input', side_effect=["U1"]):
        user = user_management.login()
    assert user is not None
    assert user.name == "John Doe"

@patch('builtins.input', side_effect=["U1"])
def test_login_invalid_user(mock_input, setup_user_management):
    user_management = setup_user_management
    user = user_management.login()
    assert user is None

def test_remove_ticket(setup_user):
    user = setup_user
    result_add= user.add_ticket("John Doe","T1","C1",1)
    result = user.remove_ticket(1, "C1", "T1")
    assert result_add is True
    assert result is True
    assert user._ticket_list == []

def test_remove_nonexistent_ticket(setup_user):
    user = setup_user
    result = user.remove_ticket(1, "C1", "T1")
    assert result is False

def test_display_tickets(setup_user):
    user = setup_user
    user.add_ticket("John Doe","T1","C1",1)
    with patch('builtins.print') as mocked_print:
        user.display_tickets()
        mocked_print.assert_called_with(f"PNR: {user._ticket_list[0].PNR_id}, Train: {user._ticket_list[0].train_number}, Seat: {user._ticket_list[0].seat_number}, Coach: {user._ticket_list[0].coach_number}")

@patch('builtins.input', side_effect=["0987654321"])
def test_update_profile(mock_input, setup_user):
    user = setup_user
    user.update_profile()
    assert user.contact == "0987654321"

def test_add_ticket_success(setup_user):
    user = setup_user
    result = user.add_ticket("John Doe", "T1", "C1", 1)
    assert result is True
    assert len(user._ticket_list) == 1
    assert user._ticket_list[0].passenger_name == "John Doe"
    assert user._ticket_list[0].train_number == "T1"
    assert user._ticket_list[0].coach_number == "C1"
    assert user._ticket_list[0].seat_number == "1"

def test_add_ticket_failure(setup_user):
    user = setup_user
    with patch('uuid.uuid4', side_effect=Exception("UUID generation failed")):
        result = user.add_ticket("John Doe", "T1", "C1", 1)
    assert result is False
    assert len(user._ticket_list) == 0
