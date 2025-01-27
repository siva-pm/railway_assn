class Passenger:
    def __init__(self, name: str, age: int, gender: str, contact: str):
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

