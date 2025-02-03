import pytest
from unittest.mock import patch, MagicMock
from models.ticket import TrainTicket
from services.booking_service import cancel_booking, book_seat

# ---------- FIXTURES FOR SETUP ----------
@pytest.fixture
def setup_admin():
    admin = MagicMock()
    
    train = MagicMock()
    train.train_id = "T1"
    train.name = "Express"
    train.available_tickets.return_value = 15

    coach = MagicMock()
    coach.coach_id = "C1"
    coach.available_seats = 10
    coach.book_seat.return_value = (42, "John Doe")  
    coach.cancel_booking.return_value = True  

    train._coach = {"C1": coach} 
    admin._trains = {"T1": train}  
    
    return admin, train, coach

@pytest.fixture
def setup_user():
    user = MagicMock()
    return user

# ---------- TEST CASES ----------
@patch("builtins.input", side_effect=["T1", "C1", "John Doe", "30", "Male", "1234567890"])  
@patch("services.payment_service.PaymentService.process_payment", return_value=True) 
def test_book_seat_success(mock_payment, mock_input, setup_admin, setup_user):
    admin, train, coach = setup_admin
    user = setup_user

    book_status = book_seat(admin, user)

    assert book_status is True

    coach.book_seat.assert_called_once()
    mock_payment.assert_called_once()
    user.add_ticket.assert_called_once_with("John Doe","T1","C1",42)

@patch("builtins.input", side_effect=["T1", "C1", "42"])  
@patch("services.payment_service.PaymentService.process_refund", return_value=True)  
def test_cancel_booking_success(mock_refund, mock_input, setup_admin, setup_user):
    admin, train, coach = setup_admin
    user = setup_user

    result = cancel_booking(admin, user)

    assert result is True
    coach.cancel_booking.assert_called_once_with(42)
    user.remove_ticket.assert_called_once_with(42, "C1", "T1")
    mock_refund.assert_called_once()

@patch("builtins.input", side_effect=["T1", "C1", "42"]) 
@patch("services.payment_service.PaymentService.process_refund", return_value=True) 
def test_cancel_booking_already_vacant(mock_refund, mock_input, setup_admin, setup_user):
    admin, train, coach = setup_admin
    user = setup_user

    coach.cancel_booking.return_value = False  

    result = cancel_booking(admin, user)

    assert result is False
    coach.cancel_booking.assert_called_once_with(42)
    mock_refund.assert_not_called()

@patch("builtins.input", side_effect=["T1", "C1", "John Doe", "30", "Male", "1234567890"])  
@patch("services.payment_service.PaymentService.process_payment", return_value=False) 
def test_book_seat_payment_failure(mock_payment, mock_input, setup_admin, setup_user):
    admin, train, coach = setup_admin
    user = setup_user

    book_status = book_seat(admin, user)

    assert book_status is False
    coach.book_seat.assert_called_once()
    mock_payment.assert_called_once()
    coach.cancel_booking.assert_called_once()

@patch("builtins.input", side_effect=["T1", "C1", "John Doe", "30", "Male", "1234567890"])  
def test_book_seat_no_available_seats(mock_input, setup_admin, setup_user):
    admin, train, coach = setup_admin
    user = setup_user

    coach.available_seats = 0

    book_status = book_seat(admin, user)

    assert book_status is False

@patch("builtins.input", side_effect=["T1", "C1", "42"])  
@patch("services.payment_service.PaymentService.process_refund", return_value=False)  
def test_cancel_booking_refund_failure(mock_refund, mock_input, setup_admin, setup_user):
    admin, train, coach = setup_admin
    user = setup_user

    result = cancel_booking(admin, user)

    assert result is False
    coach.cancel_booking.assert_called_once_with(42)
    user.remove_ticket.assert_called_once_with(42, "C1", "T1")
    mock_refund.assert_called_once()

@patch("builtins.input", side_effect=["T1", "invalid_coach", "42"])  
def test_cancel_booking_invalid_coach_id(mock_input, setup_admin, setup_user):
    admin, train, coach = setup_admin
    user = setup_user

    result = cancel_booking(admin, user)

    assert result is False
    coach.cancel_booking.assert_not_called()
    user.remove_ticket.assert_not_called()

@patch("builtins.input", side_effect=["T1", "C1", "invalid_seat"])  
def test_cancel_booking_invalid_seat_number(mock_input, setup_admin, setup_user):
    admin, train, coach = setup_admin
    user = setup_user

    result = cancel_booking(admin, user)

    assert result is False
    coach.cancel_booking.assert_not_called()
    user.remove_ticket.assert_not_called()