import os
from models.ticket import TrainTicket
from services.booking_service import book_seat, cancel_booking
from .admin import Admin
from typing import Optional
from time import sleep
import uuid

class Users:
    def __init__(self, user_id: str, name: str, contact: str):
        self._user_id = user_id
        self._name = name
        self._contact = contact
        self._ticket_list: list[TrainTicket] = []

    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def contact(self) -> str:
        return self._contact
    
    def __str__(self) -> str:
        return f"User ID: {self.user_id}\nName: {self.name}\nContact: {self.contact}"

    def add_ticket(self, passenger_name:str, train_id:str, coach_id:str, seat_number:int) -> bool:
        try:
            unique_int = int(uuid.uuid4().int % (10**18))
            ticket=TrainTicket(pnr_id=unique_int, passenger_name=passenger_name,train_number=train_id,coach_number=coach_id,seat_number=str(seat_number),journey_date="2022-12-31",booking_status="Booked")
            self._ticket_list.append(ticket)
            print(f"Ticket with PNR {ticket.PNR_id} added to user {self.name}'s ticket list.")
            return True
        except Exception as e:
            print(f"Error while adding ticket: {e}")
            return False
        
    def remove_ticket(self, seat_number:int, coach_id:str, train_id:str) -> bool:
        try:
            for ticket in self._ticket_list:
                if (str(ticket.seat_number) == str(seat_number)): 
                    if (ticket.coach_number.upper() == coach_id.upper()):
                        if (ticket.train_number.upper() == train_id.upper()):
                            self._ticket_list.remove(ticket)
                            print(f"Ticket with PNR {ticket.PNR_id} removed from user {self.name}'s ticket list.")
                            return True
                        else:
                            print(f"No ticket found, train number mismatch")
                    else:
                        print(f"No ticket found, coach number mismatch")
                else:
                    print(f"No ticket found, seat number mismatch")

            print(f"No ticket found for user {self.name} with seat number {seat_number} in coach {coach_id}.")
            return False
        except Exception as e:
            print(f"Error while removing ticket: {e}")
            return False

    def display_tickets(self) -> bool:
        try:
            if not self._ticket_list:
                print(f"No tickets found for user {self.name}.")
                return False
            else:
                print(f"Tickets for {self.name}:")
                for ticket in self._ticket_list:
                    print(f"PNR: {ticket.PNR_id}, Train: {ticket.train_number}, Seat: {ticket.seat_number}, Coach: {ticket.coach_number}")
                return True
        except Exception as e:
            print(f"Error while displaying tickets: {e}")
            return False

    def update_profile(self) -> bool:
        while True:
            try:
                new_contact = input("Enter new contact number: ").strip()
                if not new_contact.isdigit() or len(new_contact)!=10:
                    continue
                self._contact = new_contact
                return True
            except Exception as e:
                print(f"Error updating profile: {e}")
                return False
                
class UserManagement:
    def __init__(self):
        self.users: dict[str, Users] = {}

    def __str__(self) -> str:
        try:
            if not self.users:
                return "No users registered in the system."
            users_str = "\n".join(f"Name: {user.name}" for user in self.users.values())
            return f"Registered Users:\n{users_str}"
        except Exception as e:
            return f"Error displaying users: {e}"

    def register_user(self) -> bool:
        try:
            user_id = input("Enter User ID: ").strip()
            if not user_id:
                raise ValueError("User ID cannot be empty.")
            if user_id in self.users:
                raise ValueError(f"User ID '{user_id}' already exists. Please choose a different ID.")

            name = input("Enter Name: ").strip()
            if not name:
                raise ValueError("Name cannot be empty.")

            contact = input("Enter Contact: ").strip()
            if not contact.isdigit() or len(contact) != 10:
                raise ValueError("Contact number must be a valid 10-digit number.")

            self.users[user_id] = Users(user_id, name, contact)
            print(f"User '{name}' registered successfully!")
            return True  

        except ValueError as ve:
            print(ve)  
            return False  
        except Exception as e:
            print(f"Error registering user: {e}")
            return False 

    def login(self) -> Optional[Users]:
        try:
            while True:
                user_id = input("Enter User ID: ")
                if not user_id:
                    print("User ID cannot be empty. Please try again.")
                    continue
                break

            if user_id in self.users:
                print(f"User {self.users[user_id].name} logged in successfully!")
                return self.users[user_id]
            
            print("Invalid user ID!")
            return None
        except Exception as e:
            print(f"Error logging in: {e}")
            return None


def user_cli(admin: Admin, user_management: UserManagement):
    logged_in_user: Optional[Users] = None
    
    while True:
        os.system("clear")
        try:
            if not logged_in_user:
                print("\nUser Management Menu")
                print("1. Register User")
                print("2. Login User")
                print("3. List users")
                print("4. Exit")

                choice = input("Enter your choice: ")
                
                if choice == "1":
                    user_management.register_user()
                
                elif choice == "2":
                    logged_in_user=user_management.login()
                
                elif choice == "3":
                    print(user_management)
                
                elif choice == "4":
                    print("Exiting the application. Goodbye!")
                    break
                
                else:
                    print("Invalid option. Please try again.")
                
                # input("Press Enter to continue...")
            
            else:
                print("\nUser Menu")
                print("1. Book a Ticket")
                print("2. Cancel a Ticket")
                print("3. Display Tickets")
                print("4. View Train Schedule")
                print("5. View Train List")
                print("6. Logout")

                choice = input("Enter your choice: ")
                
                if choice == "1":
                    book_status = book_seat(admin, logged_in_user)
                    if book_status:
                        print(f"Booking successful!!")
                    else:
                        print("Booking failed. Please try again.")
                    
                elif choice == "2":
                    cancel_status = cancel_booking(admin, logged_in_user)
                    if cancel_status:
                        print("Cancellation successful.")
                    else:
                        print("Cancellation failed. Please try again.")
               
                elif choice == "3":
                    logged_in_user.display_tickets()
                
                elif choice == "4":
                    admin.get_train().display_schedule()
                
                elif choice == "5":
                    admin.list_trains()
                
                elif choice == "6":
                    print("Logging out...")
                    logged_in_user = None
               
                else:
                    print("Invalid option. Please try again.")  

            input("Press enter to continue...")

        except Exception as e:
            print(f"Unexpected error: {e}")
