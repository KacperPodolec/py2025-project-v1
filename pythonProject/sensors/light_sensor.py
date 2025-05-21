from .base_sensor import Sensor

# Klasa reprezentująca czujnik natężenia światła (np. światła dziennego)
class LightSensor(Sensor):
    def __init__(self, sensor_id):
        # Wywołanie konstruktora klasy bazowej z parametrami dla światła:
        # - sensor_id: identyfikator czujnika
        # - "Light": typ czujnika
        # - "lux": jednostka natężenia światła
        # - 100.0: minimalna symulowana wartość (ciemne otoczenie)
        # - 1000.0: maksymalna symulowana wartość (jasne otoczenie)
        super().__init__(sensor_id, "Light", "lux", 100.0, 1000.0)
