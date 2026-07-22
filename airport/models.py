from abc import ABC, abstractmethod
from typing import Iterator
import uuid

from .exceptions import FlightFullError, OverweightLuggageError


class Passenger:
    def __init__(
        self, name: str, document_id: str, booking_ref: str, is_vip: bool = False
    ):
        self.name: str = name
        self.__document_id: str = document_id
        self.booking_ref: str = booking_ref
        self.is_vip: bool = is_vip

    def get_masked_id(self) -> str:
        __id = ""
        id_text = str(self.__document_id)
        _document_id = range(len(id_text))
        for i in _document_id:
            if i < (len(_document_id) - 4):
                __id = __id + "*"
            else:
                __id = __id + id_text[i]
        return __id

    def get_name(self) -> str:
        return self.name

    def __repr__(self) -> str:
        vip_tag = " [VIP]" if self.is_vip else ""
        return f"Passenger({self.name}{vip_tag}, ref={self.booking_ref})"


class Luggage(ABC):
    def __init__(self, weight: float):
        self.weight: float = weight
        self._tag_id: str = uuid.uuid4().hex[:8].upper()

    @abstractmethod
    def validate_weight(self) -> None:

        pass

    def get_tag(self) -> str:

        return self._tag_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(weight={self.weight} kg, tag={self._tag_id})"


class CarryOn(Luggage):
    MAX_WEIGHT: float = 10.0

    def validate_weight(self) -> None:
        if self.weight > self.MAX_WEIGHT:
            raise OverweightLuggageError(self.weight, self.MAX_WEIGHT, "CarryOn")


class CheckedLuggage(Luggage):
    MAX_WEIGHT: float = 23.0

    def validate_weight(self) -> None:
        if self.weight > self.MAX_WEIGHT:
            raise OverweightLuggageError(self.weight, self.MAX_WEIGHT, "CheckedLuggage")


# ──────────────────────────────────────────────
#  BoardingPass
# ──────────────────────────────────────────────
class BoardingPass:
    def __init__(
        self, passenger: Passenger, flight: "Flight", seat: str, luggage_list: list
    ):
        self.passenger: Passenger = passenger
        self.flight: "Flight" = flight
        self.seat: str = seat
        self.luggage_list: list = luggage_list

    def print_pass(self) -> str:

        luggage_info = (
            ", ".join(
                f"{item.__class__.__name__}({item.weight}kg)"
                for item in self.luggage_list
            )
            or "Sin equipaje"
        )

        return (
            "╔══════════════════════════════════════╗\n"
            "║         BOARDING PASS                ║\n"
            "╠══════════════════════════════════════╣\n"
            f"║ Passanger : {self.passenger.get_name():<25}║\n"
            f"║ Id: {self.passenger.get_masked_id():<25}        ║\n"
            f"║ Flight   : {self.flight.code:<25} ║\n"
            f"║ Destiny  : {self.flight.destination:<25} ║\n"
            f"║ Exit   : {self.flight.departure:<25}   ║\n"
            f"║ Seat  : {self.seat:<25}    ╚═══════════╗\n"
            f"║ Lugagge : {luggage_info:<25} ║\n"
            "╚══════════════════════════════════════════════════╝"
        )

    def __repr__(self) -> str:
        return f"BoardingPass({self.passenger.get_name()}, {self.flight.code}, seat={self.seat})"


# ──────────────────────────────────────────────
#  Flight
# ──────────────────────────────────────────────
class Flight:
    def __init__(self, code: str, destination: str, departure: str, capacity: int):
        self.code: str = code
        self.destination: str = destination
        self.departure: str = departure
        self.capacity: int = capacity
        self._assigned_seats: list[str] = []
        self._boarding_passes: list[BoardingPass] = []

    def available_seats(self) -> int:
        return self.capacity - len(self._assigned_seats)

    def is_full(self) -> bool:
        return self.available_seats() <= 0

    def assign_seat(self) -> str:
        if self.is_full():
            raise FlightFullError(self.code)
        letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[len(self._assigned_seats)]
        seat = f"1{letter}"
        self._assigned_seats.append(seat)
        return seat

    def add_boarding_pass(self, boarding_pass: BoardingPass) -> None:
        self._boarding_passes.append(boarding_pass)

    def __iter__(self) -> Iterator[BoardingPass]:
        return iter(self._boarding_passes)

    def __repr__(self) -> str:
        return (
            f"Flight({self.code}, {self.destination}, "
            f"seats={self.available_seats()}/{self.capacity})"
        )
