from collections import deque

from airport.exceptions import EmptyQueueError
from airport.models import Passenger


class CheckInQueue:
    def __init__(self) -> None:
        self._vip_queue: deque[Passenger] = deque()
        self._regular_queue: deque[Passenger] = deque()

    def enqueue(self, passenger: Passenger) -> None:
        if passenger.is_vip:
            self._vip_queue.append(passenger)
        else:
            self._regular_queue.append(passenger)

    def next_passenger(self) -> Passenger:
        if self._vip_queue:
            return self._vip_queue.popleft()
        if self._regular_queue:
            return self._regular_queue.popleft()
        raise EmptyQueueError()

    def is_empty(self) -> bool:
        return not self._vip_queue and not self._regular_queue
