import threading

class ATM:
    def __init__(self, atm_id, account):
        self.atm_id = atm_id
        self.account = account

    def withdraw(self, amount, synchronized=True):
        user = f"ATM {self.atm_id}"
        self.account.withdraw(user, amount, synchronized)

    def deposit(self, amount, synchronized=True):
        user = f"ATM {self.atm_id}"
        self.account.deposit(user, amount, synchronized)

    def start_withdrawal(self, amount, synchronized=True):
        thread = threading.Thread(
            target=self.withdraw,
            args=(amount, synchronized)
        )
        return thread

    def start_deposit(self, amount, synchronized=True):
        thread = threading.Thread(
            target=self.deposit,
            args=(amount, synchronized)
        )
        return thread