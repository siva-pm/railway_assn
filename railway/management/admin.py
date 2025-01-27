from typing import TypeVar,Generic,Dict
from models.train import Train
from models.coach import Coach

T = TypeVar('T', bound=Train)

class Admin(Generic[T]):
    def __init__(self):
        self._trains: Dict[str, T] = {}
    
    @property
    def get_train(self,train_id:str) -> T:
        return self._trains[train_id]

    def add_train(self, train: T) -> None:
        """Adds a train to the system."""
        try:
            # Ensure the train ID is unique
            if train.train_id in self._trains:
                raise ValueError(f"Train with ID '{train.train_id}' already exists.")
            
            # Add the train to the dictionary
            self._trains[train.train_id] = train
            print(f"Train '{train.name}' with ID '{train.train_id}' added successfully.")
        
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred while adding the train: {e}")

    def remove_train(self, train_id: str) -> None:
        """Removes a train from the system."""
        try:
            # Ensure the train exists in the system
            if train_id not in self._trains:
                raise KeyError(f"Train with ID '{train_id}' does not exist.")
            
            # Remove the train
            del self._trains[train_id]
            print(f"Train with ID '{train_id}' removed successfully.")
        
        except KeyError as ke:
            print(f"KeyError: {ke}")
        except Exception as e:
            print(f"An unexpected error occurred while removing the train: {e}")

    def list_trains(self) -> None:
        """Displays all trains in the system."""
        if not self._trains:
            print("No trains available.")
        else:
            print("List of all trains:")
            for train_id, train in self._trains.items():
                print(f"Train ID: {train.train_id}, Train Name: {train.name}, Route: {train.route[0]} -> {train.route[1]}")

def admin_cli(admin: Admin[Train]):
    while True:
        print("\nAdmin Management Menu")
        print("1. Add Train")
        print("2. Remove Train")
        print("3. List Trains")
        print("4. View Train Details")
        print("5. Update Train Schedule")
        print("6. Display Train Schedule")
        print("7. Add Coach")
        print("8. Remove Coach")
        print("9. View Available Tickets")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            train_id = input("Enter Train ID: ")
            name = input("Enter Train Name: ")
            route_start = input("Enter Route Start: ")
            route_end = input("Enter Route End: ")
            train = Train(train_id=train_id, name=name, route=(route_start, route_end), coach={})
            admin.add_train(train)

        elif choice == "2":
            train_id = input("Enter Train ID to remove: ")
            admin.remove_train(train_id)

        elif choice == "3":
            admin.list_trains()

        elif choice == "4":
            train_id = input("Enter Train ID: ")
            if train_id in admin._trains:
                print(admin._trains[train_id])
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "5":
            train_id = input("Enter Train ID: ")
            if train_id in admin._trains:
                station = input("Enter Station Name: ")
                arrival = input("Enter Arrival Time: ")
                departure = input("Enter Departure Time: ")
                admin._trains[train_id].update_schedule({station: [arrival, departure]})
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "6":
            train_id = input("Enter Train ID: ")
            if train_id in admin._trains:
                admin._trains[train_id].display_schedule()
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "7":
            train_id = input("Enter Train ID: ")
            if train_id in admin._trains:
                coach_id = input("Enter Coach ID: ")
                total_seats = int(input("Enter Total Seats: "))
                coach_type = input("Enter Coach Type: ")
                new_coach = {coach_id: Coach(coach_id=coach_id, total_seats=total_seats, coach_type=coach_type)}
                admin._trains[train_id].add_coach(new_coach)
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "8":
            train_id = input("Enter Train ID: ")
            if train_id in admin._trains:
                coach_id = input("Enter Coach ID to remove: ")
                admin._trains[train_id].remove_coach(coach_id)
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "9":
            train_id = input("Enter Train ID: ")
            if train_id in admin._trains:
                admin._trains[train_id].available_tickets()
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "10":
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

def main():
    admin = Admin[Train]()
    admin_cli(admin)

if __name__ == "__main__":
    main()