from typing import List, Dict,TypeVar,Generic
from .coach import Coach

C = TypeVar('C', bound=Coach)

class Train(Generic[C]):
    def __init__(self, train_id: str, name: str, route: tuple[str,str], coach: Dict[str,Coach]):
        self._train_id = train_id
        self._train_name = name
        self._route = route
        self._schedule: Dict[str, List[str]]= {}  # Station-wise schedule
        self._coach = coach  # dictionary of coach objects with key as coach number

    def __str__(self):
        return (
            f"Train ID: {self._train_id}\n"
            f"Name: {self._name}\n"
            f"Route: {self._route[0]} -> {self._route[1]}\n"
            f"Number of Coaches: {len(self._coach)}\n"
            f"Total Passengers: {len(self.get_passenger_list())}"
        )

    @property
    def train_id(self) -> str:
        return self._train_id

    @property
    def name(self) -> str:
        return self._train_name

    @property
    def coach(self) -> Dict[str,C]:
        return self._coach

    @property
    def route(self) -> tuple[str,str]:
        return self._route

    def display_schedule(self):         #prints station, arrival time and departure time
        if not self._schedule:
            print("No schedule available.")
            return
        try:
            for station, timings in self._schedule.items():
                print(f"station:{station}    arrival:{timings[0]}    departure:{timings[1]}")
        except Exception as e:
            print(f"display schedule error{e}")

    def update_schedule(self, new_schedule: Dict[str, List[str]]):      #updates the existing schedule
        try:
            # Check if the input schedule is a dictionary and if each station has a list of two items (arrival and departure times)
            if not isinstance(new_schedule, dict):
                raise ValueError("The schedule must be a dictionary.")
            
            for station, timings in new_schedule.items():
                # Ensure each station has a valid timing list (a list of two items: arrival and departure time)
                if not isinstance(timings, list) or len(timings) != 2:
                    raise ValueError(f"Timings for station {station} should be a list with two items (arrival and departure).")
                
                # If everything checks out, update the schedule
                self._schedule[station] = timings
            
            print("Schedule updated successfully!")
        
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"An error occurred while updating the schedule: {e}")
           
    def get_passenger_list(self) -> Dict[int,str]:      # return a dict, key= pnr id, value= passenger name
        passenger_info={}

        for coach_id, coach in self._coach.tems():
            for seat_no, passenger in coach._seat.items():
                if passenger is not None:
                    passenger_info.append({
                        "passenger_id": passenger.PNR_id,
                        "name": passenger.name
                        })
        
        return passenger_info
         
    def add_coach(self, new_coach: Dict[str, C]):       #appends a new coach in existing coach dict
        try:
            # Check if new_coach is a dictionary
            if not isinstance(new_coach, dict):
                raise ValueError("The new coach data must be provided as a dictionary.")

            # Check for duplicate keys
            duplicate_coaches = set(new_coach.keys()) & set(self._coach.keys())
            if duplicate_coaches:
                raise ValueError(f"Duplicate coach IDs detected: {duplicate_coaches}. Each coach must have a unique ID.")

            # Add new coaches to the existing dictionary
            self._coach.update(new_coach)
            print("Coaches added successfully!")
        
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred while adding coaches: {e}")

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
