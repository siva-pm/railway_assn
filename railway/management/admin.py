import time
import os
from typing import TypeVar, Generic, Dict
from models.train import Train

T = TypeVar('T', bound=Train)

class Admin(Generic[T]):
    def __init__(self):
        self._trains: Dict[str, T] = {}

    def get_train(self) -> T:
        while True:
            try:
                train_id = input("Enter Train ID: ").strip().upper()
                if not train_id:
                    raise ValueError("Train ID cannot be empty.")
                if train_id not in self._trains:
                    raise KeyError(f"Train with ID '{train_id}' not found.")
                return self._trains[train_id]
            except Exception as e:
                print(f"Error while getting train: {e}")
                return None

    def add_train(self) -> bool:
        while True:
            try:
                train_id = input("Enter Train ID: ").strip().upper()
                if not train_id:
                    raise ValueError("Train ID cannot be empty.")
                if train_id in self._trains:
                    print(f"Train with ID '{train_id}' already exists.")
                    return False

                name = input("Enter Train Name: ").strip()
                if not name:
                    raise ValueError("Train name cannot be empty.")

                route_start = input("Enter Route Start: ").strip()
                route_end = input("Enter Route End: ").strip()
                if not route_start or not route_end:
                    raise ValueError("Route start and end cannot be empty.")

                train = Train(train_id=train_id, name=name, route=(route_start, route_end))
                self._trains[train_id] = train
                print(f"Train '{train.train_name}' with ID '{train.train_id}' added successfully.")
                return True

            except ValueError as ve:
                print(f"Error: {ve}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    def remove_train(self) -> bool:
        try:
            train_id = input("Enter Train ID: ").strip().upper()
            if not train_id:
                raise ValueError("Train ID cannot be empty.")

            if train_id not in self._trains:
                raise KeyError(f"Train with ID '{train_id}' does not exist.")

            train = self._trains[train_id]
            if train.available_tickets() < train.total_tickets():
                choice = input("Warning! Some tickets are booked. Do you still want to remove the train? (y/n): ").strip().lower()
                if choice != 'y':
                    print("Operation cancelled.")
                    return False

            del self._trains[train_id]
            print(f"Train with ID '{train_id}' removed successfully.")
            return True

        except KeyError as ke:
            print(f"Error: {ke}")
        except ValueError as ve:
            print(f"Error: {ve}")  
        except Exception as e:
            print(f"Unexpected error: {e}")
        return False
        

    def list_trains(self) -> bool:
        try:
            if not self._trains:
                print("No trains available.")
                return False
            
            print("List of all trains:")
            for train_id, train in self._trains.items():
                try:
                    route_start, route_end = train._route
                    print(f" Train ID: {train.train_id}, Name: {train.train_name}, Route: {route_start} -> {route_end}")
                except AttributeError as e:
                    print(f"Error retrieving route for train ID {train_id}: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred for train ID {train_id}: {e}")
            return True
        except Exception as e:
            print(f"An error occurred while listing trains: {e}")
        return False

def admin_cli(admin: Admin[Train]) -> None:
    try:
        password = input("Enter Admin Password: ").strip()
        if password != "admin":
            print("Incorrect password.")
            time.sleep(0.5)
            return

        while True:
            os.system("clear")
            print("\nAdmin Management Menu")
            print("1. Add Train")
            print("2. Remove Train")
            print("3. List Trains")
            print("4. View Train Details")
            print("5. Update Train Schedule")
            print("6. Display Train Schedule")
            print("7. Add Coach")
            print("8. Remove Coach")
            print("9. View Coach Details")
            print("10. View Available Tickets")
            print("11. View Passengers Details")
            print("12. Exit")

            choice = input("\nEnter your choice: ").strip()
            if not choice.isdigit():
                print("Invalid input! Please enter a number.")
                continue

            if choice == "1":
                admin.add_train()

            elif choice == "2":
                admin.remove_train()

            elif choice == "3":
                admin.list_trains()

            elif choice == "4":
                print(admin.get_train())

            elif choice == "5":
                admin.get_train().update_schedule()

            elif choice == "6":
               admin.get_train().display_schedule()

            elif choice == "7":
                admin.get_train().add_coach()

            elif choice == "8":
                admin.get_train().remove_coach()

            elif choice == "9":
                admin.get_train().display_coaches()

            elif choice == "10":
                try:
                    train = admin.get_train()
                    for coach_id, available_seats in train.available_tickets_by_coach():
                        print(f"Coach ID: {coach_id}, Available Seats: {available_seats}")
                except Exception as e:
                    print(f"Error at showing available seats: {e}")

            elif choice == "11":
                admin.get_train().get_passenger_list()
               
            elif choice == "12":
                print("Exiting the application. Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")

            input("Press Enter to return to the menu...")

    except Exception as e:
        print(f"Unexpected error: {e}")
