import tkinter as tk
from tkinter import messagebox, simpledialog
from account import BankAccount
from atm import ATM


# =========================================================
# ATM CASH WITHDRAWAL SIMULATOR
# Hybrid ATM + OS Synchronization Dashboard
# =========================================================

class ATMApp:

    def __init__(self, root):
        self.root = root
        self.root.title("ATM Cash Withdrawal Simulator")
        self.root.geometry("1100x850")
        self.root.resizable(False, False)
        self.root.configure(bg="#111827")

        # Shared bank account
        self.account = BankAccount(10000)

        # Two ATM terminals accessing the same account
        self.atm1 = ATM(1, self.account)
        self.atm2 = ATM(2, self.account)

        self.safe_mode = True
        self.log_position = 0
        self.test_running = False

        self.show_welcome_screen()

    # =====================================================
    # COMMON UI HELPERS
    # =====================================================

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def make_button(self, parent, text, command, width=16):
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            font=("Arial", 10, "bold"),
            bg="#374151",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=5,
            pady=6
        )

    # =====================================================
    # WELCOME SCREEN
    # =====================================================

    def show_welcome_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg="#111827")
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="🏧",
            font=("Arial", 48),
            bg="#111827",
            fg="white"
        ).pack(pady=(65, 5))

        tk.Label(
            frame,
            text="ATM CASH WITHDRAWAL SIMULATOR",
            font=("Arial", 26, "bold"),
            bg="#111827",
            fg="white"
        ).pack()

        tk.Label(
            frame,
            text="Critical Section • Mutex Synchronization • Race Condition",
            font=("Arial", 13),
            bg="#111827",
            fg="#9ca3af"
        ).pack(pady=10)

        card = tk.Frame(
            frame,
            bg="#1f2937",
            padx=45,
            pady=30
        )
        card.pack(pady=35)

        tk.Label(
            card,
            text="SHARED BANK ACCOUNT",
            font=("Arial", 13, "bold"),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack()

        tk.Label(
            card,
            text="₹ 10,000",
            font=("Arial", 30, "bold"),
            bg="#1f2937",
            fg="#34d399"
        ).pack(pady=10)

        tk.Label(
            card,
            text="Two ATM terminals • One shared balance",
            font=("Arial", 10),
            bg="#1f2937",
            fg="#9ca3af"
        ).pack()

        tk.Button(
            frame,
            text="START ATM",
            command=self.show_atm_screen,
            font=("Arial", 14, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            relief="flat",
            cursor="hand2",
            width=22,
            height=2
        ).pack(pady=15)

        tk.Label(
            frame,
            text="● SAFE — Mutex Enabled",
            font=("Arial", 11, "bold"),
            bg="#111827",
            fg="#34d399"
        ).pack(pady=8)

    # =====================================================
    # ATM SCREEN
    # =====================================================

    def show_atm_screen(self):
        self.clear_screen()

        main = tk.Frame(self.root, bg="#111827")
        main.pack(fill="both", expand=True)

        # ---------------- HEADER ----------------

        header = tk.Frame(main, bg="#1f2937", height=75)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🏧 ATM CONCURRENT TRANSACTION SYSTEM",
            font=("Arial", 20, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(side="left", padx=25, pady=20)

        tk.Label(
            header,
            text="OS LAB • CRITICAL SECTION",
            font=("Arial", 10, "bold"),
            bg="#1f2937",
            fg="#9ca3af"
        ).pack(side="right", padx=25)

        # ---------------- BALANCE ----------------

        balance_card = tk.Frame(main, bg="#1f2937", padx=25, pady=10)
        balance_card.pack(fill="x", padx=22, pady=(16, 8))

        tk.Label(
            balance_card,
            text="SHARED ACCOUNT BALANCE",
            font=("Arial", 10, "bold"),
            bg="#1f2937",
            fg="#9ca3af"
        ).pack()

        self.balance_label = tk.Label(
            balance_card,
            text=f"₹ {self.account.balance:,}",
            font=("Arial", 28, "bold"),
            bg="#1f2937",
            fg="#34d399"
        )
        self.balance_label.pack()

        # ---------------- ATM TERMINALS ----------------

        atm_area = tk.Frame(main, bg="#111827")
        atm_area.pack(fill="x", padx=22, pady=8)

        self.create_atm_card(
            atm_area,
            "ATM 01",
            0,
            self.withdraw_atm1
        )

        self.create_atm_card(
            atm_area,
            "ATM 02",
            1,
            self.withdraw_atm2
        )

        # ---------------- SYNCHRONIZATION ----------------

        sync = tk.Frame(
            main,
            bg="#1f2937",
            padx=18,
            pady=10
        )
        sync.pack(fill="x", padx=22, pady=6)

        tk.Label(
            sync,
            text="SYNCHRONIZATION MODE",
            font=("Arial", 10, "bold"),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack(side="left", padx=(5, 15))

        self.mode_var = tk.StringVar(value="SAFE")

        tk.Radiobutton(
            sync,
            text="SAFE — Mutex Enabled",
            variable=self.mode_var,
            value="SAFE",
            command=self.change_mode,
            font=("Arial", 10, "bold"),
            bg="#1f2937",
            fg="#34d399",
            selectcolor="#111827",
            activebackground="#1f2937",
            activeforeground="#34d399"
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            sync,
            text="UNSAFE — Mutex Disabled",
            variable=self.mode_var,
            value="UNSAFE",
            command=self.change_mode,
            font=("Arial", 10, "bold"),
            bg="#1f2937",
            fg="#f87171",
            selectcolor="#111827",
            activebackground="#1f2937",
            activeforeground="#f87171"
        ).pack(side="left", padx=10)

        self.status_label = tk.Label(
            sync,
            text="● SAFE — Mutex Enabled",
            font=("Arial", 10, "bold"),
            bg="#1f2937",
            fg="#34d399"
        )
        self.status_label.pack(side="right", padx=10)

        # ---------------- RACE STATUS ----------------

        self.race_label = tk.Label(
            main,
            text="✓  NO RACE CONDITION DETECTED",
            font=("Arial", 12, "bold"),
            bg="#064e3b",
            fg="#6ee7b7",
            padx=10,
            pady=8
        )
        self.race_label.pack(fill="x", padx=22, pady=6)

        # ---------------- ACTIONS ----------------

        actions = tk.Frame(main, bg="#111827")
        actions.pack(pady=4)

        self.make_button(
            actions,
            "⚡ RUN CONCURRENT TEST",
            self.run_concurrent_test,
            25
        ).grid(row=0, column=0, padx=5)

        self.make_button(
            actions,
            "＋ DEPOSIT",
            self.deposit,
            15
        ).grid(row=0, column=1, padx=5)

        self.make_button(
            actions,
            "BALANCE",
            self.check_balance,
            13
        ).grid(row=0, column=2, padx=5)

        self.make_button(
            actions,
            "RESET",
            self.reset_account,
            13
        ).grid(row=0, column=3, padx=5)

        self.make_button(
            actions,
            "EXIT",
            self.show_welcome_screen,
            13
        ).grid(row=0, column=4, padx=5)

        # ---------------- MONITOR ----------------

        tk.Label(
            main,
            text="LIVE SYNCHRONIZATION MONITOR",
            font=("Arial", 11, "bold"),
            bg="#111827",
            fg="#d1d5db"
        ).pack(pady=(7, 3))

        monitor_frame = tk.Frame(main, bg="#030712")
        monitor_frame.pack(padx=22, fill="x")

        self.log_box = tk.Text(
            monitor_frame,
            height=8,
            width=110,
            bg="#030712",
            fg="#a7f3d0",
            insertbackground="white",
            font=("Consolas", 9),
            relief="flat",
            state="disabled"
        )
        self.log_box.pack(padx=8, pady=8)

        self.log_position = len(self.account.logger.get_logs())
        self.update_log()

    # =====================================================
    # ATM CARD
    # =====================================================

    def create_atm_card(self, parent, title, column, command):
        card = tk.Frame(
            parent,
            bg="#1f2937",
            width=510,
            height=150,
            padx=22,
            pady=12
        )
        card.grid(row=0, column=column, padx=8, sticky="nsew")
        card.grid_propagate(False)

        tk.Label(
            card,
            text=f"▣  {title}",
            font=("Arial", 14, "bold"),
            bg="#1f2937",
            fg="white"
        ).grid(row=0, column=0, columnspan=2, sticky="w")

        tk.Label(
            card,
            text="WITHDRAWAL AMOUNT",
            font=("Arial", 9, "bold"),
            bg="#1f2937",
            fg="#9ca3af"
        ).grid(row=1, column=0, sticky="w", pady=(10, 2))

        entry = tk.Entry(
            card,
            font=("Arial", 13),
            bg="#111827",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=20
        )
        entry.grid(row=2, column=0, padx=(0, 12), sticky="w")

        if title == "ATM 01":
            self.atm1_amount = entry
        else:
            self.atm2_amount = entry

        tk.Button(
            card,
            text="WITHDRAW",
            command=command,
            font=("Arial", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            relief="flat",
            cursor="hand2",
            width=15,
            pady=6
        ).grid(row=2, column=1, sticky="e")

    # =====================================================
    # LIVE LOG
    # =====================================================

    def update_log(self):
        if not hasattr(self, "log_box"):
            return

        logs = self.account.logger.get_logs()
        new_logs = logs[self.log_position:]

        for log in new_logs:
            self.log_box.config(state="normal")
            self.log_box.insert(tk.END, log + "\n")
            self.log_box.see(tk.END)
            self.log_box.config(state="disabled")

            if "Entered critical section" in log:
                self.status_label.config(
                    text="● CRITICAL SECTION ACTIVE",
                    fg="#fbbf24"
                )

            elif "Waiting for critical section" in log:
                self.status_label.config(
                    text="● ATM WAITING FOR CRITICAL SECTION",
                    fg="#fbbf24"
                )

            elif "Lock released" in log:
                if self.mode_var.get() == "SAFE":
                    self.status_label.config(
                        text="● SAFE — Mutex Enabled",
                        fg="#34d399"
                    )

            elif "Withdrawal successful" in log:
                if self.mode_var.get() == "UNSAFE":
                    self.status_label.config(
                        text="● UNSAFE — Critical Section Unprotected",
                        fg="#f87171"
                    )

        self.log_position = len(logs)

        self.root.after(200, self.update_log)

    # =====================================================
    # CHANGE MODE
    # =====================================================

    def change_mode(self):
        if self.mode_var.get() == "SAFE":
            self.safe_mode = True

            self.status_label.config(
                text="● SAFE — Mutex Enabled",
                fg="#34d399"
            )

            self.race_label.config(
                text="✓  NO RACE CONDITION DETECTED",
                bg="#064e3b",
                fg="#6ee7b7"
            )

        else:
            self.safe_mode = False

            self.status_label.config(
                text="● UNSAFE — Mutex Disabled",
                fg="#f87171"
            )

            self.race_label.config(
                text="⚠  UNSAFE TEST MODE — RACE CONDITION CAN OCCUR",
                bg="#450a0a",
                fg="#fca5a5"
            )

    # =====================================================
    # ATM 01 WITHDRAWAL
    # =====================================================

    def withdraw_atm1(self):
        try:
            amount = int(self.atm1_amount.get())
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

        synchronized = self.mode_var.get() == "SAFE"

        thread = self.atm1.start_withdrawal(
            amount,
            synchronized
        )

        thread.start()
        thread.join()

        self.update_balance()
        self.atm1_amount.delete(0, tk.END)

    # =====================================================
    # ATM 02 WITHDRAWAL
    # =====================================================

    def withdraw_atm2(self):
        try:
            amount = int(self.atm2_amount.get())
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

        synchronized = self.mode_var.get() == "SAFE"

        thread = self.atm2.start_withdrawal(
            amount,
            synchronized
        )

        thread.start()
        thread.join()

        self.update_balance()
        self.atm2_amount.delete(0, tk.END)

    # =====================================================
    # CONCURRENT TEST
    # =====================================================

    def run_concurrent_test(self):
        if self.test_running:
            return

        try:
            amount1 = int(self.atm1_amount.get())
            amount2 = int(self.atm2_amount.get())
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

        synchronized = self.mode_var.get() == "SAFE"

        self.test_running = True
        self.test_initial_balance = self.account.balance
        self.test_safe_mode = synchronized
        self.test_log_start = len(self.account.logger.get_logs())

        self.log_box.config(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.config(state="disabled")

        if synchronized:
            self.race_label.config(
                text="⟳  TESTING SAFE SYNCHRONIZATION...",
                bg="#78350f",
                fg="#fde68a"
            )
        else:
            self.race_label.config(
                text="⟳  TESTING UNSAFE SYNCHRONIZATION...",
                bg="#78350f",
                fg="#fde68a"
            )

        self.log_position = len(self.account.logger.get_logs())

        thread1 = self.atm1.start_withdrawal(
            amount1,
            synchronized
        )

        thread2 = self.atm2.start_withdrawal(
            amount2,
            synchronized
        )

        thread1.start()
        thread2.start()

        self.root.after(
            100,
            self.check_threads,
            thread1,
            thread2,
            amount1,
            amount2
        )

    # =====================================================
    # CHECK THREADS
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
            return

        self.test_running = False
        self.update_balance()

        initial_balance = self.test_initial_balance
        final_balance = self.account.balance
        total_requested = amount1 + amount2

        logs = self.account.logger.get_logs()
        recent_logs = logs[self.test_log_start:]

        successful_withdrawals = 0

        for log in recent_logs:
            if "Withdrawal successful" in log:
                successful_withdrawals += 1

        # ---------------- RACE CONDITION ----------------

        if (
            not self.test_safe_mode
            and successful_withdrawals >= 2
            and total_requested > initial_balance
        ):
            self.race_label.config(
                text="🔴  RACE CONDITION DETECTED",
                bg="#7f1d1d",
                fg="#fecaca",
                font=("Arial", 14, "bold")
            )

            messagebox.showwarning(
                "RACE CONDITION DETECTED",
                f"Both ATM transactions succeeded.\n\n"
                f"Initial Balance: ₹{initial_balance:,}\n"
                f"Total Requested: ₹{total_requested:,}\n"
                f"Final Balance: ₹{final_balance:,}\n\n"
                f"INCONSISTENT ACCOUNT STATE\n\n"
                f"The shared balance was accessed "
                f"without synchronization."
            )

        # ---------------- SAFE RESULT ----------------

        elif (
            self.test_safe_mode
            and total_requested > initial_balance
        ):
            self.race_label.config(
                text="🟢  NO RACE CONDITION — MUTEX PROTECTED",
                bg="#064e3b",
                fg="#6ee7b7",
                font=("Arial", 13, "bold")
            )

            messagebox.showinfo(
                "Safe Synchronization",
                f"Mutex protected the critical section.\n\n"
                f"Initial Balance: ₹{initial_balance:,}\n"
                f"Total Requested: ₹{total_requested:,}\n"
                f"Final Balance: ₹{final_balance:,}\n\n"
                f"Only valid transactions were allowed."
            )

        else:
            self.race_label.config(
                text="🟢  NO RACE CONDITION DETECTED",
                bg="#064e3b",
                fg="#6ee7b7",
                font=("Arial", 13, "bold")
            )

        messagebox.showinfo(
            "Concurrent Test Complete",
            f"ATM 01 requested: ₹{amount1:,}\n"
            f"ATM 02 requested: ₹{amount2:,}\n\n"
            f"Final Balance: ₹{final_balance:,}"
        )

        self.atm1_amount.delete(0, tk.END)
        self.atm2_amount.delete(0, tk.END)

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
            f"ATM 1 processed deposit of ₹{amount:,}."
        )

    # =====================================================
    # CHECK BALANCE
    # =====================================================

    def check_balance(self):
        messagebox.showinfo(
            "Account Balance",
            f"Available Balance: ₹{self.account.balance:,}"
        )

    # =====================================================
    # RESET
    # =====================================================

    def reset_account(self):
        self.account = BankAccount(10000)

        self.atm1 = ATM(1, self.account)
        self.atm2 = ATM(2, self.account)

        self.test_running = False
        self.safe_mode = True

        self.update_balance()

        self.log_position = 0

        if hasattr(self, "log_box"):
            self.log_box.config(state="normal")
            self.log_box.delete("1.0", tk.END)
            self.log_box.config(state="disabled")

        if hasattr(self, "mode_var"):
            self.mode_var.set("SAFE")

        if hasattr(self, "status_label"):
            self.status_label.config(
                text="● SAFE — Mutex Enabled",
                fg="#34d399"
            )

        if hasattr(self, "race_label"):
            self.race_label.config(
                text="✓  NO RACE CONDITION DETECTED",
                bg="#064e3b",
                fg="#6ee7b7",
                font=("Arial", 12, "bold")
            )

        messagebox.showinfo(
            "Account Reset",
            "Shared account reset to ₹10,000."
        )

    # =====================================================
    # UPDATE BALANCE
    # =====================================================

    def update_balance(self):
        if hasattr(self, "balance_label"):
            self.balance_label.config(
                text=f"₹ {self.account.balance:,}"
            )


# =========================================================
# MAIN
# =========================================================

def main():
    root = tk.Tk()
    ATMApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
