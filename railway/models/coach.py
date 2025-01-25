from typing import Dict,TypeVar,Generic,Optional
from .passenger import Passenger

P = TypeVar('P', bound=Passenger)

class Coach(Generic[P]):
    def __init__(self, coach_id: str, total_seats: int, coach_type: str):
        self._coach_id = coach_id
        self._total_seats = total_seats
        self._available_seats = total_seats
        self._coach_type = coach_type
        self._seat: Dict[int,Optional[Passenger]]={i: None for i in range(1,self._total_seats+1)}
        self.seat_number :int =0

    @property
    def coach_id(self) -> str:
        return self._coach_id

    @property
    def total_seats(self) -> int:
        return self._total_seats

    @property
    def available_seats(self) -> int:
        return self._available_seats

    @property
    def coach_type(self) -> str:
        return self._coach_type
    
    @property
    def seat(self) -> Dict[int,bool]:
        return self._seat

    def find_empty_seat(self) -> bool:          #helper fn to get an empty seat_number
        for seat_number in self._total_seats:  
            if self._seat[seat_number] is None: 
                self.seat_number = seat_number  
                return True 
        return False  

    def book_seat(self) ->  int:        #gets the seat number as input and marks the seat booked
        try:     
            if not self.find_empty_seat():   #if no empty seat found
                return 0
              
            while(True):                                #get user input for a passenger while booking
                try:
                    pnr_id = int(input("Enter Passenger PNR ID: "))
                    name = input("Enter Passenger Name: ")
                    age = int(input("Enter Age: "))
                    gender = input("Enter Gender (Male/Female): ")
                    contact = input("Enter Contact Number: ")
                    if not name.strip():
                        raise ValueError("Name cannot be empty.")
                    if gender.lower() not in {"male", "female"}:
                        raise ValueError("Gender must be 'Male' or 'Female'.")
                    if not contact.isdigit() or len(contact) != 10:
                        raise ValueError("Contact number must be a valid 10-digit number.")
                    break
                except ValueError as e:
                    print(f"Invalid input: {e}. Please enter correct details.")
                    
            self._seat[self.seat_number] = Passenger(pnr_id, name, age, gender, contact)
            self._available_seats = max(0, self._available_seats - 1)  # Ensure it doesn't go below 0
            print(f"Seat {self.seat_number} successfully booked")
            return self.seat_number
        
        except Exception as e:
            print(f"An unexpected error occurred while booking seat {self.seat_number}: {e}")
            return 0
   
    def cancel_booking(self,seat_number: int) -> bool:    #gets the seat number as input and deletes the seat
        try:
            if seat_number in self._seat:
                if self._seat[seat_number]:
                    self._seat[seat_number]= None
                    self._available_seats+=1
                    print(f"Seat {seat_number} successfully cancelled")        
                    return True
                else:
                    print(f"Seat {seat_number} already vacant")
                    return False
            else:
                print(f"Invalid seat number {seat_number}/n")
                return False
        except KeyError:
            print(f"KeyError: Seat number {seat_number} not found in the seat map.")
            return False
        except TypeError as e:
            print(f"TypeError: Invalid input for seat number. Error details: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error occurred while canceling booking for seat {seat_number}: {e}")
            return False

