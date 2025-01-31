import pytest
from unittest.mock import patch, mock_open
from storage.data_storage import DataStorage
from management.user import UserManagement, Users
from management.admin import Admin
from models.train import Train
from models.ticket import TrainTicket
from models.coach import Coach
from models.passenger import Passenger
import json

# ---------- FIXTURES ----------
@pytest.fixture
def data_storage():
    return DataStorage()

@pytest.fixture
def user_management():
    return UserManagement()

@pytest.fixture
def admin():
    return Admin[Train]()

@pytest.fixture
def sample_ticket():
    return TrainTicket(
        pnr_id=1,
        passenger_name="John Doe",
        train_number="T1",
        coach_number="C1",
        seat_number=1,
        journey_date="2022-12-31",
        booking_status="Booked"
    )

@pytest.fixture
def sample_passenger():
    return Passenger(
        name="John Doe",
        age=30,
        gender="Male",
        contact="1234567890"
    )

# ---------- USER DATA TESTS ----------
def test_save_user_data_empty(data_storage, user_management):
    """Test saving user data with no users"""
    with patch('builtins.open', mock_open()) as mocked_file:
        data_storage.save_user_data(user_management)
        handle = mocked_file()
        saved_data = json.loads(handle.write.call_args[0][0])
        assert saved_data == {}

@pytest.mark.skip(reason="not studied yet")
def test_save_user_data_single_user(data_storage, user_management):
    """Test saving user data with a single user without tickets"""
    with patch('builtins.input', side_effect=["U1", "John Doe", "1234567890"]):
        user_management.register_user()
    
    with patch('builtins.open', mock_open()) as mocked_file:
        data_storage.save_user_data(user_management)
        handle = mocked_file()
        saved_data = json.loads(handle.write.call_args[0][0])
        
        assert "U1" in saved_data
        assert saved_data["U1"]["_name"] == "John Doe"  # Changed to _name
        assert saved_data["U1"]["_contact"] == "1234567890"  # Changed to _contact
        assert saved_data["U1"]["ticket_list"] == []

@pytest.mark.skip(reason="not studied yet")
def test_save_user_data_with_tickets(data_storage, user_management, sample_ticket):
    """Test saving user data with tickets"""
    with patch('builtins.input', side_effect=["U1", "John Doe", "1234567890"]):
        user_management.register_user()
        user = user_management.users["U1"]
        user.add_ticket(sample_ticket)
    
    with patch('builtins.open', mock_open()) as mocked_file:
        data_storage.save_user_data(user_management)
        handle = mocked_file()
        saved_data = json.loads(handle.write.call_args[0][0])
        
        assert len(saved_data["U1"]["ticket_list"]) == 1
        ticket_data = saved_data["U1"]["ticket_list"][0]
        assert ticket_data["passenger_name"] == "John Doe"
        assert ticket_data["train_number"] == "T1"
        assert ticket_data["seat_number"] == 1

@pytest.mark.parametrize("error", [IOError, OSError, FileNotFoundError])
def test_save_user_data_errors(data_storage, user_management, error):
    """Test error handling during user data saving"""
    with patch('builtins.open', mock_open()) as mocked_file:
        mocked_file.side_effect = error
        data_storage.save_user_data(user_management)
        # Should not raise exception

# ---------- USER DATA LOADING TESTS ----------
def test_load_user_data_empty(data_storage):
    """Test loading user data from empty file"""
    with patch('builtins.open', mock_open(read_data="{}")):
        users = data_storage.load_user_data()
        assert users == {}

def test_load_user_data_with_users(data_storage):
    """Test loading user data with existing users"""
    mock_data = {
        "U1": {
            "user_id": "U1",
            "name": "John Doe",
            "contact": "1234567890",
            "ticket_list": []
        }
    }
    
    with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
        users = data_storage.load_user_data()
        assert "U1" in users
        assert users["U1"].name == "John Doe"
        assert users["U1"].contact == "1234567890"

def test_load_user_data_with_tickets(data_storage):
    """Test loading user data with tickets"""
    mock_data = {
        "U1": {
            "user_id": "U1",
            "name": "John Doe",
            "contact": "1234567890",
            "ticket_list": [{
                "pnr": 1,
                "passenger_name": "John Doe",
                "train_number": "T1",
                "coach_number": "C1",
                "seat_number": 1,
                "journey_date": "2022-12-31",
                "booking_status": "Booked"
            }]
        }
    }
    
    with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
        users = data_storage.load_user_data()
        assert len(users["U1"]._ticket_list) == 1
        ticket = users["U1"]._ticket_list[0]
        assert ticket.passenger_name == "John Doe"
        assert ticket.train_number == "T1"
        assert ticket.seat_number == 1

# ---------- TRAIN DATA TESTS ----------
def test_save_train_data_empty(data_storage, admin):
    """Test saving train data with no trains"""
    with patch('builtins.open', mock_open()) as mocked_file:
        data_storage.save_train_data(admin)
        handle = mocked_file()
        saved_data = json.loads(handle.write.call_args[0][0])
        assert saved_data == {}

@pytest.mark.skip(reason="not studied yet")
def test_save_train_data_with_train(data_storage, admin):
    """Test saving train data with a train"""
    with patch('builtins.input', side_effect=["T1", "Express", "Station1", "Station2"]):
        admin.add_train()
    
    with patch('builtins.open', mock_open()) as mocked_file:
        data_storage.save_train_data(admin)
        handle = mocked_file()
        saved_data = json.loads(handle.write.call_args[0][0])
        
        assert "T1" in saved_data
        assert saved_data["T1"]["train_name"] == "Express"
        assert saved_data["T1"]["route"] == ["Station1", "Station2"]

@pytest.mark.skip(reason="not studied yet")
def test_save_train_data_with_coach(data_storage, admin, sample_passenger):
    """Test saving train data with coach and passenger"""
    with patch('builtins.input', side_effect=["T1", "Express", "Station1", "Station2"]):
        admin.add_train()
        train = admin._trains["T1"]
        coach = Coach("C1", 100, "General")
        coach._seat = {1: sample_passenger}
        train._coach = {"C1": coach}
    
    with patch('builtins.open', mock_open()) as mocked_file:
        data_storage.save_train_data(admin)
        handle = mocked_file()
        saved_data = json.loads(handle.write.call_args[0][0])
        
        assert "C1" in saved_data["T1"]["coaches"]
        coach_data = saved_data["T1"]["coaches"]["C1"]
        assert coach_data["coach_type"] == "General"
        assert coach_data["total_seats"] == 100
        assert coach_data["seats"]["1"]["name"] == "John Doe"

def test_load_train_data(data_storage):
    """Test loading train data with full configuration"""
    mock_data = {
        "T1": {
            "train_id": "T1",
            "train_name": "Express",
            "route": ["Station1", "Station2"],
            "schedule": {},
            "coaches": {
                "C1": {
                    "coach_id": "C1",
                    "total_seats": 100,
                    "available_seats": 99,
                    "coach_type": "General",
                    "seats": {
                        "1": {
                            "name": "John Doe",
                            "age": 30,
                            "gender": "Male",
                            "contact": "1234567890"
                        }
                    }
                }
            }
        }
    }
    
    with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
        trains = data_storage.load_train_data()
        assert "T1" in trains
        train = trains["T1"]
        assert train.train_name == "Express"
        assert "C1" in train._coach
        coach = train._coach["C1"]
        assert coach.coach_type == "General"
        assert coach._seat["1"].name == "John Doe"

@pytest.mark.parametrize(
    "error,expected",
    [
        (FileNotFoundError, {}),
        (json.JSONDecodeError("Msg", "Doc", 0), {}),
        (IOError, {})
    ]
)
def test_load_train_data_errors(data_storage, error, expected):
    """Test error handling during train data loading"""
    with patch('builtins.open') as mocked_file:
        if isinstance(error, json.JSONDecodeError):
            mocked_file.return_value.__enter__.return_value.read.return_value = "invalid json"
        else:
            mocked_file.side_effect = error
        
        trains = data_storage.load_train_data()
        assert trains == expected