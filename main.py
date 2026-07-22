from airport.models import Flight, Passenger, CarryOn, CheckedLuggage
from airport.queueing import CheckInQueue
from airport.counter import CheckInCounter
from airport.exceptions import (
    OverweightLuggageError,
    FlightFullError,
    EmptyQueueError,
)

if __name__ == "__main__":
    flight = Flight("AV001", "Bogota", "2026-06-10 08:30", capacity=2)
    queue = CheckInQueue()
    counter = CheckInCounter("CTR-01", flight, queue)

    p1 = Passenger("Ana Torres", "1020304050", "BR001", is_vip=False)
    p2 = Passenger("Luis Perez", "9988776655", "BR002", is_vip=True)
    p3 = Passenger("Marta Ruiz", "1122334455", "BR003", is_vip=False)

    p1_luggage = [CarryOn(8.5), CheckedLuggage(20.0)]
    p2_luggage = [CheckedLuggage(30.0)]
    p3_luggage = [CarryOn(5.0)]

    print("=== 1. Manual Check-In Demonstration ===")

    try:
        counter.check_in(p2, p2_luggage)
    except OverweightLuggageError as e:
        print(f"Rejected: {e}")

    boarding_pass = counter.check_in(p1, p1_luggage)
    print(boarding_pass.print_pass())

    print("\n=== 2. Queue Processing Generator Demonstration ===")

    queue.enqueue(p2, p2_luggage)
    queue.enqueue(p3, p3_luggage)

    for status, passenger, result in counter.process_queue():
        if status == "SUCCESS":
            print(f"Successful check-in for {passenger.get_name()}:")
            print(result.print_pass())
        else:
            print(f"Rejected ({passenger.get_name()}): {result}")

    print("\n=== 3. Flight Iterator & Exceptions Demonstration ===")

    for pass_issued in flight:
        print(f"Boarding pass on flight: {pass_issued.passenger.get_name()}")

    try:
        queue.next_passenger()
    except EmptyQueueError as e:
        print(f"Caught: {e}")
