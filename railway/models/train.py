from typing import Dict,TypeVar,Generic,Tuple
from .coach import Coach

C = TypeVar('C', bound=Coach)

class Train(Generic[C]):
    def __init__(self, train_id: str, name: str, route: tuple[str,str]):
        self._train_id = train_id
        self._train_name = name
        self._route = route
        self._schedule: Dict[str, Tuple[str]]= {}  # Station-wise schedule
        self._coach:Dict[str,Coach] = {} # dictionary of coach objects with key as coach number

    def __str__(self):
        return (
            f"Train ID: {self._train_id}\n"
            f"Name: {self._train_name}\n"
            f"Route: {self._route[0]} -> {self._route[1]}\n"
            f"Number of Coaches: {len(self._coach)}\n"
            f"Total Passengers: {len(self.get_passenger_list())}"
        )

    def display_schedule(self):         #prints station, arrival time and departure time
        if not self._schedule:
            print("No schedule available.")
            return
        try:
            for station, timings in self._schedule.items():
                print(f"station:{station}    arrival:{timings[0]}    departure:{timings[1]}")
        except Exception as e:
            print(f"display schedule error{e}")

    def update_schedule(self):      #updates the existing schedule
        try:
            station = input("Enter Station Name: ")
            arrival = input("Enter Arrival Time: ")
            departure = input("Enter Departure Time: ")
            if not station or not arrival or not departure:
                raise ValueError("All fields (station, arrival, and departure) must be filled.")
            
            new_schedule:Dict[str,Tuple[str]] = {station: (arrival, departure)}            
            self._schedule.update(new_schedule)
            print("Schedule updated successfully!")
        
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"An error occurred while updating the schedule: {e}")
           
    def get_passenger_list(self) -> Dict[int,str]:      # return a dict, key= pnr id, value= passenger name
        try:
            passenger_info={}
            for coach_id, coach in self._coach.items():
                for seat_no, passenger in coach._seat.items():
                    if passenger is not None:
                        passenger_info[passenger.PNR_id] = passenger.name
            
            return passenger_info
        except Exception as e:
            print(f"Error fetching passenger list: {e}")
            return {}
             
    def add_coach(self):       #adds new coach in existing coach dict
        try:
            coach_id = input("Enter Coach ID: ")
            if coach_id in self._coach:
                raise ValueError(f"Coach with ID '{coach_id}' already exists.")
            total_seats = int(input("Enter Total Seats: "))
            coach_type = input("Enter Coach Type: ")
            
            new_coach:Dict[str,Coach] = {coach_id: Coach(coach_id=coach_id, total_seats=total_seats, coach_type=coach_type)}
            self._coach.update(new_coach)
            print(f"Coach with ID '{coach_id}' added successfully!")
        
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred while adding the coach: {e}")
        
    def remove_coach(self, coach_id: str):          #removes an exsiting coach entry
        try:    
            # Check if the coach ID exists
            if coach_id not in self._coach:
                raise KeyError(f"Coach with ID '{coach_id}' does not exist.")
            
            # Remove the coach
            del self._coach[coach_id]
            print(f"Coach with ID '{coach_id}' removed successfully!")
        
        except KeyError as ke:
            print(f"KeyError: {ke}")
        except Exception as e:
            print(f"An unexpected error occurred while removing the coach: {e}")

    def available_tickets(self) -> int:         #returns all available tickets in the train
        total_tickets = sum(coach.available_seats for coach in self._coach.values())
        print(f"Total available tickets: {total_tickets}")
        return total_tickets

    def available_tickets_by_coach(self) -> Tuple[str,int]:        #returns available tickets by coach
        available_ticket_by_coach = [(coach.coach_id, coach.available_seats) for coach in self._coach.values()]
        print(f"Available tickets by coach: {available_ticket_by_coach}")
        return available_ticket_by_coach

    def total_tickets(self) -> int:         #returns total tickets in the train
        total_tickets = sum(coach.total_seats for coach in self._coach.values())
        print(f"Total tickets: {total_tickets}")
        return total_tickets

