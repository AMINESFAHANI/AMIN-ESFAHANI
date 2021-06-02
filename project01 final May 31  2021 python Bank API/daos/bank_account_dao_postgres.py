from daos.bank_account_dao import BankAccountDao
from entities.bank_accounts import BankAccount
from exceptions.ResourceNotFoundError import ResourceNotFoundError
from utiles.connection_util import connection


class BankAccountDaoPostgres(BankAccountDao):

    def create_bank_account(self, bank_account: BankAccount) -> BankAccount:
        sql = """insert into bank_account (account_type,balance,customer_id) values (%s,%s,%s) RETURNING account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, [bank_account.account_type, bank_account.balance, bank_account.customer_id])
        connection.commit()
        bank_account.account_id = cursor.fetchone()[0]
        return bank_account

    def get_all_bank_account_by_customer_id(self, customer_id: int) -> [BankAccount]:
        sql = """select * from bank_account where customer_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id])
        records = cursor.fetchall()
        accounts = [BankAccount(*record) for record in records]
        if len(accounts) == 0:
            raise ResourceNotFoundError
        return accounts

    def get_bank_accounts_by_customer_id_and_range(self, customer_id: int, lower: int, grater: int) -> [BankAccount]:
        sql = """select * from bank_account where customer_id = %s and balance between %s and %s """
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id, lower, grater])
        records = cursor.fetchall()
        accounts = [BankAccount(*record) for record in records]
        if len(accounts) == 0:
            raise ResourceNotFoundError
        return accounts

    def get_bank_account_by_customer_id_and_bank_account_id(self, customer_id: int, account_id: int) -> BankAccount:
        sql = """select * from bank_account where customer_id = %s and account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id, account_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError
        account = BankAccount(*record)
        return account

    def update_bank_account_by_customer_id_and_bank_account_id(self, account: BankAccount, customer_id: int,
                                                               account_id: int) -> BankAccount:
        sql = """update bank_account set account_type = %s, balance = %s where account_id = %s and customer_id = %s returning account_id,customer_id ;"""
        cursor = connection.cursor()
        cursor.execute(sql, [account.account_type, account.balance, account_id, customer_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError
        account.account_id = record[0]
        account.customer_id = record[1]
        return account

    def delete_bank_account_by_customer_id_and_bank_account_id(self, customer_id: int, account_id: int) -> bool:
        sql = """delete from bank_account where customer_id = %s and account_id = %s returning account_id ;"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id, account_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError
        return True

    def delete_bank_account_by_customer_id(self, customer_id: int) -> bool:
        sql = """delete from bank_account where customer_id = %s ;"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id])
        connection.commit()
        return True

    def get_bank_account_by_bank_account_id(self, account_id: int) -> BankAccount:
        sql = """select * from bank_account where account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError
        account = BankAccount(*record)
        return account

    def update_balance_bank_account_by_bank_account_id(self, balance: int, account_id: int):
        sql = """update bank_account set balance = %s where account_id = %s returning account_id"""
        cursor = connection.cursor()
        cursor.execute(sql, [balance, account_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError
        return True
