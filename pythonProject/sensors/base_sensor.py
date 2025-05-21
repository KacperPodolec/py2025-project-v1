import numpy as np
from datetime import datetime

class Sensor:
    def __init__(self, sensor_id, name, unit, min_value, max_value, frequency=1):
        self.sensor_id = sensor_id
        self.name = name
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value
        self.frequency = frequency  # Hz
        self.callbacks = []

    def register_callback(self, callback):
        """
        Rejestruje funkcję, która ma zostać wywołana po każdym odczycie czujnika.
        Zwykle będzie to metoda `log_reading` z klasy Logger.
        """
        self.callbacks.append(callback)

    def read_value(self):
        """
        Generuje losową wartość w zadanym zakresie i wywołuje wszystkie zarejestrowane callbacki
        z odpowiednimi danymi pomiarowymi.
        """
        value = np.random.uniform(self.min_value, self.max_value)   # Losowa wartość z zakresu
        timestamp = datetime.now()                                  # Aktualna data i czas odczytu
        for callback in self.callbacks:
            # Wywołanie zarejestrowanej funkcji z danymi pomiarowymi
            callback(sensor_id=self.sensor_id, timestamp=timestamp, value=value, unit=self.unit)
