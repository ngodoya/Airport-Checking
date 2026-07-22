from models import BoardingPass
from exception import FlightFullError, OverweightLuggageError


class CheckInCounter:
    def __init__(self, counter_id, flight, queue):
        self.counter_id = counter_id
        self.flight = flight
        self.queue = queue

    def check_in(self, passenger, luggage_items):
        if self.flight.is_full():
            raise FlightFullError(f"Flight {self.flight.code} is full.")

        for item in luggage_items:
            item.validate_weight()

        seat = self.flight.assign_seat()

        boarding_pass = BoardingPass(passenger, self.flight, seat, luggage_items)

        self.flight.register_boartdin_pass(boarding_pass)
        return boarding_pass

    def process_queue(self):
        while not self.queue.is_empty():
            passenger, luggage_items = self.queue.next_passenger()

            try:
                boarding_pass = self.queue.next(passenger, luggage_items)
                yield ("SUCCESS", passenger, boarding_pass)

            except FlightFullError as error:
                yield ("REJECTED", passenger, error)

            except OverweightLuggageError as error:
                yield ("REJECTED", passenger, error)
