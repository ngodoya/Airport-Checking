from airport.models import Flight, Passenger, CarryOn, CheckedLuggage
from airport.queueing import CheckInQueue
from airport.counter import CheckInCounter
from airport.exceptions import (
    OverweightLuggageError,
    FlightFullError,
    EmptyQueueError,
)

if __name__ == "__main__":
    flight = Flight("AV001", "Bogota", "2026-06-10 08:30", capacity=1)
    queue = CheckInQueue()
    counter = CheckInCounter("CTR-01", flight, queue)

    p1 = Passenger("Ana Torres", "1020304050", "BR001", is_vip=False)
    p2 = Passenger("Luis Perez", "9988776655", "BR002", is_vip=True)
    p3 = Passenger("Marta Ruiz", "1122334455", "BR003", is_vip=False)

    p1_luggage = [CarryOn(8.5), CheckedLuggage(20.0)]
    p2_luggage = [CheckedLuggage(30.0)]
    p3_luggage = [CarryOn(5.0)]

    queue.enqueue(p1, p1_luggage)
    queue.enqueue(p2, p2_luggage)

    next_p = queue.next_passenger()
    try:
        counter.check_in(next_p, p2_luggage)
    except OverweightLuggageError as e:
        print(f"Rechazado: {e}")

    next_p = queue.next_passenger()
    boarding_pass = counter.check_in(next_p, p1_luggage)
    print(boarding_pass.print_pass())

    try:
        counter.check_in(p3, p3_luggage)
    except FlightFullError as e:
        print(f"Rechazado: {e}")

    for pass_issued in flight:
        print(f"Pase en vuelo: {pass_issued.passenger.get_name()}")

    try:
        queue.next_passenger()
    except EmptyQueueError as e:
        print(f"Capturado: {e}")
