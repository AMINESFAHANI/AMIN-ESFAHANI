from daos.bank_account_dao import BankAccountDao
from daos.customer_dao import CustomerDao
from entities.bank_accounts import BankAccount
from exceptions.insufficient_budget import InsufficientBudget
from service.bank_account_service import BankAccountService


class BankAccountServiceImpl(BankAccountService):

    def __init__(self, bank_account_dao: BankAccountDao, customer_dao: CustomerDao):
        self.bank_account_dao = bank_account_dao
        self.customer_dao = customer_dao

    def register_bank_account_by_customer_id(self, bank_account: BankAccount, customer_id: int) -> BankAccount:
        self.customer_dao.get_customer_with_id(customer_id)
        bank_account.customer_id = customer_id
        return self.bank_account_dao.create_bank_account(bank_account)

    def retrieve_account_by_customer_id(self, customer_id: int) -> list[BankAccount]:
        self.customer_dao.get_customer_with_id(customer_id)
        return self.bank_account_dao.get_all_bank_account_by_customer_id(customer_id)

    def retrieve_accounts_by_customer_id_and_range(self, customer_id: int, lower: int, grater: int) -> [BankAccount]:
        self.customer_dao.get_customer_with_id(customer_id)
        return self.bank_account_dao.get_bank_accounts_by_customer_id_and_range(customer_id, lower, grater)

    def retrieve_account_by_customer_id_and_bank_account_id(self, customer_id: int, account_id: int) -> BankAccount:
        return self.bank_account_dao.get_bank_account_by_customer_id_and_bank_account_id(customer_id, account_id)

    def update_account_by_customer_id_and_bank_account_id(self, account: BankAccount, customer_id: int,
                                                          account_id: int) -> BankAccount:
        return self.bank_account_dao.update_bank_account_by_customer_id_and_bank_account_id(account, customer_id,
                                                                                            account_id)

    def remove_account_by_customer_id_and_bank_account_id(self, customer_id: int, account_id: int) -> bool:
        self.bank_account_dao.delete_bank_account_by_customer_id_and_bank_account_id(customer_id, account_id)

    def remove_account_by_customer_id(self, customer_id: int) -> bool:
        self.bank_account_dao.delete_bank_account_by_customer_id(customer_id)

    def transaction_account_by_customer_id_and_account_id(self, customer_id: int, account_id: int, withdraw: int,
                                                          deposit: int) -> BankAccount:
        account = self.bank_account_dao.get_bank_account_by_customer_id_and_bank_account_id(customer_id, account_id)
        if account.balance < (withdraw - deposit):
            raise InsufficientBudget
        account.balance += (deposit - withdraw)
        return self.bank_account_dao.update_bank_account_by_customer_id_and_bank_account_id(account, customer_id,
                                                                                            account_id)

    def transfer_amount_between_accounts_with_account_id(self, account1_id: int, account2_id: int,
                                                         amount: int):
        account1 = self.bank_account_dao.get_bank_account_by_bank_account_id(account1_id)
        account2 = self.bank_account_dao.get_bank_account_by_bank_account_id(account2_id)
        if account1.balance < amount:
            raise InsufficientBudget
        account1.balance -= amount
        account2.balance += amount
        self.bank_account_dao.update_balance_bank_account_by_bank_account_id(account1.balance, account1_id)
        self.bank_account_dao.update_balance_bank_account_by_bank_account_id(account2.balance, account2_id)
        return [account1, account2]
