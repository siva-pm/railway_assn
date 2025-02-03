from abc import ABC, abstractmethod
class Ticket_model(ABC):
    @property
    @abstractmethod
    def PNR_id(self):
        pass

    @property
    @abstractmethod
    def passenger_name(self):
        pass

    @property
    @abstractmethod
    def train_number(self):
        pass

    @property
    @abstractmethod
    def journey_date(self):
        pass

    @property
    @abstractmethod
    def booking_status(self):
        pass

class TrainTicket(Ticket_model):
    def __init__(self, pnr_id: int, passenger_name: str, train_number: str, coach_number: str,
                 seat_number: str, journey_date: str, booking_status: str):
        self._PNR_id = pnr_id
        self._passenger_name = passenger_name
        self._train_number = train_number
        self.coach_number = coach_number
        self.seat_number = seat_number
        self._journey_date = journey_date
        self._booking_status = booking_status

    @property
    def PNR_id(self):
        return self._pnr_id

    @property
    def passenger_name(self):
        return self._passenger_name

    @property
    def train_number(self):
        return self._train_number

    @property
    def journey_date(self):
        return self._journey_date

    @property
    def booking_status(self):
        return self._booking_status

    def __str__(self):
        return (f"PNR ID: {self.PNR_id}, Passenger: {self.passenger_name}, "
                f"Train: {self.train_number}, Seat: {self.coach_number} {self.seat_number}, "
                f"Date: {self.journey_date}, Status: {self.booking_status}")

class WL_Ticket(Ticket_model):  #NOT YET IMPLEMENTED
    def __init__(self, pnr_id: int, passenger_name: str, train_number: str,journey_date: str, booking_status: str = "PQWL"):
        self._PNR_id = pnr_id
        self._passenger_name = passenger_name
        self._train_number = train_number
        self._journey_date = journey_date
        self._booking_status = booking_status

    @property
    def PNR_id(self):
        return self._pnr_id

    @property
    def passenger_name(self):
        return self._passenger_name

    @property
    def train_number(self):
        return self._train_number

    @property
    def journey_date(self):
        return self._journey_date

    @property
    def booking_status(self):
        return self._booking_status
    
    def __str__(self):
        return (f"PNR ID: {self.PNR_id}, Passenger: {self.passenger_name}, "
                f"Train: {self.train_number}"
                f"Date: {self.journey_date}, Status: {self.booking_status}")
