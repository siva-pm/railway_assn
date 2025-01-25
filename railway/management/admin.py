from typing import TypeVar,Generic,Dict
from models.train import Train

T = TypeVar('T', bound=Train)

class Admin(Generic[T]):
    def __init__(self):
        self._trains: Dict[str, T] = {}

    def add_train(self, train: T) -> None:
        """Adds a train to the system."""
        try:
            # Ensure the train ID is unique
            if train.train_id in self._trains:
                raise ValueError(f"Train with ID '{train.train_id}' already exists.")
            
            # Add the train to the dictionary
            self._trains[train.train_id] = train
            print(f"Train '{train.name}' with ID '{train.train_id}' added successfully.")
        
        except ValueError as ve:
            print(f"ValueError: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred while adding the train: {e}")

    def remove_train(self, train_id: str) -> None:
        """Removes a train from the system."""
        try:
            # Ensure the train exists in the system
            if train_id not in self._trains:
                raise KeyError(f"Train with ID '{train_id}' does not exist.")
            
            # Remove the train
            del self._trains[train_id]
            print(f"Train with ID '{train_id}' removed successfully.")
        
        except KeyError as ke:
            print(f"KeyError: {ke}")
        except Exception as e:
            print(f"An unexpected error occurred while removing the train: {e}")

    def list_trains(self) -> None:
        """Displays all trains in the system."""
        if not self._trains:
            print("No trains available.")
        else:
            print("List of all trains:")
            for train_id, train in self._trains.items():
                print(f"Train ID: {train.train_id}, Train Name: {train.name}, Route: {train.route[0]} -> {train.route[1]}")

