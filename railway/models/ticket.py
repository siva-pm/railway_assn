class TrainTicket:
    def __init__(self, pnr_id: int, passenger_name: str, train_number: str, coach_number: str,
                 seat_number: int, journey_date: str, booking_status: str = "Booked"):
        self.PNR_id = pnr_id
        self.passenger_name = passenger_name
        self.train_number = train_number
        self.coach_number = coach_number
        self.seat_number = seat_number
        self.journey_date = journey_date
        self.booking_status = booking_status

    def __str__(self):
        return (f"PNR ID: {self.PNR_id}, Passenger: {self.passenger_name}, "
                f"Train: {self.train_number}, Seat: {self.coach_number} {self.seat_number}, "
                f"Date: {self.journey_date}, Status: {self.booking_status}")
