
import threading
import time
from logger import TransactionLogger


class BankAccount:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()
        self.logger = TransactionLogger()
        self.demo_barrier = None

    def withdraw(
        self, user, amount, synchronized=True,
        use_demo_barrier=False
    ):
        self.logger.log(
            f"{user} → Transaction requested: Withdrawal ₹{amount}"
        )

        if synchronized:
            self.logger.log(f"{user} → Lock requested")
            self.lock.acquire()

        try:
            self.logger.log(
                f"{user} → Critical section entered"
            )

            current_balance = self.balance
            self.logger.log(
                f"{user} → Balance read: ₹{current_balance}"
            )

            # Used only by the isolated race-condition demonstration.
            if use_demo_barrier and self.demo_barrier:
                self.logger.log(
                    f"{user} → Waiting at demo synchronization point"
                )
                self.demo_barrier.wait(timeout=5)

            time.sleep(0.2)

            if current_balance >= amount:
                new_balance = current_balance - amount
                self.balance = new_balance

                self.logger.log(
                    f"{user} → Balance updated: "
                    f"₹{current_balance} → ₹{new_balance}"
                )
                self.logger.log(
                    f"{user} → Withdrawal successful: ₹{amount}"
                )
                self.logger.log(
                    f"New account balance: ₹{self.balance}"
                )
                return True

            self.logger.log(
                f"{user} → Transaction failed: Insufficient balance"
            )
            return False

        except threading.BrokenBarrierError:
            self.logger.log(
                f"{user} → Demo synchronization timed out"
            )
            return False

        finally:
            if synchronized:
                self.lock.release()
                self.logger.log(f"{user} → Lock released")

            self.logger.log(
                f"{user} → Leaving critical section"
            )

    def deposit(self, user, amount, synchronized=True):
        self.logger.log(
            f"{user} → Transaction requested: Deposit ₹{amount}"
        )

        if synchronized:
            self.logger.log(f"{user} → Lock requested")
            self.lock.acquire()

        try:
            self.logger.log(
                f"{user} → Critical section entered"
            )

            current_balance = self.balance
            self.logger.log(
                f"{user} → Balance read: ₹{current_balance}"
            )

            time.sleep(0.2)

            self.balance = current_balance + amount

            self.logger.log(
                f"{user} → Balance updated: "
                f"₹{current_balance} → ₹{self.balance}"
            )
            self.logger.log(
                f"{user} → Deposit successful: ₹{amount}"
            )
            self.logger.log(
                f"New account balance: ₹{self.balance}"
            )
            return True

        finally:
            if synchronized:
                self.lock.release()
                self.logger.log(f"{user} → Lock released")

            self.logger.log(
                f"{user} → Leaving critical section"
            )
