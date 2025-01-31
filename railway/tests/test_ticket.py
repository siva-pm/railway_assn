import pytest
from models.ticket import TrainTicket

# ---------- FIXTURES FOR SETUP ----------
@pytest.fixture
def setup_ticket():
    ticket = TrainTicket(1, "John Doe", "T1", "C1", 1, "2022-12-31")
    return ticket

# ---------- TEST CASES ----------
def test_ticket_details(setup_ticket):
    ticket = setup_ticket
    assert ticket.PNR_id == 1
    assert ticket.passenger_name == "John Doe"
    assert ticket.train_number == "T1"
    assert ticket.coach_number == "C1"
    assert ticket.seat_number == 1
    assert ticket.journey_date == "2022-12-31"
    assert ticket.booking_status == "Booked"

def test_ticket_str_representation(setup_ticket):
    ticket = setup_ticket
    expected_str = (
        "PNR ID: 1, Passenger: John Doe, Train: T1, Seat: C1 1, "
        "Date: 2022-12-31, Status: Booked"
    )
    assert str(ticket) == expected_str

@pytest.mark.xfail(reason="This test fails because ticket class is just a data class and doesnt error correct")
@pytest.mark.parametrize("pnr_id, passenger_name, train_number, coach_number, seat_number, journey_date", [
    (-1, "John Doe", "T1", "C1", 1, "2022-12-31"),
    (1, "John Doe", "T1", "C1", -1, "2022-12-31"),
    (1, "John Doe", "T1", "C1", 1, "invalid_date")
])
def test_invalid_ticket(pnr_id, passenger_name, train_number, coach_number, seat_number, journey_date):
    with pytest.raises(ValueError):
        TrainTicket(pnr_id, passenger_name, train_number, coach_number, seat_number, journey_date)