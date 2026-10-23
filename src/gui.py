
import threading
import tkinter as tk
from tkinter import messagebox

from account import BankAccount
from atm import ATM, UPI
from monitor import TransactionMonitor
from notifier import EmailNotifier


class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JointBank - Shared Account Simulator")
        self.root.geometry("1100x820")
        self.root.minsize(950, 700)
        self.root.configure(bg="#111827")

        self.account = BankAccount(10000)
        self.atm1 = ATM(1, self.account)
        self.upi = UPI(2, self.account)
        self.monitor = TransactionMonitor(self.account)
        self.notifier = EmailNotifier(self.account.logger)

        self.atm_amount = tk.StringVar(value="7000")
        self.upi_amount = tk.StringVar(value="5000")
        self.deposit_amount = tk.StringVar(value="3000")
        self.start_balance = tk.StringVar(value="10000")

        self.busy = False
        self.log_position = 0

        self.build_ui()
        self.update_log()

    def make_button(self, parent, text, command, color="#2563eb"):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 10, "bold"),
            bg=color,
            fg="white",
            activebackground="#374151",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=7
        )

    def build_ui(self):
        header = tk.Frame(self.root, bg="#1f2937", pady=14)
        header.pack(fill="x")

        tk.Label(
            header,
            text="JOINTBANK",
            font=("Arial", 22, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(side="left", padx=24)

        tk.Label(
            header,
            text="SHARED ACCOUNT TRANSACTION MONITOR",
            font=("Arial", 10, "bold"),
            bg="#1f2937",
            fg="#9ca3af"
        ).pack(side="right", padx=20)

        main = tk.Frame(
            self.root, bg="#111827", padx=22, pady=12
        )
        main.pack(fill="both", expand=True)

        tk.Label(
            main,
            text="CURRENT JOINT ACCOUNT BALANCE",
            font=("Arial", 10, "bold"),
            bg="#111827",
            fg="#9ca3af"
        ).pack()

        self.balance_label = tk.Label(
            main,
            text="₹ 10,000",
            font=("Arial", 30, "bold"),
            bg="#111827",
            fg="#34d399"
        )
        self.balance_label.pack(pady=(0, 10))

        self.demo_balance_label = tk.Label(
            main,
            text="DEMO ACCOUNT: Not running",
            font=("Arial", 10, "bold"),
            bg="#111827",
            fg="#9ca3af"
        )
        self.demo_balance_label.pack(pady=(0, 8))

        settings = tk.Frame(
            main, bg="#1f2937", padx=12, pady=8
        )
        settings.pack(fill="x", pady=4)

        tk.Label(
            settings,
            text="Reset balance (₹)",
            bg="#1f2937",
            fg="white"
        ).pack(side="left")

        tk.Entry(
            settings,
            textvariable=self.start_balance,
            width=12,
            font=("Arial", 11)
        ).pack(side="left", padx=10)

        self.make_button(
            settings, "RESET ACCOUNT", self.reset_account, "#374151"
        ).pack(side="left", padx=5)

        cards = tk.Frame(main, bg="#111827")
        cards.pack(fill="x", pady=5)
        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)

        self.make_card(
            cards,
            "PERSON 1 · ATM WITHDRAWAL",
            "Withdrawal amount (₹)",
            self.atm_amount,
            0,
            self.withdraw_atm
        )

        self.make_card(
            cards,
            "PERSON 2 · UPI PAYMENT",
            "Payment amount (₹)",
            self.upi_amount,
            1,
            self.pay_upi
        )

        deposit_frame = tk.Frame(
            main, bg="#1f2937", padx=14, pady=10
        )
        deposit_frame.pack(fill="x", pady=6)

        tk.Label(
            deposit_frame,
            text="JOINT ACCOUNT DEPOSIT",
            font=("Arial", 12, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(side="left", padx=(0, 12))

        tk.Entry(
            deposit_frame,
            textvariable=self.deposit_amount,
            width=14,
            font=("Arial", 12)
        ).pack(side="left", padx=5)

        self.make_button(
            deposit_frame, "DEPOSIT", self.deposit, "#059669"
        ).pack(side="left", padx=8)

        controls = tk.Frame(
            main, bg="#1f2937", padx=8, pady=8
        )
        controls.pack(fill="x", pady=5)

        self.make_button(
            controls, "RUN CONCURRENT TEST",
            self.run_concurrent_test, "#2563eb"
        ).pack(side="left", padx=4)

        self.make_button(
            controls, "RUN RACE-CONDITION DEMO",
            self.run_detection_demo, "#7c3aed"
        ).pack(side="left", padx=4)

        self.make_button(
            controls, "CHECK BALANCE",
            self.check_balance, "#374151"
        ).pack(side="left", padx=4)

        self.status = tk.Label(
            main,
            text="READY · Normal transactions use mutex synchronization",
            font=("Arial", 11, "bold"),
            bg="#064e3b",
            fg="#6ee7b7",
            padx=10,
            pady=9,
            wraplength=1000,
            justify="left"
        )
        self.status.pack(fill="x", pady=5)

        tk.Label(
            main,
            text="LIVE TRANSACTION ACTIVITY",
            font=("Arial", 10, "bold"),
            bg="#111827",
            fg="#d1d5db"
        ).pack(anchor="w", pady=(4, 2))

        log_frame = tk.Frame(main, bg="#030712")
        log_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        self.log_box = tk.Text(
            log_frame,
            height=9,
            bg="#030712",
            fg="#a7f3d0",
            font=("Consolas", 9),
            relief="flat",
            state="disabled",
            yscrollcommand=scrollbar.set
        )
        self.log_box.pack(
            side="left", fill="both", expand=True, padx=6, pady=6
        )
        scrollbar.config(command=self.log_box.yview)

    def make_card(
        self, parent, title, label, variable, column, command
    ):
        card = tk.Frame(
            parent, bg="#1f2937", padx=14, pady=12
        )
        card.grid(
            row=0, column=column, padx=5, pady=5, sticky="nsew"
        )

        tk.Label(
            card, text=title, font=("Arial", 12, "bold"),
            bg="#1f2937", fg="white"
        ).pack(anchor="w")

        tk.Label(
            card, text=label, bg="#1f2937", fg="#9ca3af"
        ).pack(anchor="w", pady=(7, 3))

        tk.Entry(
            card, textvariable=variable, font=("Arial", 13), width=22
        ).pack(anchor="w")

        self.make_button(
            card, "PROCESS TRANSACTION", command
        ).pack(anchor="w", pady=(8, 0))

    def read_amount(self, variable, description):
        try:
            amount = int(variable.get())
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            messagebox.showerror(
                "Invalid amount",
                f"Enter a positive whole number for {description}."
            )
            return None

    def refresh_balance(self):
        self.balance_label.config(
            text=f"₹ {self.account.balance:,}"
        )

    def set_status(self, text, success):
        self.status.config(
            text=text,
            bg="#064e3b" if success else "#7f1d1d",
            fg="#6ee7b7" if success else "#fecaca"
        )

    def notify_transaction(
        self, transaction_type, amount, success, balance, details=""
    ):
        """Queue a notification without blocking the transaction or GUI."""
        subject_status = "SUCCESS" if success else "FAILED"
        subject = (
            f"JointBank: {subject_status} - {transaction_type}"
        )
        body = EmailNotifier.transaction_message(
            transaction_type=transaction_type,
            amount=amount,
            success=success,
            balance=balance,
            details=details
        )

        # Email delivery failure must never undo a transaction.
        self.notifier.send_async(subject, body)

    def start_operation(
        self, operation, description, transaction_type, amount
    ):
        if self.busy:
            messagebox.showwarning(
                "Please wait",
                "Another transaction is already running."
            )
            return

        self.busy = True
        result = {}

        self.status.config(
            text=f"PROCESSING · {description}",
            bg="#78350f",
            fg="#fde68a"
        )

        def worker():
            try:
                result["success"] = operation()
            except Exception as exc:
                result["error"] = str(exc)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

        self.poll_operation(
            thread, result, description, transaction_type, amount
        )

    def poll_operation(
        self, thread, result, description, transaction_type, amount
    ):
        if thread.is_alive():
            self.root.after(
                50, self.poll_operation, thread, result,
                description, transaction_type, amount
            )
            return

        self.busy = False
        self.refresh_balance()
        balance = self.account.balance

        if "error" in result:
            self.set_status(f"ERROR · {result['error']}", False)
            messagebox.showerror("Transaction error", result["error"])
            return

        success = result.get("success") is True
        details = (
            "Transaction completed."
            if success else "Transaction rejected; check available balance."
        )

        self.notify_transaction(
            transaction_type, amount, success, balance, details
        )

        if success:
            self.set_status(
                f"SUCCESS · {description} · New balance ₹{balance:,}",
                True
            )
            messagebox.showinfo(
                "Transaction successful",
                f"{description}\n\nUpdated joint balance: ₹{balance:,}"
            )
        else:
            self.set_status(
                f"FAILED · {description} · Balance ₹{balance:,}", False
            )
            messagebox.showerror(
                "Transaction failed",
                f"{description}\nInsufficient balance.\n\n"
                f"Current balance: ₹{balance:,}"
            )

    def withdraw_atm(self):
        amount = self.read_amount(self.atm_amount, "ATM withdrawal")
        if amount is None:
            return

        self.start_operation(
            lambda: self.atm1.withdraw(amount, True),
            f"Person 1 ATM withdrawal ₹{amount:,}",
            "ATM withdrawal",
            amount
        )

    def pay_upi(self):
        amount = self.read_amount(self.upi_amount, "UPI payment")
        if amount is None:
            return

        self.start_operation(
            lambda: self.upi.pay(amount, True),
            f"Person 2 UPI payment ₹{amount:,}",
            "UPI payment",
            amount
        )

    def deposit(self):
        amount = self.read_amount(
            self.deposit_amount, "joint account deposit"
        )
        if amount is None:
            return

        self.start_operation(
            lambda: self.atm1.deposit(amount, True),
            f"Joint account deposit ₹{amount:,}",
            "Joint account deposit",
            amount
        )

    def run_concurrent_test(self):
        if self.busy:
            messagebox.showwarning(
                "Please wait", "Another transaction is running."
            )
            return

        atm_amount = self.read_amount(self.atm_amount, "ATM withdrawal")
        upi_amount = self.read_amount(self.upi_amount, "UPI payment")

        if atm_amount is None or upi_amount is None:
            return

        self.busy = True
        results = {}

        self.status.config(
            text="RUNNING · ATM and UPI use mutex synchronization",
            bg="#78350f",
            fg="#fde68a"
        )

        def perform(name, operation):
            try:
                results[name] = operation()
            except Exception as exc:
                results[name] = exc

        t1 = threading.Thread(
            target=perform,
            args=("atm", lambda: self.atm1.withdraw(atm_amount, True))
        )
        t2 = threading.Thread(
            target=perform,
            args=("upi", lambda: self.upi.pay(upi_amount, True))
        )

        t1.start()
        t2.start()
        self.poll_concurrent(t1, t2, results, atm_amount, upi_amount)

    def poll_concurrent(self, t1, t2, results, atm_amount, upi_amount):
        if t1.is_alive() or t2.is_alive():
            self.root.after(
                50, self.poll_concurrent, t1, t2, results,
                atm_amount, upi_amount
            )
            return

        self.busy = False
        self.refresh_balance()
        balance = self.account.balance

        errors = [
            str(value) for value in results.values()
            if isinstance(value, Exception)
        ]

        if errors:
            self.set_status("CONCURRENT TEST ERROR", False)
            messagebox.showerror("Concurrent test error", "\n".join(errors))
            return

        atm_ok = results.get("atm") is True
        upi_ok = results.get("upi") is True

        self.notify_transaction(
            "ATM withdrawal (concurrent test)", atm_amount, atm_ok,
            balance, "Concurrent test; mutex synchronization enabled."
        )
        self.notify_transaction(
            "UPI payment (concurrent test)", upi_amount, upi_ok,
            balance, "Concurrent test; mutex synchronization enabled."
        )

        self.set_status(
            f"CONCURRENT TEST COMPLETE · "
            f"ATM: {'SUCCESS' if atm_ok else 'REJECTED'} · "
            f"UPI: {'SUCCESS' if upi_ok else 'REJECTED'} · "
            f"Balance ₹{balance:,}",
            True
        )

        messagebox.showinfo(
            "Concurrent test complete",
            f"ATM ₹{atm_amount:,}: "
            f"{'Successful' if atm_ok else 'Rejected'}\n"
            f"UPI ₹{upi_amount:,}: "
            f"{'Successful' if upi_ok else 'Rejected'}\n\n"
            f"Updated joint balance: ₹{balance:,}\n\n"
            "Both transactions used mutex synchronization."
        )

    def run_detection_demo(self):
        if self.busy:
            messagebox.showwarning(
                "Please wait",
                "Another transaction is already running."
            )
            return

        # This separate account prevents the demo from changing real balance.
        demo_account = BankAccount(10000)
        demo_account.demo_barrier = threading.Barrier(2)

        demo_atm = ATM(1, demo_account)
        demo_upi = UPI(2, demo_account)
        demo_monitor = TransactionMonitor(demo_account)

        self.busy = True
        self.status.config(
            text="RUNNING · Controlled race-condition demo",
            bg="#78350f",
            fg="#fde68a"
        )
        self.demo_balance_label.config(
            text="DEMO ACCOUNT: Running from ₹10,000",
            fg="#fbbf24"
        )

        results = {}

        def perform(name, operation):
            try:
                results[name] = operation()
            except Exception as exc:
                results[name] = exc

        t1 = threading.Thread(
            target=perform,
            args=("atm", lambda: demo_atm.withdraw(7000, False, True))
        )
        t2 = threading.Thread(
            target=perform,
            args=("upi", lambda: demo_upi.pay(5000, False, True))
        )

        t1.start()
        t2.start()
        self.poll_demo(t1, t2, demo_account, demo_monitor, results)

    def poll_demo(self, t1, t2, demo_account, demo_monitor, results):
        if t1.is_alive() or t2.is_alive():
            self.root.after(
                50, self.poll_demo, t1, t2, demo_account, demo_monitor, results
            )
            return

        self.busy = False

        result = demo_monitor.analyze()
        demo_balance = demo_account.balance
        real_balance = self.account.balance

        self.demo_balance_label.config(
            text=(
                f"DEMO BALANCE: ₹{demo_balance:,}  |  "
                f"REAL JOINT BALANCE: ₹{real_balance:,}"
            ),
            fg="#f87171" if result["race_condition"] else "#fbbf24"
        )

        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, "\n--- ISOLATED RACE-CONDITION DEMO ---\n")
        for line in demo_account.logger.get_logs():
            self.log_box.insert(tk.END, line + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")

        if result["race_condition"]:
            self.set_status(
                f"RACE CONDITION CONFIRMED · Demo balance ₹{demo_balance:,} · "
                f"Real balance ₹{real_balance:,}",
                False
            )

            evidence = "\n".join(result.get("evidence", []))

            self.notifier.send_async(
                "JointBank SIMULATION ALERT: Race condition detected",
                "SIMULATION ALERT — NOT A REAL ACCOUNT TRANSACTION\n\n"
                f"{result['message']}\n\n"
                f"Evidence:\n{evidence}\n\n"
                f"Demo balance: INR {demo_balance:,}\n"
                f"Real joint-account balance: INR {real_balance:,}\n\n"
                "This was an isolated educational race-condition demo. "
                "The real joint account was not changed by the demo."
            )

            messagebox.showwarning(
                "Race condition detected",
                f"{result['message']}\n\n{evidence}\n\n"
                f"Demo account balance: ₹{demo_balance:,}\n"
                f"Real joint-account balance: ₹{real_balance:,}\n\n"
                "The demo did not change the real account."
            )
        else:
            self.set_status(
                f"{result['status']} · Demo balance ₹{demo_balance:,} · "
                f"Real balance ₹{real_balance:,}",
                True
            )

            messagebox.showinfo(
                "Detection result",
                f"{result['status']}\n\n{result['message']}\n\n"
                f"Demo balance: ₹{demo_balance:,}\n"
                f"Real joint balance: ₹{real_balance:,}"
            )

    def update_log(self):
        logs = self.account.logger.get_logs()
        new_logs = logs[self.log_position:]

        if new_logs:
            self.log_box.config(state="normal")
            for line in new_logs:
                self.log_box.insert(tk.END, line + "\n")
            self.log_box.see(tk.END)
            self.log_box.config(state="disabled")
            self.log_position = len(logs)

        self.root.after(200, self.update_log)

    def check_balance(self):
        messagebox.showinfo(
            "Joint account balance",
            f"Current balance: ₹{self.account.balance:,}"
        )

    def reset_account(self):
        if self.busy:
            messagebox.showwarning(
                "Please wait",
                "Wait for the current operation to finish."
            )
            return

        try:
            balance = int(self.start_balance.get())
            if balance < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid balance",
                "Enter a non-negative whole number."
            )
            return

        self.account = BankAccount(balance)
        self.atm1 = ATM(1, self.account)
        self.upi = UPI(2, self.account)
        self.monitor = TransactionMonitor(self.account)
        self.notifier = EmailNotifier(self.account.logger)

        self.log_box.config(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.config(state="disabled")
        self.log_position = 0

        self.refresh_balance()
        self.demo_balance_label.config(
            text="DEMO ACCOUNT: Not running",
            fg="#9ca3af"
        )

        self.set_status(f"ACCOUNT RESET · Balance ₹{balance:,}", True)


def main():
    root = tk.Tk()
    ATMApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
