from unittest.mock import MagicMock

from daos.bank_account_dao import BankAccountDao
from daos.bank_account_dao_postgres import BankAccountDaoPostgres
from daos.customer_dao import CustomerDao
from daos.customer_dao_postgres import CustomerDaoPostgres
from entities.bank_accounts import BankAccount
from entities.customers import Customer
from exceptions.ResourceNotFoundError import ResourceNotFoundError
from service.bank_account_service import BankAccountService
from service.bank_account_service_impl import BankAccountServiceImpl

customer_dao: CustomerDao = CustomerDaoPostgres()
bank_account_dao: BankAccountDao = BankAccountDaoPostgres()
bank_account_service: BankAccountService = BankAccountServiceImpl(bank_account_dao, customer_dao)

test_customer: Customer = Customer(0, "ali")
customer_dao.create_customer(test_customer)
test_bank_account: BankAccount = BankAccount(0, "saving", 1000, test_customer.customer_id)
bank_account_dao.create_bank_account(test_bank_account)
bank_account_dao.get_bank_account_by_customer_id_and_bank_account_id = MagicMock(return_value=test_bank_account)


class TestBankAccountService:
    def test_transaction_account_by_customer_id_and_account_id(self):
        account = bank_account_service.transaction_account_by_customer_id_and_account_id(test_bank_account.customer_id,
                                                                                         test_bank_account.account_id,
                                                                                         0, 1000)
        assert account.balance == test_bank_account.balance

    def test_transaction_account_by_customer_id_and_account_id_1(self):
        try:
            bank_account_service.transaction_account_by_customer_id_and_account_id(0, test_bank_account.account_id, 0,
                                                                                   1000)

            assert False
        except ResourceNotFoundError:
            pass

    def test_transfer_amount_between_accounts_with_account_id(self):
        account1 = bank_account_dao.create_bank_account(test_bank_account)
        account2 = bank_account_dao.create_bank_account(test_bank_account)
        print(account1)
        print(account2)
        accounts = bank_account_service.transfer_amount_between_accounts_with_account_id(account1.account_id,
                                                                                         account2.account_id,
                                                                                         10)
        assert (accounts[1].balance - account1.balance) == 10

    def test_transfer_amount_between_accounts_with_account_id_1(self):
        try:
            bank_account_service.transfer_amount_between_accounts_with_account_id(0, test_bank_account.account_id,
                                                                                  1000)

            assert False
        except ResourceNotFoundError:
            pass
