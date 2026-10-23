from account import BankAccount
from atm import ATM

def run_withdrawal_test(synchronized):

    account = BankAccount(10000)

    atm1 = ATM(1, account)
    atm2 = ATM(2, account)

    mode = (
        "SAFE - WITH SYNCHRONIZATION"
        if synchronized
        else "UNSAFE - WITHOUT SYNCHRONIZATION"
    )

    print("\n========================================")
    print(mode)
    print("========================================")
    print("Initial Balance: ₹10,000\n")

    thread1 = atm1.start_withdrawal(7000, synchronized)
    thread2 = atm2.start_withdrawal(5000, synchronized)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(f"Final Balance: ₹{account.balance}")
    print("========================================\n")


def run_deposit_withdrawal_test():

    account = BankAccount(10000)

    atm1 = ATM(1, account)
    atm2 = ATM(2, account)
    atm3 = ATM(3, account)

    print("\n========================================")
    print("DEPOSIT + WITHDRAWAL TEST")
    print("========================================")
    print("Initial Balance: ₹10,000\n")

    thread1 = atm1.start_withdrawal(7000, True)
    thread2 = atm2.start_deposit(5000, True)
    thread3 = atm3.start_withdrawal(6000, True)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    print(f"Final Balance: ₹{account.balance}")
    print("========================================\n")


def main():

    run_withdrawal_test(False)

    run_withdrawal_test(True)

    run_deposit_withdrawal_test()


if __name__ == "__main__":
    main()