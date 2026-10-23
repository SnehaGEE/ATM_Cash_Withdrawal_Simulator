# JointBank — Shared Account Simulator

A Python-based Operating Systems mini-project demonstrating multithreading, mutex synchronization, concurrent transactions, race-condition detection, transaction logging, and email notifications.

## Overview

JointBank simulates a shared bank account accessed by two users through different transaction interfaces:

- **Person 1 — ATM:** Performs withdrawals.
- **Person 2 — UPI:** Performs payments.
- **Joint Account:** Supports deposits, balance checking, and account reset.

The application demonstrates how multiple threads access shared data and how mutex locks help prevent inconsistent account balance updates. It also includes a controlled race-condition demonstration using a separate account, so the experiment does not modify the real simulated joint-account balance.

JointBank includes a graphical interface built with Python Tkinter and email notifications sent to both configured joint account members through Gmail SMTP.

> **Disclaimer:** JointBank is an educational simulator. It is not connected to real bank accounts, ATMs, or UPI services.

## Features

- ATM withdrawals and UPI payments.
- Joint account deposits.
- Shared balance display and account reset.
- Concurrent ATM and UPI transaction testing.
- Mutex synchronization for normal transactions.
- Controlled race-condition demonstration.
- Transaction activity logging.
- Race-condition monitoring based on transaction logs.
- Gmail email notifications for successful and failed transactions.
- Simulation alerts for detected race conditions.
- Background email delivery to keep the graphical interface responsive.
- Environment-based configuration for Gmail credentials.

## Operating Systems Concepts

### 1. Multithreading

ATM and UPI transactions can execute in separate Python threads, demonstrating concurrent execution.

### 2. Shared Resource

The `BankAccount` object stores the balance accessed by both transaction interfaces.

### 3. Critical Section

The balance check and update form the critical section because multiple threads must not modify the shared account inconsistently.

### 4. Mutex Synchronization

A `threading.Lock` protects normal balance operations and ensures mutual exclusion while the critical section is being executed.

### 5. Race Condition

A race condition can occur when multiple threads access and modify shared data without suitable synchronization. JointBank demonstrates this behaviour through a controlled experiment using a separate demonstration account.

### 6. Transaction Monitoring

The transaction logger records events, while the transaction monitor analyses them to identify the expected race-condition pattern.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| `threading` | Concurrent transaction and background execution |
| `threading.Lock` | Mutual exclusion |
| Tkinter | Graphical user interface |
| `smtplib` | Gmail SMTP communication |
| `email.message.EmailMessage` | Email composition |
| `python-dotenv` | Loading local environment configuration |
| Gmail SMTP | Email notifications |

## Project Structure

```text
ATM_Cash_Withdrawal_Simulator/
├── .gitignore
├── .env                 # Local credentials; do not commit
├── README.md
├── requirements.txt
├── docs/
├── tests/
├── src/
│   ├── account.py
│   ├── atm.py
│   ├── gui.py
│   ├── logger.py
│   ├── main.py
│   ├── monitor.py
│   └── notifier.py
└── frontend/
```

The `frontend/` directory is included in the repository structure if present in your local project. The main Python simulator is launched from `src/gui.py`.

## Requirements

- Python 3.11 or a compatible Python version.
- Git.
- Internet access for Gmail email notifications.
- A Gmail account configured for App Password authentication if email notifications are required.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SnehaGEE/ATM_Cash_Withdrawal_Simulator.git
cd ATM_Cash_Withdrawal_Simulator
```

### 2. Create a virtual environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the appropriate activation method for your system or run the virtual environment's Python executable directly.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

The project uses `python-dotenv` to load the local Gmail configuration.

## Gmail Email Configuration

JointBank can send transaction notifications to two configured joint account members.

### 1. Enable 2-Step Verification

Enable 2-Step Verification on the Gmail account that will send notifications.

### 2. Generate an App Password

Open the official Google App Passwords page:

https://myaccount.google.com/apppasswords

Generate an App Password for JointBank if your Google account supports this feature.

### 3. Create the `.env` file

Create a file named `.env` in the project root, alongside `README.md` and `requirements.txt`.

Add the following configuration, replacing the placeholders with your own values:

```dotenv
GMAIL_ADDRESS=your_sender@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
JOINT_MEMBER_1_EMAIL=person1@example.com
JOINT_MEMBER_2_EMAIL=person2@example.com
```

Use the 16-character App Password generated by Google, not your normal Gmail sign-in password. You can enter the App Password without spaces.

### 4. Protect your credentials

Ensure `.gitignore` contains:

```gitignore
.env
.env.*
!.env.example
```

**Never commit your actual `.env` file or Gmail App Password to GitHub.** The repository should contain only placeholders and setup instructions, never private credentials.

Email delivery requires valid configuration, successful Gmail authentication, and network connectivity. If email delivery fails, the application logs the error; a completed transaction is not reversed because of email failure.

## Running the Application

Activate the virtual environment, open the project root in your terminal, and run:

```powershell
python -u src/gui.py
```

The JointBank graphical interface should open.

## How to Use JointBank

### ATM Withdrawal

1. Enter the withdrawal amount in the Person 1 ATM section.
2. Click **PROCESS TRANSACTION**.
3. The application checks the available balance and processes the withdrawal using mutex synchronization.
4. The interface displays the transaction result and updated balance.
5. Both configured members receive an email notification when delivery succeeds.

### UPI Payment

1. Enter the payment amount in the Person 2 UPI section.
2. Click **PROCESS TRANSACTION**.
3. The payment is processed against the shared account balance.
4. The interface displays the result, and the notification is sent to both configured recipients.

### Joint Account Deposit

1. Enter a positive deposit amount.
2. Click **DEPOSIT**.
3. The account balance is increased and a transaction notification is prepared.

### Concurrent Transaction Test

Click **RUN CONCURRENT TEST** to execute an ATM withdrawal and UPI payment concurrently with mutex synchronization. The application displays the results of both transactions and the resulting account balance.

### Race-Condition Demonstration

Click **RUN RACE-CONDITION DEMO** to run the controlled unsynchronized transaction experiment.

The demonstration starts with a separate simulated account and attempts an ATM withdrawal of ₹7,000 and a UPI payment of ₹5,000 from an initial balance of ₹10,000. The application analyses the transaction log and displays the detection result.

If the expected race-condition pattern is detected, JointBank sends a clearly labelled simulation alert. The real simulated joint-account balance is separate and is not changed by the demonstration.

### Other Controls

- **CHECK BALANCE:** Displays the current joint-account balance.
- **RESET ACCOUNT:** Resets the simulated account to the entered non-negative initial balance.

## Testing

The following scenarios have been tested during development:

| Test scenario | Expected behaviour |
|---|---|
| Successful ATM withdrawal | Balance decreases and a success notification is sent |
| Successful UPI payment | Balance decreases and a success notification is sent |
| Joint account deposit | Balance increases and a notification is sent |
| Withdrawal exceeding available balance | Transaction is rejected and a failure notification is sent |
| Concurrent ATM and UPI transactions | Mutex protects normal balance operations |
| Race-condition demonstration | Monitor analyses the log and reports the detection result |
| Race-condition notification | A simulation alert is sent when the condition is detected |
| Email delivery to joint members | Both configured recipients receive notifications |

Email delivery was verified during development for successful ATM and UPI transactions and the race-condition demonstration. Successful and failed transaction notifications were also tested.

## Limitations

- This is a simulation, not a production banking application.
- Account balances are maintained in memory and are not persisted to a banking database.
- The project does not connect to real ATMs, bank accounts, or UPI services.
- Email notifications depend on Gmail configuration, authentication, and network connectivity.
- The application does not provide production-grade banking authentication, fraud prevention, or financial infrastructure.

## Future Enhancements

- Store account and transaction data in a database.
- Add account login and role-based access.
- Support multiple simulated joint accounts.
- Add transaction-history export and audit reports.
- Implement email delivery retry handling and delivery-status tracking.
- Expand automated concurrency tests and synchronization comparisons.

## Security Notes

- Keep `.env` private and excluded from Git tracking.
- Never publish your Gmail App Password.
- If an App Password has previously been exposed or committed, revoke it and generate a replacement.
- Use a separate test Gmail account for demonstrations where practical.
- Do not use this educational simulator for real financial transactions.

## Author and Project Information

**Project:** JointBank — Shared Account Simulator  
**Domain:** Operating Systems  
**Language:** Python  
**Core concepts:** Multithreading, mutex synchronization, critical sections, race conditions, and shared-resource management.

## References

- Python threading documentation: https://docs.python.org/3/library/threading.html
- Python Tkinter documentation: https://docs.python.org/3/library/tkinter.html
- Python SMTP client documentation: https://docs.python.org/3/library/smtplib.html
- Python email message documentation: https://docs.python.org/3/library/email.message.html
- python-dotenv documentation: https://saurabh-kumar.com/python-dotenv/
