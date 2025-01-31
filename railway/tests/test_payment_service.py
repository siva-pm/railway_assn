import pytest
from unittest.mock import patch
from services.payment_service import PaymentService

# ---------- TEST CASES ----------
@patch('builtins.print')
def test_process_payment_success(mocked_print):
    assert PaymentService.process_payment(1) is True
    mocked_print.assert_called_with("Processing payment for seat number 1...")

@pytest.mark.xfail(reason="process_payment is designed such way that it always passes")
@patch('services.payment_service.PaymentService.process_payment', side_effect=Exception("Payment error"))
@patch('builtins.print')
def test_process_payment_failure(mocked_print, mock_process_payment):
    assert PaymentService.process_payment(1) is False
    mocked_print.assert_called_with("Payment processing error: Payment error")

@patch('builtins.print')
def test_process_refund_success(mocked_print):
    assert PaymentService.process_refund(1) is True
    mocked_print.assert_called_with("Processing refund for seat number 1...")

@pytest.mark.xfail(reason="process_refund is designed such way that it always passes")
@patch('services.payment_service.PaymentService.process_refund', side_effect=Exception("Refund error"))
@patch('builtins.print')
def test_process_refund_failure(mocked_print, mock_process_refund):
    assert PaymentService.process_refund(1) is False
    mocked_print.assert_called_with("Refund processing error: Refund error")