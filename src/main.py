
import threading

from account import BankAccount
from atm import ATM, UPI
from monitor import TransactionMonitor


def run_test(synchronized):
    account = BankAccount(10000)
    monitor = TransactionMonitor(account)

    atm = ATM(1, account)
    upi = UPI(2, account)

    mode = "SAFE MODE" if synchronized else "UNSAFE DEMO MODE"

    print("\n" + "=" * 45)
    print(mode)
    print("=" * 45)
    print("Initial balance: ₹10,000")

    # Force both unsafe transactions to read the old balance
    # before either is allowed to update it.
    if not synchronized:
        account.demo_barrier = threading.Barrier(2)

    atm_thread = threading.Thread(
        target=atm.withdraw,
        args=(7000, synchronized, not synchronized)
    )

    upi_thread = threading.Thread(
        target=upi.pay,
        args=(5000, synchronized, not synchronized)
    )

    atm_thread.start()
    upi_thread.start()

    atm_thread.join()
    upi_thread.join()

    result = monitor.analyze()

    print("\nFinal balance:", f"₹{account.balance}")
    print("Monitor status:", result["status"])
    print("Details:", result["message"])

    if result["evidence"]:
        print("Evidence:")
        for item in result["evidence"]:
            print("-", item)

    print("=" * 45)


def main():
    run_test(synchronized=True)
    run_test(synchronized=False)


if __name__ == "__main__":
    main()
