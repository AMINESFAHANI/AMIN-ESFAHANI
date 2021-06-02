from daos.bank_account_dao import BankAccountDao
from daos.bank_account_dao_postgres import BankAccountDaoPostgres
from daos.customer_dao import CustomerDao
from daos.customer_dao_postgres import CustomerDaoPostgres
from entities.bank_accounts import BankAccount
from entities.customers import Customer
from exceptions.ResourceNotFoundError import ResourceNotFoundError

customer_dao: CustomerDao = CustomerDaoPostgres()
bank_account_dao: BankAccountDao = BankAccountDaoPostgres()

test_customer: Customer = Customer(0, "ali")
customer_dao.create_customer(test_customer)
test_bank_account: BankAccount = BankAccount(0, "saving", 1000, 0)


class TestBankAccountDao:

    def test_create_bank_account(self):
        test_bank_account.customer_id = test_customer.customer_id
        bank_account_dao.create_bank_account(test_bank_account)
        assert test_bank_account.account_id != 0

    def test_get_all_bank_account_by_customer_id(self):
        test_accounts = bank_account_dao.get_all_bank_account_by_customer_id(test_customer.customer_id)
        assert len(test_accounts) == 1

    def test_get_all_bank_account_by_customer_id_1(self):
        try:
            bank_account_dao.get_all_bank_account_by_customer_id(-10)
            assert False
        except ResourceNotFoundError:
            pass

    def test_get_bank_accounts_by_customer_id_and_range(self):
        test_accounts = bank_account_dao.get_bank_accounts_by_customer_id_and_range(test_customer.customer_id, 0, 1000)
        assert len(test_accounts) == 1

    def test_get_bank_accounts_by_customer_id_and_range_1(self):
        try:
            test_accounts = bank_account_dao.get_bank_accounts_by_customer_id_and_range(0, 0, 1000)
            assert False
        except ResourceNotFoundError:
            pass

    def test_get_bank_account_by_customer_id_and_bank_account_id(self):
        test_account = bank_account_dao.get_bank_account_by_customer_id_and_bank_account_id(test_customer.customer_id,
                                                                                            test_bank_account.account_id)
        assert test_account.balance == test_bank_account.balance

    def test_get_bank_account_by_customer_id_and_bank_account_id(self):
        try:
            bank_account_dao.get_bank_account_by_customer_id_and_bank_account_id(0, test_bank_account.account_id)
            assert False
        except ResourceNotFoundError:
            pass

    def test_update_bank_account_by_customer_id_and_bank_account_id(self):
        test_account = bank_account_dao.update_bank_account_by_customer_id_and_bank_account_id(test_bank_account,
                                                                                               test_customer.customer_id,
                                                                                               test_bank_account.account_id)
        assert test_account.balance == test_bank_account.balance

    def test_update_bank_account_by_customer_id_and_bank_account_id_1(self):
        try:
            bank_account_dao.update_bank_account_by_customer_id_and_bank_account_id(test_bank_account,
                                                                                    test_customer.customer_id, 0)
            assert False
        except ResourceNotFoundError:
            pass

    def test_get_bank_account_by_bank_account_id(self):
        test_account = bank_account_dao.get_bank_account_by_bank_account_id(test_bank_account.account_id)
        assert test_account.balance == test_bank_account.balance


    def test_update_balance_bank_account_by_bank_account_id(self):
        bank_account_dao.update_balance_bank_account_by_bank_account_id(test_bank_account.balance, test_bank_account.account_id)
        assert True

    def test_delete_bank_account_by_customer_id_and_bank_account_id(self):
        bank_account_dao.delete_bank_account_by_customer_id(test_bank_account.customer_id)
        assert True

