from .base_sensor import Sensor

# Klasa reprezentująca czujnik temperatury
class TemperatureSensor(Sensor):
    def __init__(self, sensor_id):
        # Wywołanie konstruktora klasy bazowej (Sensor) z parametrami specyficznymi dla temperatury:
        # - sensor_id: unikalny identyfikator czujnika
        # - "Temperature": nazwa typu czujnika
        # - "°C": jednostka pomiaru
        # - -20.0: minimalna wartość generowana losowo (symulacja)
        # - 50.0: maksymalna wartość generowana losowo (symulacja)
        super().__init__(sensor_id, "Temperature", "°C", -20.0, 50.0)
