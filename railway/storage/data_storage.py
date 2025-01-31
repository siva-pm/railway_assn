import json
from typing import Dict, Union
from management.user import UserManagement,Users
from management.admin import Admin
from models.train import Train
from models.ticket import TrainTicket
from models.coach import Coach
from models.passenger import Passenger
class DataStorage:
    
    def __init__(self):
        self.data: Dict[str, Dict[str, Union[Train,Users]]] = {
            "users": {},  # Stores user data
            "trains": {},  # Stores train data
        }

    def save_user_data(self, user_management: UserManagement) -> None:
        self.data["users"] = {
            user_id: {
                "user_id": user._user_id,
                "name": user._name,
                "contact": user._contact,
                "ticket_list": [
                    {
                        "pnr": ticket.PNR_id,
                        "passenger_name": ticket.passenger_name,
                        "train_number": ticket.train_number,
                        "coach_number": ticket.coach_number,
                        "seat_number": ticket.seat_number,
                        "journey_date": ticket.journey_date,
                        "booking_status": ticket.booking_status
                    } for ticket in user._ticket_list
                ] 
            }for user_id, user in user_management.users.items()
        }
        try:
            with open("user_data.json", "w") as f:
                json.dump(self.data["users"], f, indent=4)
            print("User data saved successfully.")
        except (IOError, OSError) as e:
            print(f"Error saving user data: {e}")

    def load_user_data(self) -> Dict[str, Users]:
        try:
            with open("user_data.json", "r") as f:
                users_data = json.load(f)
                self.data["users"] = {
                    user_id: Users( 
                        user_id=user["user_id"],
                        name=user["name"],
                        contact=user["contact"],
                    ) for user_id, user in users_data.items()  
                }
            for user_id, user in self.data["users"].items():
                user._ticket_list = [
                    TrainTicket(
                        pnr_id=ticket["pnr"],
                        passenger_name=ticket["passenger_name"],
                        train_number=ticket["train_number"],
                        coach_number=ticket["coach_number"],
                        seat_number=ticket["seat_number"],
                        journey_date=ticket["journey_date"],
                        booking_status=ticket["booking_status"]
                    ) for ticket in users_data[user_id]["ticket_list"]
                ]

            print("User data loaded successfully.")
        except FileNotFoundError:
            print("No previous user data found. Returning an empty dictionary.")
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Error loading user data: {e}")
        return self.data["users"]

    def save_train_data(self, admin: Admin) -> None:
        self.data["trains"] = {
            train_id: {
                "train_id": train._train_id,
                "train_name": train._train_name,
                "route": train._route,
                "schedule": train._schedule,
                "coaches": {
                    coach_id: {
                        "coach_id": coach.coach_id,
                        "total_seats": coach.total_seats,
                        "available_seats": coach.available_seats,
                        "coach_type": coach.coach_type,
                        "seats": {
                            seat_number: {
                                "name": passenger.name,
                                "age": passenger.age,
                                "gender": passenger.gender,
                                "contact": passenger.contact
                            } if passenger else None
                            for seat_number, passenger in coach._seat.items()
                        }
                    } for coach_id, coach in train._coach.items()
                }
            } for train_id, train in admin._trains.items()
        }
        try:
            with open("train_data.json", "w") as f:
                json.dump(self.data["trains"], f, indent=4)
            print("Train data saved successfully.")
        except (IOError, OSError) as e:
            print(f"Error saving train data: {e}")

    def load_train_data(self) -> Dict[str, Train]:
        try:
            with open("train_data.json", "r") as f:
                trains_data = json.load(f)
                self.data["trains"] = {
                    train_id: Train(
                        train_id=train["train_id"],
                        name=train["train_name"],
                        route=tuple(train["route"]),
                    ) for train_id, train in trains_data.items()
                }
                for train_id, train in self.data["trains"].items():
                    train._schedule = trains_data[train_id]["schedule"]
                    train._coach = {
                        coach_id: Coach(
                            coach_id=coach["coach_id"],
                            total_seats=coach["total_seats"],
                            coach_type=coach["coach_type"]
                        ) for coach_id, coach in trains_data[train_id]["coaches"].items()
                    }
                    for coach_id, coach in train._coach.items():
                        coach._seat = {
                            seat_number: Passenger(
                                name=seat["name"],
                                age=seat["age"],
                                gender=seat["gender"],
                                contact=seat["contact"]
                            ) if seat else None
                            for seat_number, seat in trains_data[train_id]["coaches"][coach_id]["seats"].items()
                        }
            print("Train data loaded successfully.")
        except FileNotFoundError:
            print("No previous train data found. Returning an empty dictionary.")
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Error loading train data: {e}")
        return self.data["trains"]