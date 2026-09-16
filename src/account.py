import threading
import time
from logger import TransactionLogger


class BankAccount:

    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()
        self.logger = TransactionLogger()

    def withdraw(self, user, amount, synchronized=True):

        self.logger.log(
            f"{user} → Withdrawal requested: ₹{amount}"
        )

        if synchronized:
            self.logger.log(
                f"{user} → Waiting for critical section"
            )
            self.lock.acquire()

        try:
            self.logger.log(
                f"{user} → Entered critical section"
            )

            current_balance = self.balance

            # Simulate ATM processing time
            time.sleep(1)

            if current_balance >= amount:

                self.balance = current_balance - amount

                self.logger.log(
                    f"{user} → Withdrawal successful: ₹{amount}"
                )

                self.logger.log(
                    f"Account balance: ₹{self.balance}"
                )

            else:

                self.logger.log(
                    f"{user} → Withdrawal failed: Insufficient balance"
                )

            self.logger.log(
                f"{user} → Leaving critical section"
            )

        finally:

            if synchronized:
                self.lock.release()

                self.logger.log(
                    f"{user} → Lock released"
                )

    def deposit(self, user, amount, synchronized=True):

        self.logger.log(
            f"{user} → Deposit requested: ₹{amount}"
        )

        if synchronized:
            self.lock.acquire()

        try:
            self.logger.log(
                f"{user} → Entered critical section"
            )

            current_balance = self.balance

            time.sleep(1)

            self.balance = current_balance + amount

            self.logger.log(
                f"{user} → Deposit successful: ₹{amount}"
            )

            self.logger.log(
                f"Account balance: ₹{self.balance}"
            )

            self.logger.log(
                f"{user} → Leaving critical section"
            )

        finally:

            if synchronized:
                self.lock.release()

                self.logger.log(
                    f"{user} → Lock released"
                )