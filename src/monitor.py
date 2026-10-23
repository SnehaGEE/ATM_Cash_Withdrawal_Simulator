
import re


class TransactionMonitor:
    def __init__(self, account):
        self.account = account

    def analyze(self):
        logs = self.account.logger.get_logs()

        reads = {}
        updates = {}
        successful = set()

        for line in logs:
            user = None

            if "ATM 1 →" in line:
                user = "ATM 1"
            elif "UPI User 2 →" in line:
                user = "UPI User 2"
            elif "ATM 2 →" in line:
                user = "ATM 2"

            if user is None:
                continue

            # Example: Balance read: ₹10000
            read_match = re.search(
                r"Balance read:\s*₹?\s*([\d,]+)",
                line
            )

            if read_match:
                reads[user] = int(
                    read_match.group(1).replace(",", "")
                )

            # Example: Balance updated: ₹10000 → ₹3000
            update_match = re.search(
                r"Balance updated:\s*₹?\s*([\d,]+)"
                r"\s*→\s*₹?\s*([\d,]+)",
                line
            )

            if update_match:
                old_balance = int(
                    update_match.group(1).replace(",", "")
                )
                new_balance = int(
                    update_match.group(2).replace(",", "")
                )

                updates[user] = (old_balance, new_balance)

            if "Withdrawal successful:" in line:
                successful.add(user)

        # Compare transactions that read the same original balance.
        for user_a, balance_a in reads.items():
            for user_b, balance_b in reads.items():

                if user_a == user_b:
                    continue

                if balance_a != balance_b:
                    continue

                if not (
                    user_a in successful
                    and user_b in successful
                    and user_a in updates
                    and user_b in updates
                ):
                    continue

                old_a, new_a = updates[user_a]
                old_b, new_b = updates[user_b]

                if old_a == balance_a and old_b == balance_b:
                    evidence = [
                        f"{user_a} read ₹{balance_a:,}.",
                        f"{user_b} read ₹{balance_b:,}.",
                        f"{user_a} updated ₹{old_a:,} → ₹{new_a:,}.",
                        f"{user_b} updated ₹{old_b:,} → ₹{new_b:,}.",
                        "Both withdrawals succeeded using the same original balance.",
                        "One update overwrote the other."
                    ]

                    return {
                        "status": "RACE CONDITION CONFIRMED",
                        "race_condition": True,
                        "message": (
                            "A lost-update race condition was detected."
                        ),
                        "evidence": evidence
                    }

        return {
            "status": "NO RACE CONDITION DETECTED",
            "race_condition": False,
            "message": (
                "No lost update was identified in the available logs."
            ),
            "evidence": []
        }
