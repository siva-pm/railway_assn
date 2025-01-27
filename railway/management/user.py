from models.ticket import TrainTicket
from services.booking_service import book_seat, cancel_booking
from models.train import Train
from management.admin import Admin
import uuid
class Users:    # """Class to represent individual user details."""
   
    def __init__(self, user_id: str, name: str, contact: str):
        self.user_id = user_id
        self.name = name
        self.contact = contact
        self.ticket_list: list[TrainTicket] = []  # Stores tickets for the user

    def __str__(self) -> str:   # """String representation of the Users class."""
       
        return f"User ID: {self.user_id}\nName: {self.name}\nContact: {self.contact}"

    def add_ticket(self, new_ticket: TrainTicket) -> None:  # """Adds a ticket to the user's ticket list."""
        self.ticket_list.append(new_ticket)
        print(f"Ticket with PNR {new_ticket.pnr} added to user {self.name}'s ticket list.")

    def remove_ticket(self, seat_number:int, coach_id:str, train_id:str) -> None: # """Removes a ticket from the user's ticket list."""
        for ticket in self.ticket_list:
            if ticket.seat_number == seat_number and ticket.coach_id == coach_id and ticket.train_id == train_id:
                self.ticket_list.remove(ticket)
                print(f"Ticket with PNR {ticket.pnr} removed from user {self.name}'s ticket list.")
                return
        print(f"No ticket found for user {self.name} with seat number {seat_number} in coach {coach_id}.")

    def display_tickets(self) -> None:  # """Displays all tickets for the user."""
        if not self.ticket_list:
            print(f"No tickets found for user {self.name}.")
        else:
            print(f"Tickets for {self.name}:")
            for ticket in self.ticket_list:
                print(f"PNR: {ticket.pnr}, Train: {ticket.train_name}, Seat: {ticket.seat_number}")

class UserManagement:   # """Class to manage user registration and login."""
    
    def __init__(self):
        self.users: dict[str, Users] = {}  # Stores all registered users

    def __str__(self) -> str:  # """String representation of the UserManagement class."""
        if not self.users:
            return "No users registered in the system."
        users_str = "\n".join(f"User ID: {user.user_id}, Name: {user.name}" for user in self.users.values())
        return f"Registered Users:\n{users_str}"

    def register_user(self, user_id: str, name: str, contact: str) -> bool: # """Registers a new user."""
        if user_id in self.users:
            print(f"User {user_id} already exists.")
            return False
        self.users[user_id] = Users(user_id, name, contact)
        print(f"User {name} registered successfully!")
        return True

    def login(self, user_id: str) -> bool:  # """Logs in a user."""
        if user_id in self.users:
            print(f"User {self.users[user_id].name} logged in successfully!")
            return True
        print("Invalid user ID!")
        return False

    def update_profile(self, user_id: str, contact: str) -> bool:  # """Updates a user's profile contact."""
        if user_id in self.users:
            self.users[user_id].contact = contact
            print(f"User {self.users[user_id].name}'s profile updated successfully.")
            return True
        print("User not found!")
        return False

def user_cli(admin: Admin,user_management: UserManagement): # """User command-line interface."""
    logged_in_user = None

    while True:
        if not logged_in_user:
            print("\nUser Management Menu")
            print("1. Register User")
            print("2. Login User")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                user_id = input("Enter User ID: ")
                name = input("Enter Name: ")
                contact = input("Enter Contact: ")
                user_management.register_user(user_id, name, contact)

            elif choice == "2":
                user_id = input("Enter User ID: ")
                if user_management.login(user_id):
                    logged_in_user = user_management.users[user_id]

            elif choice == "3":
                print("Exiting the application. Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")
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
                train_id = input("Enter Train ID: ")
                booking_result = book_seat(train_id,admin)
                if booking_result:
                    ticket=booking_result
                    logged_in_user.add_ticket(ticket)
                    print(f"Booking successful! Seat {seat_number} in Coach {coach_id}")
                else:
                    print("Booking failed. Please try again.")

            elif choice == "2":
                try:
                    train_id = input("Enter Train ID: ")
                    coach_id = input("Enter Coach ID: ")
                    seat_number = int(input("Enter Seat Number: "))
                    cancel_status = cancel_booking(seat_number, coach_id, train_id,admin)
                    if cancel_status:
                        print("Cancellation successful.")
                        logged_in_user.remove_ticket(seat_number, coach_id, train_id)
                    else:
                        print("Cancellation failed. Please try again.")

                except ValueError:
                    print("Invalid input. Please enter correct details.")

            elif choice == "3":
                train_id = input("Enter Train ID: ")
                train = admin.get_train(train_id)
                print("\nTrain Schedule:")
                train.display_schedule()

            elif choice == "4":
                print("\nUser Tickets:")
                logged_in_user.display_tickets()

            elif choice == "5":
                print("\nTrain List:")
                admin.list_trains()

            elif choice == "6":
                print("Logging out...")
                logged_in_user = None

            else:
                print("Invalid option. Please try again.")
