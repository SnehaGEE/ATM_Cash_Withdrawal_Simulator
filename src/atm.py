
import threading


class ATM:
    def __init__(self, atm_id, account):
        self.atm_id = atm_id
        self.account = account

    def withdraw(
        self, amount, synchronized=True,
        use_demo_barrier=False
    ):
        user = f"ATM {self.atm_id}"
        return self.account.withdraw(
            user, amount, synchronized, use_demo_barrier
        )

    def deposit(self, amount, synchronized=True):
        user = f"ATM {self.atm_id}"
        return self.account.deposit(
            user, amount, synchronized
        )

    def start_withdrawal(
        self, amount, synchronized=True,
        use_demo_barrier=False
    ):
        return threading.Thread(
            target=self.withdraw,
            args=(amount, synchronized, use_demo_barrier)
        )

    def start_deposit(self, amount, synchronized=True):
        return threading.Thread(
            target=self.deposit,
            args=(amount, synchronized)
        )


class UPI:
    def __init__(self, user_id, account):
        self.user_id = user_id
        self.account = account

    def pay(
        self, amount, synchronized=True,
        use_demo_barrier=False
    ):
        user = f"UPI User {self.user_id}"
        return self.account.withdraw(
            user, amount, synchronized, use_demo_barrier
        )

    def start_payment(
        self, amount, synchronized=True,
        use_demo_barrier=False
    ):
        return threading.Thread(
            target=self.pay,
            args=(amount, synchronized, use_demo_barrier)
        )
