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

def test_add_ticket(setup_user):
    user = setup_user
    ticket = TrainTicket(1, "John Doe", "T1", "C1", 1, "2022-12-31")
    user.add_ticket(ticket)
    assert ticket in user._ticket_list

def test_remove_ticket(setup_user):
    user = setup_user
    ticket = TrainTicket(1, "John Doe", "T1", "C1", 1, "2022-12-31")
    result_add= user.add_ticket(ticket)
    result = user.remove_ticket(1, "C1", "T1")
    assert result_add is True
    assert result is True
    assert ticket not in user._ticket_list

def test_remove_nonexistent_ticket(setup_user):
    user = setup_user
    result = user.remove_ticket(1, "C1", "T1")
    assert result is False

def test_display_tickets(setup_user):
    user = setup_user
    ticket = TrainTicket(1, "John Doe", "T1", "C1", 1, "2022-12-31")
    user.add_ticket(ticket)
    with patch('builtins.print') as mocked_print:
        user.display_tickets()
        mocked_print.assert_called_with(f"PNR: {ticket.PNR_id}, Train: {ticket.train_number}, Seat: {ticket.seat_number}")

@patch('builtins.input', side_effect=["0987654321"])
def test_update_profile(mock_input, setup_user):
    user = setup_user
    user.update_profile()
    assert user.contact == "0987654321"