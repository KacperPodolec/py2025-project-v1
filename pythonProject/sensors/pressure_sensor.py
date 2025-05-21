from .base_sensor import Sensor

# Klasa reprezentująca czujnik ciśnienia atmosferycznego
class PressureSensor(Sensor):
    def __init__(self, sensor_id):
        # Wywołanie konstruktora klasy bazowej (Sensor) z parametrami specyficznymi dla ciśnienia:
        # - sensor_id: identyfikator czujnika
        # - "Pressure": typ czujnika
        # - "hPa": jednostka miary (hektopaskale)
        # - 950.0: minimalna symulowana wartość ciśnienia
        # - 1050.0: maksymalna symulowana wartość ciśnienia
        super().__init__(sensor_id, "Pressure", "hPa", 950.0, 1050.0)
