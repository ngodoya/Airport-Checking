from collections import deque

from airport.exceptions import EmptyQueueError
from airport.models import Passenger


class CheckInQueue:
    def __init__(self) -> None:
        self._vip_queue: deque[tuple[Passenger, list]] = deque()
        self._regular_queue: deque[tuple[Passenger, list]] = deque()

    def enqueue(self, passenger: Passenger, luggage_items: list) -> None:
        entry = (passenger, luggage_items)
        if passenger.is_vip:
            self._vip_queue.append(entry)
        else:
            self._regular_queue.append(entry)

    def next_passenger(self) -> tuple[Passenger, list]:
        if self._vip_queue:
            return self._vip_queue.popleft()
        if self._regular_queue:
            return self._regular_queue.popleft()
        raise EmptyQueueError()

    def is_empty(self) -> bool:
        return not self._vip_queue and not self._regular_queue
