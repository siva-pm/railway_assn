from models.ticket import TrainTicket
from services.booking_service import book_seat, cancel_booking
from .admin import Admin
from typing import Optional
class Users:    # """Class to represent individual user details."""
   
    def __init__(self, user_id: str, name: str, contact: str):
        self._user_id = user_id
        self._name = name
        self._contact = contact
        self._ticket_list: list[TrainTicket] = []  # Stores tickets for the user

    def __str__(self) -> str:   # """String representation of the Users class."""
       
        return f"User ID: {self.user_id}\nName: {self.name}\nContact: {self.contact}"

    def add_ticket(self, new_ticket: TrainTicket) -> None:  # """Adds a ticket to the user's ticket list."""
        self._ticket_list.append(new_ticket)
        print(f"Ticket with PNR {new_ticket.pnr} added to user {self.name}'s ticket list.")

    def remove_ticket(self, seat_number:int, coach_id:str, train_id:str) -> None: # """Removes a ticket from the user's ticket list."""
        for ticket in self._ticket_list:
            if ticket.seat_number == seat_number and ticket.coach_id == coach_id and ticket.train_id == train_id:
                self._ticket_list.remove(ticket)
                print(f"Ticket with PNR {ticket.pnr} removed from user {self.name}'s ticket list.")
                return
        print(f"No ticket found for user {self.name} with seat number {seat_number} in coach {coach_id}.")

    def display_tickets(self) -> None:  # """Displays all tickets for the user."""
        if not self._ticket_list:
            print(f"No tickets found for user {self.name}.")
        else:
            print(f"Tickets for {self.name}:")
            for ticket in self._ticket_list:
                print(f"PNR: {ticket.pnr}, Train: {ticket.train_name}, Seat: {ticket.seat_number}")

    def update_profile(self) -> bool:  # """Updates a user's profile contact."""
        new_contact = input("Enter new contact number: ")
        self._contact = new_contact

class UserManagement:   # """Class to manage user registration and login."""
    
    def __init__(self):
        self.users: dict[str, Users] = {}  # Stores all registered users

    def __str__(self) -> str:  # """String representation of the UserManagement class."""
        if not self.users:
            return "No users registered in the system."
        users_str = "\n".join(f"User ID: {user.user_id}, Name: {user.name}" for user in self.users.values())
        return f"Registered Users:\n{users_str}"

    def register_user(self) -> bool: # """Registers a new user."""
        user_id = input("Enter User ID: ")
        name = input("Enter Name: ")
        contact = input("Enter Contact: ") 
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

def user_cli(admin: Admin,user_management: UserManagement): # """User command-line interface."""
    logged_in_user:Optional[Users] = None

    while True:
        if not logged_in_user:
            print("\nUser Management Menu")
            print("1. Register User")
            print("2. Login User")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                user_management.register_user()

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
                booking_result = book_seat(train_id,admin,logged_in_user)
                if booking_result:
                    ticket=booking_result
                    print(f"Booking successful! seat number is {ticket.seat_number} in coach {ticket.coach_id}")
                else:
                    print("Booking failed. Please try again.")

            elif choice == "2":
                cancel_status = cancel_booking(train_id,admin,logged_in_user)
                if cancel_status:
                    print("Cancellation successful.")
                else:
                    print("Cancellation failed. Please try again.")

            elif choice == "3":
                train_id = input("Enter Train ID: ")
                my_train = admin.get_train(train_id)
                print("\nTrain Schedule:")
                my_train.display_schedule()

            elif choice == "4":
                print("\nUser Tickets:")
                logged_in_user.display_tickets()

            elif choice == "5":
                print("\nTrain List:")
                admin.list_trains()

            elif choice == "6":
                logged_in_user.update_profile()

            elif choice == "7":
                print("Logging out...")
                logged_in_user = None

            else:
                print("Invalid option. Please try again.")
