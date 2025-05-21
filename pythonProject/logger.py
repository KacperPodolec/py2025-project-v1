import os
import csv
import json
import zipfile
from datetime import datetime, timedelta
from typing import Optional, Iterator, Dict

class Logger:
    def __init__(self, config_path: str):
        # Wczytanie konfiguracji z pliku JSON
        with open(config_path, "r") as f:
            config = json.load(f)

        # Parametry konfiguracyjne
        self.log_dir = config["log_dir"]
        self.filename_pattern = config["filename_pattern"]
        self.buffer_size = config["buffer_size"]
        self.rotate_every_hours = config["rotate_every_hours"]
        self.max_size_mb = config["max_size_mb"]
        self.rotate_after_lines = config.get("rotate_after_lines", None)
        self.retention_days = config["retention_days"]

        # Tworzenie katalogów, jeśli nie istnieją
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(os.path.join(self.log_dir, "archive"), exist_ok=True)

        # Inicjalizacja pól pomocniczych
        self.buffer = []
        self.current_file = None
        self.current_writer = None
        self.file_start_time = None
        self.current_filename = ""
        self.current_line_count = 0

    def start(self):
        # Rozpoczęcie nowego pliku logu
        self.file_start_time = datetime.now()
        self.current_filename = self._generate_filename()
        file_path = os.path.join(self.log_dir, self.current_filename)

        is_new = not os.path.exists(file_path)  # Sprawdzenie czy plik już istnieje
        self.current_file = open(file_path, "a", newline="")    # Otwórz w trybie dopisywania
        self.current_writer = csv.writer(self.current_file)

        if is_new:
            # Jeśli plik nowy – dodaj nagłówek
            self.current_writer.writerow(["timestamp", "sensor_id", "value", "unit"])

    def stop(self):
        # Zatrzymanie loggera – zapis i zamknięcie pliku
        self._flush()
        if self.current_file:
            self.current_file.close()
            self._rotate_if_needed(force=True)  # Wymuszenie rotacji przy zamknięciu

    def log_reading(self, sensor_id: str, timestamp: datetime, value: float, unit: str):
        # Dodanie nowego wpisu do bufora
        self.buffer.append([timestamp.isoformat(), sensor_id, value, unit])
        if len(self.buffer) >= self.buffer_size:
            self._flush()   # Zapis do pliku
            self._rotate_if_needed()    # Sprawdzenie potrzeby rotacji

    def read_logs(self, start: datetime, end: datetime, sensor_id: Optional[str] = None) -> Iterator[Dict]:
        # Czytanie danych z plików logów w zadanym zakresie czasu (i opcjonalnie dla danego czujnika)
        for file in self._get_all_log_files():
            open_fn = self._open_file(file)
            with open_fn as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row_time = datetime.fromisoformat(row["timestamp"])
                    if start <= row_time <= end:
                        if sensor_id is None or row["sensor_id"] == sensor_id:
                            yield {
                                "timestamp": row_time,
                                "sensor_id": row["sensor_id"],
                                "value": float(row["value"]),
                                "unit": row["unit"]
                            }

    def _flush(self):
        # Wypisanie zawartości bufora do pliku
        for entry in self.buffer:
            self.current_writer.writerow(entry)
            self.current_line_count += 1
        self.current_file.flush()
        self.buffer.clear()

    def _generate_filename(self):
        # Generowanie nazwy pliku wg wzorca z konfiguracji
        return datetime.now().strftime(self.filename_pattern)

    def _rotate_if_needed(self, force=False):
        # Sprawdzenie, czy należy wykonać rotację pliku
        now = datetime.now()
        file_path = os.path.join(self.log_dir, self.current_filename)
        should_rotate = False

        # Warunki wymuszające rotację
        if force:
            should_rotate = True
        elif (now - self.file_start_time).total_seconds() >= self.rotate_every_hours * 3600:
            should_rotate = True
        elif os.path.getsize(file_path) >= self.max_size_mb * 1024 * 1024:
            should_rotate = True
        elif self.rotate_after_lines and self.current_line_count >= self.rotate_after_lines:
            should_rotate = True

        if should_rotate:
            # Jeśli należy zrotować:
            self.current_file.close()  # Zamknięcie pliku
            self._archive_file(file_path)  # Przeniesienie do archiwum
            self._cleanup_old_archives()  # Usuwanie starych archiwów
            self.start()  # Utworzenie nowego pliku logu

    def _archive_file(self, file_path):
        # Spakowanie i przeniesienie pliku do katalogu archive/
        archive_path = os.path.join(self.log_dir, "archive", os.path.basename(file_path) + ".zip")
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, arcname=os.path.basename(file_path))
        os.remove(file_path)    # Usunięcie oryginalnego pliku CSV

    def _cleanup_old_archives(self):
        # Usunięcie archiwów starszych niż retention_days
        archive_dir = os.path.join(self.log_dir, "archive")
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        for file in os.listdir(archive_dir):
            full_path = os.path.join(archive_dir, file)
            if os.path.isfile(full_path) and datetime.fromtimestamp(os.path.getmtime(full_path)) < cutoff:
                os.remove(full_path)

    def _get_all_log_files(self):
        # Pobranie listy wszystkich plików CSV i ZIP do odczytu
        files = []
        for f in os.listdir(self.log_dir):
            if f.endswith(".csv"):
                files.append(os.path.join(self.log_dir, f))
        for f in os.listdir(os.path.join(self.log_dir, "archive")):
            if f.endswith(".zip"):
                files.append(os.path.join(self.log_dir, "archive", f))
        return files

    def _open_file(self, filepath):
        # Otwarcie pliku CSV lub pliku ZIP (archiwum)
        if filepath.endswith(".zip"):
            zf = zipfile.ZipFile(filepath)
            inner = zf.namelist()[0]    # Zakładamy, że w archiwum jest tylko jeden plik
            return zf.open(inner, 'r')
        else:
            return open(filepath, 'r', newline='')
