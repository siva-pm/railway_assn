from models.train import Train
from models.coach import Coach
from services.booking_service import book_seat, cancel_booking
from storage.data_storage import DataStorage
from typing import Dict

# Initialize shared data storage
data_storage = DataStorage()

# Example train and coaches (static initialization for demonstration)
coach_a = Coach(coach_id="A1", total_seats=72, coach_type="Sleeper")
coach_b = Coach(coach_id="B1", total_seats=48, coach_type="AC")
coaches: Dict[str, Coach] = {"A1": coach_a, "B1": coach_b}

train = Train(train_id="12345", name="Express", route=("CityA", "CityB"), coach=coaches)


def main():
    print("Welcome to the Railway Booking System!")

    while True:
        print("\nMain Menu")
        print("1. Book a Ticket")
        print("2. Cancel a Ticket")
        print("3. View Train Schedule")
        print("4. Add Train Schedule")
        print("5. Available Tickets")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            booking_result = book_seat(train)
            if booking_result:
                seat_number, coach_id = booking_result
                print(f"Booking successful! Seat {seat_number} in Coach {coach_id}")
            else:
                print("Booking failed. Please try again.")

        elif choice == "2":
            try:
                coach_id = input("Enter Coach ID: ")
                seat_number = int(input("Enter Seat Number: "))
                cancel_status = cancel_booking(seat_number, coach_id, train)
                if cancel_status:
                    print("Cancellation successful.")
                else:
                    print("Cancellation failed. Please try again.")
            except ValueError:
                print("Invalid input. Please enter correct details.")

        elif choice == "3":
            print("\nTrain Schedule:")
            train.display_schedule()

        elif choice == "4":
            try:
                print("\nAdd Train Schedule")
                station = input("Enter Station Name: ")
                arrival = input("Enter Arrival Time: ")
                departure = input("Enter Departure Time: ")
                train.update_schedule({station: [arrival, departure]})
            except Exception as e:
                print(f"Error while adding schedule: {e}")

        elif choice == "5":
            train.available_tickets()

        elif choice == "6":
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
