from typing import Dict, TypeVar, Generic, Optional, Tuple
from abc import ABC, abstractmethod
from .passenger import Passenger

P = TypeVar('P', bound=Passenger)

class Coach_Model(ABC, Generic[P]):
    @abstractmethod
    def find_empty_seat(self) -> Optional[int]:
        pass

    @abstractmethod
    def book_seat(self) -> Optional[Tuple[int, str]]:
        pass

    @abstractmethod
    def cancel_booking(self, seat_number: int) -> bool:
        pass

class Coach(Coach_Model[P]):
    def __init__(self, coach_id: str, total_seats: int, coach_type: str):
        self._coach_id = coach_id
        self._total_seats = total_seats
        self._available_seats = total_seats
        self._coach_type = coach_type
        self._seat: Dict[int, Optional[P]] = {i: None for i in range(1, self._total_seats + 1)}

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

    def find_empty_seat(self) -> Optional[int]:
        try:
            for seat_number, passenger in self._seat.items():
                if passenger is None:
                    return seat_number
        except Exception as e:
            print(f"An error occured while finding an empty seat: {e}")
        return None

    def book_seat(self) -> Optional[Tuple[int, str]]:
        try:
            seat_number = self.find_empty_seat()
            if seat_number is None:
                print("No empty seats available.")
                return None
            
            name = input("Enter Passenger Name: ").strip()
            age = int(input("Enter Age: ").strip())
            gender = input("Enter Gender (Male/Female): ").strip().lower()
            contact = input("Enter Contact Number: ").strip()

            if age <= 0 or not name.strip() or gender.lower() not in {"male", "female"} or not contact.isdigit() or len(contact) != 10:
                raise ValueError("Invalid input data.")

            self._seat[seat_number] = Passenger(name, age, gender, contact)
            self._available_seats -= 1
            print(f"Seat {seat_number} successfully booked.")
            return seat_number, name
        except ValueError as ve:
            print(f"Invalid input: {ve}. Please enter correct details.")
        except Exception as e:
            print(f"Unknown error occurred while booking seat {e}")
        return None  

    def cancel_booking(self, seat_number: int) -> bool:
        try:
            if seat_number not in self._seat:
                print(f"Invalid seat number {seat_number}.")
                return False

            if self._seat[seat_number] is None:
                print(f"Seat {seat_number} is already vacant.")
                return False

            self._seat[seat_number] = None
            self._available_seats += 1
            print(f"Seat {seat_number} successfully cancelled.")
            return True
        except Exception as e:
            print(f"Error occured while cancelling seat {e}")
            return False

class LadiesCoach(Coach_Model[P]):
    def find_empty_seat(self) -> Optional[int]:
        print("Ladies Coach")
        return super().find_empty_seat()

    def book_seat(self) -> Optional[Tuple[int, str]]:
        print("Ladies Coach")
        return super().book_seat()

    def cancel_booking(self, seat_number: int) -> bool:
        print("Ladies Coach")
        return super().cancel_booking(seat_number)
