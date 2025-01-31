import pytest
from unittest.mock import patch, MagicMock
from models.train import Train

# ---------- FIXTURES FOR SETUP ----------
@pytest.fixture
def setup_train():
    train = Train("T1", "Express", ("Station1", "Station2"))
    return train

# ---------- TEST CASES ----------
@patch('builtins.input', side_effect=["C1", "100", "General"])
def test_add_coach(mock_input, setup_train):
    train = setup_train
    train.add_coach()
    assert "C1" in train._coach

@patch('builtins.input', side_effect=["C1", "100", "General"])
def test_add_coach_with_existing_id(mock_input, setup_train):
    train = setup_train
    train.add_coach()
    result= train.add_coach()
    assert result is False

@patch('builtins.input', side_effect=["C1", "100", "General"])
def test_remove_coach(mock_input, setup_train):
    train = setup_train
    train.add_coach()
    with patch('builtins.input', side_effect=["C1"]):
        train.remove_coach()
    assert "C1" not in train._coach

@patch('builtins.input', side_effect=["C1"])
def test_remove_nonexistent_coach(mock_input, setup_train):
    train = setup_train
    result= train.remove_coach()
    assert result is False

@patch('builtins.input', side_effect=["C1", "100", "General"])
def test_available_tickets(mock_input, setup_train):
    train = setup_train
    train.add_coach()
    assert train.available_tickets() == 100

@patch('builtins.input', side_effect=["C1", "100", "General"])
def test_available_tickets_by_coach(mock_input, setup_train):
    train = setup_train
    train.add_coach()
    available_tickets = train.available_tickets_by_coach()
    assert available_tickets == [("C1", 100)]

@patch('builtins.input', side_effect=["C1", "100", "General"])
def test_total_tickets(mock_input, setup_train):
    train = setup_train
    train.add_coach()
    assert train.total_tickets() == 100

@patch('builtins.input', side_effect=["Station1", "10:00", "10:15"])
def test_display_schedule(mock_input, setup_train):
    train = setup_train
    train.update_schedule()
    assert train.display_schedule() is True

@patch('builtins.input', side_effect=["Station1", "10:00", "10:15"])
def test_update_schedule(mock_input, setup_train):
    train = setup_train
    assert train.update_schedule() is True

@patch('builtins.input', side_effect=["Station1", "10:00", "10:15"])
def test_update_schedule_existing_station(mock_input, setup_train):
    train = setup_train
    train.update_schedule()
    with patch('builtins.input', side_effect=["Station1", "11:00", "11:15"]):
        assert train.update_schedule() is False

@patch('builtins.input', side_effect=["C1", "100", "General"])
def test_get_passenger_list(mock_input, setup_train):
    train = setup_train
    train.add_coach()
    passenger_list = train.get_passenger_list()
    assert passenger_list == {}