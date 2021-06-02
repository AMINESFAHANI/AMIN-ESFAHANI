from abc import ABC, abstractmethod
from entities.bank_accounts import BankAccount


class BankAccountDao(ABC):

    @abstractmethod
    def create_bank_account(self, bank_account: BankAccount) -> BankAccount:
        pass

    @abstractmethod
    def get_all_bank_account_by_customer_id(self, customer_id: int) -> list[BankAccount]:
        pass

    @abstractmethod
    def get_bank_accounts_by_customer_id_and_range(self, customer_id: int, lower: int, grater: int) -> [BankAccount]:
        pass

    @abstractmethod
    def get_bank_account_by_customer_id_and_bank_account_id(self, customer_id: int, account_id: int) -> BankAccount:
        pass

    @abstractmethod
    def update_bank_account_by_customer_id_and_bank_account_id(self, account: BankAccount, customer_id: int,
                                                               account_id: int) -> BankAccount:
        pass

    @abstractmethod
    def delete_bank_account_by_customer_id_and_bank_account_id(self, customer_id: int, account_id: int) -> bool:
        pass

    @abstractmethod
    def delete_bank_account_by_customer_id(self, customer_id: int) -> bool:
        pass

    @abstractmethod
    def get_bank_account_by_bank_account_id(self, account_id: int) -> BankAccount:
        pass

    @abstractmethod
    def update_balance_bank_account_by_bank_account_id(self, balance: int, account_id: int):
        pass
