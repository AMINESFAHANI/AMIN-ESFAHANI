from abc import ABC, abstractmethod
from entities.bank_accounts import BankAccount


class BankAccountService(ABC):

    @abstractmethod
    def register_bank_account_by_customer_id(self, bank_account: BankAccount, customer_id: int) -> BankAccount:
        pass

    @abstractmethod
    def retrieve_account_by_customer_id(self, customer_id: int) -> list[BankAccount]:
        pass

    @abstractmethod
    def retrieve_accounts_by_customer_id_and_range(self, customer_id: int, lower: int, grater: int) -> [BankAccount]:
        pass

    @abstractmethod
    def retrieve_account_by_customer_id_and_bank_account_id(self, customer_id: int, account_id: int) -> BankAccount:
        pass

    @abstractmethod
    def update_account_by_customer_id_and_bank_account_id(self, account: BankAccount, customer_id: int,
                                                          account_id: int) -> BankAccount:
        pass

    @abstractmethod
    def remove_account_by_customer_id_and_bank_account_id(self, customer_id: int, account_id: int) -> bool:
        pass

    @abstractmethod
    def remove_account_by_customer_id(self, customer_id: int) -> bool:
        pass

    @abstractmethod
    def transaction_account_by_customer_id_and_account_id(self, customer_id: int, account_id: int, withdraw: int,
                                                          deposit: int) -> BankAccount:
        pass

    @abstractmethod
    def transfer_amount_between_accounts_with_account_id(self, account1_id: int, account2_id: int, amount: int) -> [BankAccount]:
        pass
