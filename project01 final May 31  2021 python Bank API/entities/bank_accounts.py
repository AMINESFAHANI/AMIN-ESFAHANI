class BankAccount:

    # variables and functions should be in snake case.
    # classes should be in title case.
    def __init__(self, account_id: int, account_type: str, balance: int, customer_id: int):
        self.account_id = account_id
        self.account_type = account_type
        self.balance = balance
        self.customer_id = customer_id

    # json files should be camelcase.
    def __str__(self):
        return f"account_id={self.account_id},account_type={self.account_type},balance={self.balance}, customer_id={self.account_id}"


    def serialized(self) -> dict:
        return {"accountId": self.account_id,
                "accountType": self.account_type,
                "balance": self.balance,
                "customerId": self.customer_id}

    @staticmethod
    def deserialized(dic: dict):
        bank_account = BankAccount(0, "", 0, 0)
        bank_account.account_id = dic["accountId"]
        bank_account.account_type = dic["accountType"]
        bank_account.balance = dic["balance"]
        bank_account.customer_id = dic["customerId"]
        return bank_account
