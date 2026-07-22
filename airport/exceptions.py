class FlightFullError(Exception):
    def __init__(self, flight_code: str) -> None:
        super().__init__(f"El vuelo {flight_code} no tiene cupos disponibles.")

class OverweightLuggageError(Exception):
    def __init__(self, weight: float, max_weight: float, luggage_type: str) -> None:
        super().__init__(f"{luggage_type} pesa {weight} kg, excede el maximo permitido de {max_weight} kg.")

class EmptyQueueError(Exception):
    def __init__(self) -> None:
        super().__init__("No hay pasajeros en la fila de espera.")
