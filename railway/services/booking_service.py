from models.ticket import TrainTicket
from .payment_service import PaymentService
from typing import Optional
import uuid

def book_seat(admin,user) -> Optional[TrainTicket]:
    try:
        train_id = input("Enter Train ID: ").strip()
        if admin._trains[train_id]:
            train=admin._trains[train_id]
        else:
            print(f"No such train with train id {train_id}")
            return None

        if train.available_tickets()>0:    
            for coach_id, coach in train.coach.items():
                if coach.available_seats>0:  
                    seat_number,name = coach.book_seat() #books a seat and returns the seat_number 
                    if seat_number:
                        print(f"Seat {seat_number} booked successfully in coach {coach_id}!")
                        payment_status = PaymentService.process_payment(seat_number)
                        if payment_status:
                            print("Payment processed successfully!")
                            ticket=TrainTicket(pnr=uuid.uuid4(), passenger_name=name,train_name=train.name,seat_number=seat_number,journey_date="2022-12-31",booking_status="Booked")
                            user.add_ticket(ticket)
                            return ticket 
                        else:
                            print("Payment failed. Booking will be canceled.")
                            coach.cancel_booking(seat_number) 
                            return None   
                    else:
                        print(f"No available seat in coach {coach_id}. Checking next coach.")
    except Exception as e:
        print(f"An error occurred during booking: {e}")
        return None
                
    print("No available seats in any coach. Please try again later.")
    return None

def cancel_booking(admin,user) -> bool:
    try:
        train_id = input("Enter Train ID: ").split()
        if train_id not in admin._trains:
            print(f"No such train with train id {train_id}")
            return False

        train = admin._trains[train_id]    

        coach_id = input("Enter Coach ID: ").strip().upper()
        if coach_id not in train._coach:
            print(f"No such coach with coach Id {coach_id} in train {train_id}")
            return False

        coach = train._coach[coach_id]
          
        seat_number = int(input("Enter Seat Number: ").strip())
        cancellation_status = coach.cancel_booking(seat_number)

        if cancellation_status:
            print(f"Seat {seat_number} in coach {coach_id} canceled successfully.")
            user.remove_ticket(seat_number, coach_id, train_id)

            refund_status = PaymentService.process_refund(seat_number)
            if refund_status:
                print("Refund processed successfully!")
                return True
            else:
                print("Refund processing failed. Please contact support.")
                return False 
        else:
            print(f"Seat {seat_number} in coach {coach_id} is not currently booked. Cancellation failed.")
            return False
        
    except Exception as e:
        print(f"An error occurred during cancellation: {e}")
        return False
