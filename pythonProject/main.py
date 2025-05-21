import time
# Importy klas czujników z modułu sensors
from sensors.temperature_sensor import TemperatureSensor
from sensors.pressure_sensor import PressureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.light_sensor import LightSensor

# Import loggera odpowiedzialnego za zapis odczytów do plików
from logger import Logger

def main():
    logger = Logger(config_path="config.json")
    logger.start()

    # Lista czujników z unikalnymi identyfikatorami
    sensors = [
        TemperatureSensor("T1"),
        PressureSensor("P1"),
        HumiditySensor("H1"),
        LightSensor("L1")
    ]

    # Rejestracja logger jako obserwatora (callback) dla każdego czujnika
    for sensor in sensors:
        sensor.register_callback(logger.log_reading)

    try:
        print("Rozpoczynanie symulacji...")
        # Cykliczny odczyt danych z czujników
        while True:
            for sensor in sensors:
                sensor.read_value()
            time.sleep(1)
    except KeyboardInterrupt:
        # Obsługa przerwania programu
        print("Zatrzymywanie symulacji...")
    finally:
        # Zatrzymujemy logger: zapisujemy dane z bufora i zamykamy plik
        logger.stop()

if __name__ == "__main__":
    main()
