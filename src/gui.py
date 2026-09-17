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

        # Shared bank account
        self.account = BankAccount(10000)

        # Two ATM terminals accessing the same account
        self.atm1 = ATM(1, self.account)
        self.atm2 = ATM(2, self.account)

        # Default synchronization mode
        self.safe_mode = True

        self.show_welcome_screen()

    # =====================================================
    # WELCOME SCREEN
    # =====================================================

    def show_welcome_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(
            self.root,
            bg="#202020"
        )

        frame.pack(
            fill="both",
            expand=True
        )

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

    # =====================================================
    # ATM SCREEN
    # =====================================================

    def show_atm_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(
            self.root,
            bg="#202020"
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # ---------------- HEADER ----------------

        tk.Label(
            main_frame,
            text="ATM CONCURRENT TRANSACTION SYSTEM",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#202020"
        ).pack(pady=15)

        # ---------------- SHARED BALANCE ----------------

        self.balance_label = tk.Label(
            main_frame,
            text=f"SHARED ACCOUNT BALANCE: ₹{self.account.balance}",
            font=("Arial", 18, "bold"),
            fg="#00ff99",
            bg="#202020"
        )

        self.balance_label.pack(pady=8)

        # =================================================
        # SYNCHRONIZATION MODE
        # =================================================

        mode_frame = tk.Frame(
            main_frame,
            bg="#303030",
            padx=15,
            pady=8
        )

        mode_frame.pack(pady=8)

        tk.Label(
            mode_frame,
            text="SYNCHRONIZATION MODE:",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#303030"
        ).pack(side="left", padx=10)

        self.mode_var = tk.StringVar(
            value="SAFE"
        )

        tk.Radiobutton(
            mode_frame,
            text="SAFE — Mutex Enabled",
            variable=self.mode_var,
            value="SAFE",
            fg="#00ff99",
            bg="#303030",
            selectcolor="#202020",
            font=("Arial", 10, "bold"),
            command=self.change_mode
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            mode_frame,
            text="UNSAFE — Mutex Disabled",
            variable=self.mode_var,
            value="UNSAFE",
            fg="#ff5555",
            bg="#303030",
            selectcolor="#202020",
            font=("Arial", 10, "bold"),
            command=self.change_mode
        ).pack(side="left", padx=10)

        # =================================================
        # ATM PANELS
        # =================================================

        atm_frame = tk.Frame(
            main_frame,
            bg="#202020"
        )

        atm_frame.pack(pady=15)

        # ---------------- ATM 01 ----------------

        atm1_frame = tk.LabelFrame(
            atm_frame,
            text="ATM 01",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#303030",
            padx=20,
            pady=15
        )

        atm1_frame.grid(
            row=0,
            column=0,
            padx=15
        )

        tk.Label(
            atm1_frame,
            text="Enter Amount",
            fg="white",
            bg="#303030",
            font=("Arial", 11)
        ).pack()

        self.atm1_amount = tk.Entry(
            atm1_frame,
            font=("Arial", 13),
            width=15
        )

        self.atm1_amount.pack(pady=8)

        tk.Button(
            atm1_frame,
            text="WITHDRAW",
            width=15,
            command=self.withdraw_atm1
        ).pack(pady=5)

        # ---------------- ATM 02 ----------------

        atm2_frame = tk.LabelFrame(
            atm_frame,
            text="ATM 02",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#303030",
            padx=20,
            pady=15
        )

        atm2_frame.grid(
            row=0,
            column=1,
            padx=15
        )

        tk.Label(
            atm2_frame,
            text="Enter Amount",
            fg="white",
            bg="#303030",
            font=("Arial", 11)
        ).pack()

        self.atm2_amount = tk.Entry(
            atm2_frame,
            font=("Arial", 13),
            width=15
        )

        self.atm2_amount.pack(pady=8)

        tk.Button(
            atm2_frame,
            text="WITHDRAW",
            width=15,
            command=self.withdraw_atm2
        ).pack(pady=5)

        # =================================================
        # CONCURRENT TEST
        # =================================================

        tk.Button(
            main_frame,
            text="RUN CONCURRENT WITHDRAWALS",
            font=("Arial", 12, "bold"),
            width=30,
            height=2,
            command=self.run_concurrent_test
        ).pack(pady=15)

        # =================================================
        # OTHER OPERATIONS
        # =================================================

        other_frame = tk.Frame(
            main_frame,
            bg="#202020"
        )

        other_frame.pack(pady=5)

        tk.Button(
            other_frame,
            text="DEPOSIT",
            width=15,
            command=self.deposit
        ).grid(
            row=0,
            column=0,
            padx=6
        )

        tk.Button(
            other_frame,
            text="CHECK BALANCE",
            width=15,
            command=self.check_balance
        ).grid(
            row=0,
            column=1,
            padx=6
        )

        tk.Button(
            other_frame,
            text="RESET ACCOUNT",
            width=15,
            command=self.reset_account
        ).grid(
            row=0,
            column=2,
            padx=6
        )

        tk.Button(
            other_frame,
            text="EXIT",
            width=15,
            command=self.show_welcome_screen
        ).grid(
            row=0,
            column=3,
            padx=6
        )

        # =================================================
        # RACE CONDITION INDICATOR
        # =================================================

        self.race_label = tk.Label(
            main_frame,
            text="STATUS: NO RACE CONDITION DETECTED",
            font=("Arial", 13, "bold"),
            fg="#00ff99",
            bg="#202020"
        )

        self.race_label.pack(pady=(8, 5))

        # =================================================
        # LIVE SYNCHRONIZATION MONITOR
        # =================================================

        tk.Label(
            main_frame,
            text="LIVE SYNCHRONIZATION MONITOR",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#202020"
        ).pack(pady=(5, 3))

        self.log_box = tk.Text(
            main_frame,
            height=9,
            width=90,
            bg="#101010",
            fg="#00ff99",
            font=("Consolas", 9),
            state="disabled"
        )

        self.log_box.pack(pady=5)

        # =================================================
        # STATUS
        # =================================================

        self.status_label = tk.Label(
            main_frame,
            text="Synchronization Status: SAFE — Mutex Enabled",
            font=("Arial", 12, "bold"),
            fg="#00ff99",
            bg="#202020"
        )

        self.status_label.pack(pady=8)

        # Remember current log position
        self.log_position = len(
            self.account.logger.get_logs()
        )

        # Start live log monitoring
        self.update_log()

    # =====================================================
    # LIVE LOG UPDATE
    # =====================================================

    def update_log(self):

        if not hasattr(self, "log_box"):
            return

        logs = self.account.logger.get_logs()

        new_logs = logs[self.log_position:]

        for log in new_logs:

            self.log_box.config(
                state="normal"
            )

            self.log_box.insert(
                tk.END,
                log + "\n"
            )

            self.log_box.see(
                tk.END
            )

            self.log_box.config(
                state="disabled"
            )

            # Update status based on latest event
            if "Entered critical section" in log:

                self.status_label.config(
                    text="CRITICAL SECTION ACTIVE",
                    fg="#ffaa00"
                )

            elif "Waiting for critical section" in log:

                self.status_label.config(
                    text="ATM WAITING FOR CRITICAL SECTION",
                    fg="#ffaa00"
                )

            elif "Lock released" in log:

                if self.mode_var.get() == "SAFE":

                    self.status_label.config(
                        text="SAFE — Mutex Enabled",
                        fg="#00ff99"
                    )

            elif "Withdrawal successful" in log:

                if self.mode_var.get() == "UNSAFE":

                    self.status_label.config(
                        text="UNSAFE — Critical Section Unprotected",
                        fg="#ff5555"
                    )

        self.log_position = len(logs)

        self.root.after(
            200,
            self.update_log
        )

    # =====================================================
    # CHANGE SYNCHRONIZATION MODE
    # =====================================================

    def change_mode(self):

        if self.mode_var.get() == "SAFE":

            self.safe_mode = True

            self.status_label.config(
                text="Synchronization Status: SAFE — Mutex Enabled",
                fg="#00ff99"
            )

            self.race_label.config(
                text="STATUS: NO RACE CONDITION DETECTED",
                fg="#00ff99"
            )

        else:

            self.safe_mode = False

            self.status_label.config(
                text="Synchronization Status: UNSAFE — Mutex Disabled",
                fg="#ff5555"
            )

            self.race_label.config(
                text="STATUS: RACE CONDITION TEST MODE",
                fg="#ff5555"
            )

    # =====================================================
    # ATM 01 WITHDRAWAL
    # =====================================================

    def withdraw_atm1(self):

        try:

            amount = int(
                self.atm1_amount.get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid number."
            )

            return

        if amount <= 0:

            messagebox.showerror(
                "Invalid Amount",
                "Enter an amount greater than zero."
            )

            return

        synchronized = (
            self.mode_var.get() == "SAFE"
        )

        thread = self.atm1.start_withdrawal(
            amount,
            synchronized
        )

        thread.start()
        thread.join()

        self.update_balance()

        self.atm1_amount.delete(
            0,
            tk.END
        )

    # =====================================================
    # ATM 02 WITHDRAWAL
    # =====================================================

    def withdraw_atm2(self):

        try:

            amount = int(
                self.atm2_amount.get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid number."
            )

            return

        if amount <= 0:

            messagebox.showerror(
                "Invalid Amount",
                "Enter an amount greater than zero."
            )

            return

        synchronized = (
            self.mode_var.get() == "SAFE"
        )

        thread = self.atm2.start_withdrawal(
            amount,
            synchronized
        )

        thread.start()
        thread.join()

        self.update_balance()

        self.atm2_amount.delete(
            0,
            tk.END
        )

    # =====================================================
    # CONCURRENT WITHDRAWAL TEST
    # =====================================================

    def run_concurrent_test(self):

        try:

            amount1 = int(
                self.atm1_amount.get()
            )

            amount2 = int(
                self.atm2_amount.get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Enter valid amounts for both ATMs."
            )

            return

        if amount1 <= 0 or amount2 <= 0:

            messagebox.showerror(
                "Invalid Amount",
                "Both amounts must be greater than zero."
            )

            return

        synchronized = (
            self.mode_var.get() == "SAFE"
        )

        # Store starting balance for race detection
        self.test_initial_balance = self.account.balance
        self.test_amount1 = amount1
        self.test_amount2 = amount2
        self.test_safe_mode = synchronized

        # Clear previous monitor
        self.log_box.config(
            state="normal"
        )

        self.log_box.delete(
            "1.0",
            tk.END
        )

        self.log_box.config(
            state="disabled"
        )

        # Reset race indicator
        if synchronized:

            self.race_label.config(
                text="STATUS: TESTING SAFE SYNCHRONIZATION...",
                fg="#ffaa00"
            )

        else:

            self.race_label.config(
                text="STATUS: TESTING UNSAFE SYNCHRONIZATION...",
                fg="#ffaa00"
            )

        # Start reading logs from current point
        # Save a fixed log position for race-condition detection
        self.test_log_start = len(
            self.account.logger.get_logs()
        )

        # Create concurrent threads
        thread1 = self.atm1.start_withdrawal(
            amount1,
            synchronized
        )

        thread2 = self.atm2.start_withdrawal(
            amount2,
            synchronized
        )

        # Start both threads
        thread1.start()
        thread2.start()

        # Check their status without freezing GUI
        self.root.after(
            100,
            self.check_threads,
            thread1,
            thread2,
            amount1,
            amount2
        )

    # =====================================================
    # CHECK CONCURRENT THREADS
    # =====================================================

    def check_threads(
        self,
        thread1,
        thread2,
        amount1,
        amount2
    ):

        if thread1.is_alive() or thread2.is_alive():

            self.root.after(
                100,
                self.check_threads,
                thread1,
                thread2,
                amount1,
                amount2
            )

        else:

            self.update_balance()

            # ---------------------------------------------
            # RACE CONDITION DETECTION
            # ---------------------------------------------

            total_requested = amount1 + amount2
            initial_balance = self.test_initial_balance
            final_balance = self.account.balance

            logs = self.account.logger.get_logs()

            recent_logs = logs[self.test_log_start:]

            successful_withdrawals = 0

            for log in recent_logs:

                if "Withdrawal successful" in log:
                    successful_withdrawals += 1

            # UNSAFE CASE
            # Both withdrawals succeed even though their
            # combined amount exceeds the initial balance.
            if (
                not self.test_safe_mode
                and successful_withdrawals >= 2
                and total_requested > initial_balance
            ):

                self.race_label.config(
                    text="🔴 RACE CONDITION DETECTED",
                    fg="#ff3333",
                    font=("Arial", 15, "bold")
                )

                messagebox.showwarning(
                    "RACE CONDITION DETECTED",
                    f"Both ATM transactions succeeded.\n\n"
                    f"Initial Balance: ₹{initial_balance}\n"
                    f"Total Requested: ₹{total_requested}\n"
                    f"Final Balance: ₹{final_balance}\n\n"
                    f"INCONSISTENT ACCOUNT STATE\n\n"
                    f"The shared balance was accessed "
                    f"without synchronization."
                )

            # SAFE CASE
            elif (
                self.test_safe_mode
                and total_requested > initial_balance
            ):

                self.race_label.config(
                    text="🟢 NO RACE CONDITION — MUTEX PROTECTED",
                    fg="#00ff99",
                    font=("Arial", 13, "bold")
                )

                messagebox.showinfo(
                    "Safe Synchronization",
                    f"Mutex protected the critical section.\n\n"
                    f"Initial Balance: ₹{initial_balance}\n"
                    f"Total Requested: ₹{total_requested}\n"
                    f"Final Balance: ₹{final_balance}\n\n"
                    f"Only valid transactions were allowed."
                )

            else:

                self.race_label.config(
                    text="🟢 NO RACE CONDITION DETECTED",
                    fg="#00ff99",
                    font=("Arial", 13, "bold")
                )

            # ---------------------------------------------
            # FINAL RESULT
            # ---------------------------------------------

            messagebox.showinfo(
                "Concurrent Test Complete",
                f"ATM 01 requested: ₹{amount1}\n"
                f"ATM 02 requested: ₹{amount2}\n\n"
                f"Final Balance: ₹{self.account.balance}"
            )

            self.atm1_amount.delete(
                0,
                tk.END
            )

            self.atm2_amount.delete(
                0,
                tk.END
            )

    # =====================================================
    # DEPOSIT
    # =====================================================

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

        synchronized = (
            self.mode_var.get() == "SAFE"
        )

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

    # =====================================================
    # CHECK BALANCE
    # =====================================================

    def check_balance(self):

        messagebox.showinfo(
            "Account Balance",
            f"Available Balance: ₹{self.account.balance}"
        )

    # =====================================================
    # RESET ACCOUNT
    # =====================================================

    def reset_account(self):

        self.account = BankAccount(
            10000
        )

        self.atm1 = ATM(
            1,
            self.account
        )

        self.atm2 = ATM(
            2,
            self.account
        )

        self.update_balance()

        self.log_position = 0

        self.log_box.config(
            state="normal"
        )

        self.log_box.delete(
            "1.0",
            tk.END
        )

        self.log_box.config(
            state="disabled"
        )

        self.status_label.config(
            text="Synchronization Status: SAFE — Mutex Enabled",
            fg="#00ff99"
        )

        self.race_label.config(
            text="STATUS: NO RACE CONDITION DETECTED",
            fg="#00ff99",
            font=("Arial", 13, "bold")
        )

        self.mode_var.set(
            "SAFE"
        )

        self.safe_mode = True

        messagebox.showinfo(
            "Account Reset",
            "Shared account reset to ₹10,000."
        )

    # =====================================================
    # UPDATE BALANCE
    # =====================================================

    def update_balance(self):

        self.balance_label.config(
            text=f"SHARED ACCOUNT BALANCE: ₹{self.account.balance}"
        )


# =========================================================
# MAIN
# =========================================================

def main():

    root = tk.Tk()

    app = ATMApp(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()