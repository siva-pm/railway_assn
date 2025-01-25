class PaymentService:
    @staticmethod
    def process_payment(seat_number: int) -> bool:
        try:
            print(f"Processing payment for seat number {seat_number}...")
            return True
        except Exception as e:
            print(f"Payment processing error: {str(e)}")
            return False

    @staticmethod
    def process_refund(seat_number: int) -> bool:
        try: 
            print(f"Processing refund for seat number {seat_number}...")
            return True
        except Exception as e:
            print(f"Refund processing error: {str(e)}")
            return False
