from typing import Dict, TypeVar, Generic, Tuple
from .coach import Coach

C = TypeVar('C', bound=Coach)

class Train(Generic[C]):
    def __init__(self, train_id: str, name: str, route: tuple[str, str]):
        self._train_id = train_id
        self._train_name = name
        self._route = route
        self._schedule: Dict[str, Tuple[str, str]] = {}  # Station-wise schedule
        self._coach: Dict[str, C] = {}  # dictionary of coach objects with key as coach number

    @property
    def train_id(self) -> str:
        return self._train_id
    @property
    def train_name(self) -> str:
        return self._train_name

    def __str__(self):
        return (
            f"Train ID: {self._train_id}\n"
            f"Name: {self._train_name}\n"
            f"Route: {self._route[0]} -> {self._route[1]}\n"
            f"Number of Coaches: {len(self._coach)}\n"
            f"Total Passengers: {len(self.get_passenger_list())}"
        )

    def display_schedule(self) -> bool:  # prints station, arrival time and departure time
        if not self._schedule:
            print("No schedule available.")
            return False
        try:
            for station, timings in self._schedule.items():
                if len(timings) == 2:
                    print(f"station:{station}    arrival:{timings[0]}    departure:{timings[1]}")
                else:
                    print(f"Incomplete schedule for station {station}.")
                    return False
            return True
        except Exception as e:
            print(f"display schedule error: {e}")
        return False

    def update_schedule(self) -> bool:  # updates the existing schedule
        try:
            station = input("Enter Station Name: ").strip().upper()
            arrival = input("Enter Arrival Time: ").strip().upper()
            departure = input("Enter Departure Time: ").strip().upper()
            if not station or not arrival or not departure:
                raise ValueError("All fields (station, arrival, and departure) must be filled.")
            if station in self._schedule:
                raise ValueError(f"Station '{station}' already exists.")
            new_schedule: Dict[str, Tuple[str, str]] = {station: (arrival, departure)}            
            self._schedule.update(new_schedule)
            print("Schedule updated successfully!")
            return True
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"An error occurred while updating the schedule: {e}")
        return False
    
    def get_passenger_list(self) -> Dict[int, str]:  # return a dict, key= pnr id, value= passenger name
        try:
            passenger_info = {}
            for coach_id, coach in self._coach.items():
                for seat_no, passenger in coach._seat.items():
                    if passenger is not None:
                        passenger_info[coach_id] = passenger.name

            if not passenger_info:
                print("No Passengers in this train")
            else:
                for pnr_id, passenger_name in passenger_info.items():
                    print(f"PNR ID: {pnr_id}, Passenger Name: {passenger_name}")
                
            return passenger_info
        
        except AttributeError as e:
            print(f"Attribute error while fetching passenger list: {e}")
            return {}
        except Exception as e:
            print(f"Error fetching passenger list: {e}")
            return {}
    
    def add_coach(self) -> bool:  # adds new coach in existing coach dict
        try:
            coach_id = input("Enter Coach ID: ").upper().strip()
            if not coach_id:
                raise ValueError(f"Coach ID cannot be empty!!!")
            if coach_id in self._coach:
                raise ValueError(f"Coach with ID '{coach_id}' already exists.")
            
            total_seats = int(input("Enter Total Seats: ").strip())
            if not total_seats:
                raise ValueError(f"Totals seats cannot be empty!!!")
            
            coach_type = input("Enter Coach Type: ").upper().strip()
            if not coach_type:
                raise ValueError(f"Coach type cannot be empty!!!")
            
            new_coach: Dict[str, Coach] = {coach_id: Coach(coach_id=coach_id, total_seats=total_seats, coach_type=coach_type)}
            self._coach.update(new_coach)
            print(f"Coach with ID '{coach_id}' added successfully!")
            return True
        
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred while adding the coach: {e}")
        return False
        
    def remove_coach(self) -> bool:  # removes an existing coach entry
        try: 
            coach_id = input("Enter Coach ID to remove: ").strip().upper()
            if not coach_id:
                raise ValueError("Coach ID cannot be empty.")
            if coach_id not in self._coach:
                raise KeyError(f"Coach with ID '{coach_id}' does not exist.")
            del self._coach[coach_id]
            print(f"Coach with ID '{coach_id}' removed successfully!")
            return True
        
        except KeyError as ke:
            print(f"KeyError: {ke}")
        except Exception as e:
            print(f"An unexpected error occurred while removing the coach: {e}")
        return False

    def available_tickets(self) -> int:  # returns count of available tickets in the train
        try:
            total_tickets = sum(coach.available_seats for coach in self._coach.values())
            print(f"Total available tickets: {total_tickets}")
            return total_tickets
        except AttributeError as e:
            print(f"Error accessing available seats: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while calculating available tickets: {e}")
        return 0    

    def available_tickets_by_coach(self) -> list[Tuple[str, int]]:  # returns available tickets by coach
        try:
            available_ticket_by_coach = [(coach.coach_id, coach.available_seats) for coach in self._coach.values()]
            return available_ticket_by_coach
        except AttributeError as e:
            print(f"Error accessing coach attributes: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while fetching available tickets by coach: {e}")
        return [] 

    def total_tickets(self) -> int:  # returns total tickets in the train
        try:
            total_tickets = sum(coach.total_seats for coach in self._coach.values())
            print(f"Total tickets: {total_tickets}")
            return total_tickets
        except AttributeError as e:
            print(f"Error accessing total seats: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while calculating total tickets: {e}")
        return 0  

    def display_coaches(self) -> bool:  # displays all coaches
        try:
            if not self._coach:
                print("No coaches available.")
                return False
            
            print("List of all coaches:")
            for coach_id, coach in self._coach.items():
                try:
                    print(f"{coach_id} - {coach.coach_type}, Total Seats: {coach.total_seats}")
                except AttributeError as e:
                    print(f"Error accessing attributes for coach ID {coach_id}: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred for coach ID {coach_id}: {e}")
            
            return True
        
        except Exception as e:
            print(f"An error occurred while displaying coaches: {e}")
        return False
