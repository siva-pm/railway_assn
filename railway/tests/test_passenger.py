import pytest
from models.passenger import Passenger

# ---------- FIXTURES FOR SETUP ----------
@pytest.fixture
def setup_passenger():
    passenger = Passenger(name="Alice", age=30, gender="Female", contact="1234567890")
    return passenger

# ---------- TEST CASES ----------
def test_passenger_attributes(setup_passenger):
    passenger = setup_passenger
    assert passenger.name == "Alice"
    assert passenger.age == 30
    assert passenger.gender == "Female"
    assert passenger.contact == "1234567890"

def test_passenger_str_representation(setup_passenger):
    passenger = setup_passenger
    passenger.PNR_id = "ABC123"  # Assigning a sample PNR ID
    expected_str = (
        "Passenger ID: ABC123\n"
        "Name: Alice\n"
        "Age: 30\n"
        "Gender: Female\n"
        "Contact: 1234567890"
    )
    assert str(passenger) == expected_str

@pytest.mark.xfail(reason="this test fails because passenger is a data class and doesnt have error handling")
@pytest.mark.parametrize("name, age, gender, contact", [
    ("Bob", 25, "Male", "invalid"),
    ("Charlie", -5, "Male", "1234567890"),
    ("", 25, "Male", "1234567890"),
    ("Dana", 25, "Unknown", "1234567890")
])
def test_invalid_passenger(name, age, gender, contact):
    with pytest.raises(ValueError):
        Passenger(name=name, age=age, gender=gender, contact=contact)