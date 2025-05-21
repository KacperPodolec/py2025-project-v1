from .base_sensor import Sensor

# Klasa reprezentująca czujnik wilgotności
class HumiditySensor(Sensor):
    def __init__(self, sensor_id):
        # Wywołanie konstruktora klasy bazowej Sensor z parametrami charakterystycznymi dla wilgotności:
        # - sensor_id: unikalny identyfikator czujnika
        # - "Humidity": typ czujnika
        # - "%": jednostka miary wilgotności
        # - 10.0: minimalna symulowana wartość (niska wilgotność)
        # - 90.0: maksymalna symulowana wartość (wysoka wilgotność)
        super().__init__(sensor_id, "Humidity", "%", 10.0, 90.0)
