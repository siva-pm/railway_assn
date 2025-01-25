class Passenger:
    def __init__(self, pnr_id: int, name: str, age: int, gender: str, contact: str):
        self.PNR_id = pnr_id
        self.name = name
        self.age = age
        self.gender = gender
        self.contact = contact

    def __str__(self):
        return (
        f"Passenger ID: {self.PNR_id}\n"
        f"Name: {self.name}\n"
        f"Age: {self.age}\n"
        f"Gender: {self.gender}\n"
        f"Contact: {self.contact}"
        )

    def add_passenger(self):
        # Get user input for passenger details
        try:
            pnr_id = int(input("Enter Passenger PNR ID: "))
            name = input("Enter Passenger Name: ")
            age = int(input("Enter Age: "))
            gender = input("Enter Gender (Male/Female): ")
            contact = input("Enter Contact Number: ")
        except ValueError:
            print("Invalid input. Please enter correct details.")
            return
