from models.ticket import TrainTicket

class Users:
    """Class to represent individual user details."""
    def __init__(self, user_id: str, name: str, contact: str):
        self.user_id = user_id
        self.name = name
        self.contact = contact
        self.ticket_list: list[TrainTicket] = []  # Stores tickets for the user

    def __str__(self) -> str:
        """String representation of a user."""
        return f"User ID: {self.user_id}\nName: {self.name}\nContact: {self.contact}"

    def add_ticket(self, new_ticket: TrainTicket) -> None:
        """Adds a new ticket to the user's ticket list."""
        self.ticket_list.append(new_ticket)
        print(f"Ticket with PNR {new_ticket.pnr} added to user {self.name}'s ticket list.")

    def display_tickets(self) -> None:
        """Displays all tickets booked by the user."""
        if not self.ticket_list:
            print(f"No tickets found for user {self.name}.")
        else:
            print(f"Tickets for {self.name}:")
            for ticket in self.ticket_list:
                print(f"PNR: {ticket.pnr}, Train: {ticket.train_name}, Seat: {ticket.seat_number}")


class UserManagement:
    """Class to manage user registrations, logins, and ticket updates."""
    def __init__(self):
        self.users: dict[str, Users] = {}  # Stores all registered users

    def __str__(self) -> str:
        """String representation of the user management system (user_id and name only)."""
        if not self.users:
            return "No users registered in the system."
        users_str = "\n".join(f"User ID: {user.user_id}, Name: {user.name}" for user in self.users.values())
        return f"Registered Users:\n{users_str}"

    def register_user(self, user_id: str, name: str, contact: str) -> bool:
        """Registers a new user."""
        if user_id in self.users:
            print(f"User {user_id} already exists.")
            return False
        self.users[user_id] = Users(user_id, name, contact)
        print(f"User {name} registered successfully!")
        return True

    def login(self, user_id: str) -> bool:
        """Logs in a user."""
        if user_id in self.users:
            print(f"User {self.users[user_id].name} logged in successfully!")
            return True
        print("Invalid user ID!")
        return False

    def update_profile(self, user_id: str, contact: str) -> bool:
        """Updates a user's profile contact."""
        if user_id in self.users:
            self.users[user_id].contact = contact
            print(f"User {self.users[user_id].name}'s profile updated successfully.")
            return True
        print("User not found!")
        return False

