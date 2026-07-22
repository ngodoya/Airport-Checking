class FlightFullError(Exception):
    def __init__(self, flight_code: str) -> None:
        super().__init__(f"El vuelo {flight_code} no tiene cupos disponibles.")
