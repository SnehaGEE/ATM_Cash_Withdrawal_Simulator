import tkinter as tk
from tkinter import messagebox, simpledialog
from account import BankAccount
from atm import ATM


class ATMApp:

    def __init__(self, root):
        self.root = root

        root.title("ATM Cash Withdrawal Simulator")
        root.geometry("900x600")
        root.resizable(False, False)

        self.account = BankAccount(10000)

        self.atm1 = ATM(1, self.account)
        self.atm2 = ATM(2, self.account)

        self.safe_mode = True

        self.show_welcome_screen()

    # ---------------- WELCOME SCREEN ----------------

    def show_welcome_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(
            self.root,
            bg="#202020"
        )
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="ATM CASH WITHDRAWAL SIMULATOR",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#202020"
        ).pack(pady=(70, 20))

        tk.Label(
            frame,
            text="Critical Section & Race Condition Demonstration",
            font=("Arial", 13),
            fg="lightgray",
            bg="#202020"
        ).pack(pady=10)

        tk.Label(
            frame,
            text="SHARED BANK ACCOUNT",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#202020"
        ).pack(pady=(50, 10))

        tk.Label(
            frame,
            text="Balance: ₹10,000",
            font=("Arial", 22, "bold"),
            fg="#00ff99",
            bg="#202020"
        ).pack(pady=10)

        tk.Button(
            frame,
            text="START ATM",
            font=("Arial", 16, "bold"),
            width=18,
            height=2,
            command=self.show_atm_screen
        ).pack(pady=50)

        tk.Label(
            frame,
            text="Synchronization Mode: SAFE",
            font=("Arial", 12, "bold"),
            fg="#00ff99",
            bg="#202020"
        ).pack()

    # ---------------- ATM SCREEN ----------------

    def show_atm_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(
            self.root,
            bg="#202020"
        )
        main_frame.pack(fill="both", expand=True)

        # Header
        tk.Label(
            main_frame,
            text="ATM TERMINAL",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#202020"
        ).pack(pady=25)

        # Balance
        self.balance_label = tk.Label(
        main_frame,
        text=f"Available Balance: ₹{self.account.balance}",
            font=("Arial", 18, "bold"),
            fg="#00ff99",
            bg="#202020"
        )
        self.balance_label.pack(pady=15)

        # Synchronization mode
        mode_frame = tk.Frame(
            main_frame,
            bg="#303030",
            padx=20,
            pady=15
        )
        mode_frame.pack(pady=15)

        tk.Label(
            mode_frame,
            text="SYNCHRONIZATION MODE",
            font=("Arial", 13, "bold"),
            fg="white",
            bg="#303030"
        ).pack()

        self.mode_var = tk.StringVar(value="SAFE")

        tk.Radiobutton(
            mode_frame,
            text="SAFE — Mutex Enabled",
            variable=self.mode_var,
            value="SAFE",
            fg="#00ff99",
            bg="#303030",
            selectcolor="#202020",
            font=("Arial", 11, "bold"),
            command=self.change_mode
        ).pack(side="left", padx=20, pady=10)

        tk.Radiobutton(
            mode_frame,
            text="UNSAFE — Mutex Disabled",
            variable=self.mode_var,
            value="UNSAFE",
            fg="#ff5555",
            bg="#303030",
            selectcolor="#202020",
            font=("Arial", 11, "bold"),
            command=self.change_mode
        ).pack(side="left", padx=20, pady=10)

        # ATM operations
        button_frame = tk.Frame(
            main_frame,
            bg="#202020"
        )
        button_frame.pack(pady=30)

        tk.Button(
            button_frame,
            text="WITHDRAW",
            width=18,
            height=2,
            font=("Arial", 13, "bold"),
            command=self.withdraw
        ).grid(row=0, column=0, padx=15, pady=10)

        tk.Button(
            button_frame,
            text="DEPOSIT",
            width=18,
            height=2,
            font=("Arial", 13, "bold"),
            command=self.deposit
        ).grid(row=0, column=1, padx=15, pady=10)

        tk.Button(
            button_frame,
            text="CHECK BALANCE",
            width=18,
            height=2,
            font=("Arial", 13, "bold"),
            command=self.check_balance
        ).grid(row=1, column=0, padx=15, pady=10)

        tk.Button(
            button_frame,
            text="EXIT",
            width=18,
            height=2,
            font=("Arial", 13, "bold"),
            command=self.show_welcome_screen
        ).grid(row=1, column=1, padx=15, pady=10)

        self.status_label = tk.Label(
            main_frame,
            text="Synchronization Status: SAFE",
            font=("Arial", 13, "bold"),
            fg="#00ff99",
            bg="#202020"
        )
        self.status_label.pack(pady=20)

    # ---------------- FUNCTIONS ----------------

    def change_mode(self):

        if self.mode_var.get() == "SAFE":

            self.safe_mode = True

            self.status_label.config(
                text="Synchronization Status: SAFE — Mutex Enabled",
                fg="#00ff99"
            )

        else:

            self.safe_mode = False

            self.status_label.config(
                text="Synchronization Status: UNSAFE — Mutex Disabled",
                fg="#ff5555"
            )

    def withdraw(self):

        amount = simpledialog.askinteger(
        "Withdrawal",
        "Enter withdrawal amount:"
        )

        if amount is None:
            return

        if amount <= 0:
            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid amount."
            )
            return

        synchronized = self.mode_var.get() == "SAFE"

        thread = self.atm1.start_withdrawal(
            amount,
            synchronized
        )

        thread.start()
        thread.join()

        self.update_balance()

        messagebox.showinfo(
            "Transaction Complete",
            f"ATM 1 processed withdrawal of ₹{amount}."
        )

    def deposit(self):

        amount = simpledialog.askinteger(
            "Deposit",
            "Enter deposit amount:"
        )

        if amount is None:
            return

        if amount <= 0:
            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid amount."
            )
            return

        synchronized = self.mode_var.get() == "SAFE"

        thread = self.atm1.start_deposit(
            amount,
            synchronized
        )

        thread.start()
        thread.join()

        self.update_balance()

        messagebox.showinfo(
            "Transaction Complete",
            f"ATM 1 processed deposit of ₹{amount}."
    )

    def check_balance(self):

        messagebox.showinfo(
        "Account Balance",
        f"Available Balance: ₹{self.account.balance}"
    )

    def update_balance(self):

        self.balance_label.config(
        text=f"Available Balance: ₹{self.account.balance}"
    )


def main():

    root = tk.Tk()

    app = ATMApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()