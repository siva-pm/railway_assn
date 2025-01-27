from typing import TypeVar,Generic,Dict
from models.train import Train

T = TypeVar('T', bound=Train)
class Admin(Generic[T]):
    def __init__(self):
        self._trains: Dict[str, T] = {}
    
    @property
    def get_train(self,train_id:str) -> T:
        return self._trains[train_id]

    def add_train(self) -> None:    #adds a new train
        
        try:
            train_id = input("Enter Train ID: ")
            if train_id in self._trains:
                raise ValueError(f"Train with ID '{train_id}' already exists.")
            name = input("Enter Train Name: ")
            route_start = input("Enter Route Start: ")
            route_end = input("Enter Route End: ")
            train = Train(train_id=train_id, name=name, route=(route_start, route_end), coach={})
            
            # Add the train to the dictionary
            self._trains[train.train_id] = train
            print(f"Train '{train.name}' with ID '{train.train_id}' added successfully.")
        
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred while adding the train: {e}")

    def remove_train(self, train_id: str) -> None:  #removes a train
        try:
            # Ensure the train exists in the system
            if train_id not in self._trains:
                raise KeyError(f"Train with ID '{train_id}' does not exist.")
            
            if self._trains[train_id].available_tickets() < self._trains[train_id].total_tickets:
                choice=input("Warning! Some tickets have been booked. Do you still want to remove the train? (y/n): ")
                if choice.lower() != 'y':
                    del self._trains[train_id]
                    print(f"Train with ID '{train_id}' removed successfully.")
                else:
                    print("Operation cancelled.")
        
        except KeyError as ke:
            print(f"KeyError: {ke}")
        except Exception as e:
            print(f"An unexpected error occurred while removing the train: {e}")

    def list_trains(self) -> None:  #lists all trains
        if not self._trains:
            print("No trains available.")
        else:
            print("List of all trains:")
            for train_id, train in self._trains.items():
                print(f"Train ID: {train.train_id}, Train Name: {train.name}, Route: {train.route[0]} -> {train.route[1]}")

def admin_cli(admin: Admin[Train]) -> None:  # Admin command-line interface.
    password = input("Enter Admin Password: ")
    if password != "admin":
        print("Incorrect password.")
        return
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
        print("10. View Passengers details")
        print("11. Exit")

        choice:int = input("Enter your choice: ")

        if choice == "1":
            admin.add_train()

        elif choice == "2":
            train_id = input("Enter Train ID to remove: ")
            admin.remove_train(train_id)

        elif choice == "3":
            admin.list_trains()

        elif choice == "4":
            train_id = input("Enter Train ID: ")
            my_train=admin.get_train(train_id)
            if my_train:
                print(my_train)
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "5":
            train_id = input("Enter Train ID: ")
            my_train=admin.get_train(train_id)
            if my_train:
                my_train.update_schedule()
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "6":
            train_id = input("Enter Train ID: ")
            my_train=admin.get_train(train_id)
            if my_train:
                my_train.display_schedule()
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "7":
            train_id = input("Enter Train ID: ")
            my_train=admin.get_train(train_id)
            if my_train:
                my_train.add_coach()
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "8":
            train_id = input("Enter Train ID: ")
            my_train=admin.get_train(train_id)
            if my_train:
                coach_id = input("Enter Coach ID to remove: ")
                my_train.remove_coach(coach_id)
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "9":
            train_id = input("Enter Train ID: ")
            my_train=admin.get_train(train_id)
            if my_train:
                for coach_id, available_seats in my_train.available_tickets_by_coach():
                    print(f"Coach ID: {coach_id}, Available Seats: {available_seats}")
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "10":
            train_id = input("Enter Train ID: ")
            my_train=admin.get_train(train_id)
            if my_train:
                for pnr_id, passenger_name in my_train.get_passenger_details():
                    print(f"PNR ID: {pnr_id}, Passenger Name: {passenger_name}")
            else:
                print(f"Train with ID '{train_id}' not found.")

        elif choice == "11":
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

def main():
    admin = Admin[Train]()
    admin_cli(admin)

if __name__ == "__main__":
    main()