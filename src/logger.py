import threading
from datetime import datetime


class TransactionLogger:

    def __init__(self):
        self.logs = []
        self.lock = threading.Lock()

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")

        with self.lock:
            entry = f"[{timestamp}] {message}"
            self.logs.append(entry)
            print(entry)

    def get_logs(self):
        with self.lock:
            return self.logs.copy()