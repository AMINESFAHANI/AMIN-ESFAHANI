from flask import Flask, request, jsonify, json

from daos.bank_account_dao import BankAccountDao
from daos.bank_account_dao_postgres import BankAccountDaoPostgres
from daos.customer_dao import CustomerDao

from daos.customer_dao_postgres import CustomerDaoPostgres
from entities.bank_accounts import BankAccount
from entities.customers import Customer
from exceptions.ResourceNotFoundError import ResourceNotFoundError
from exceptions.insufficient_budget import InsufficientBudget
from exceptions.value_type_error import TypeValueError
from service.bank_account_service import BankAccountService
from service.bank_account_service_impl import BankAccountServiceImpl
from service.customer_service import CustomerService
from service.customer_service_impl import CustomerServiceImpl

customer_dao: CustomerDao = CustomerDaoPostgres()
bank_account_dao: BankAccountDao = BankAccountDaoPostgres()
bank_account_service: BankAccountService = BankAccountServiceImpl(bank_account_dao, customer_dao)


def account_create_rout(app: Flask):
    @app.route("/account/<customer_id>", methods=["POST"])
    def post_account(customer_id: str):
        try:
            if not customer_id.isnumeric():
                raise TypeError(" The type of variable does not match.")
            bank_account = BankAccount.deserialized(request.json)
            bank_account_service.register_bank_account_by_customer_id(bank_account, int(customer_id))
            app.logger.info(f'new account registered with ID: {bank_account.account_id}')
            return jsonify(bank_account.serialized()), 201
        except TypeError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/accounts/<customer_id>", methods=["GET"])
    def get_accounts_by_customer_id(customer_id: str):
        try:
            if not customer_id.isnumeric():
                raise TypeValueError
            accounts = bank_account_service.retrieve_account_by_customer_id(int(customer_id))
            app.logger.info(f' all accounts with customer_id: {customer_id}')
            return jsonify([account.serialized() for account in accounts]), 200
        except TypeValueError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/accounts/customer_id:/<customer_id>/lower:/<lower>/grater:/<grater>", methods=["GET"])
    def get_accounts_by_customer_id_and_range(customer_id: str, lower: str, grater: str):
        try:
            if not (customer_id.isnumeric() and lower.isnumeric() and grater.isnumeric()):
                raise TypeValueError
            accounts = bank_account_service.retrieve_accounts_by_customer_id_and_range(int(customer_id), int(lower),
                                                                                       int(grater))
            app.logger.info(f' all accounts with customer_id: {customer_id} and range between {lower} and {grater}')
            return jsonify([account.serialized() for account in accounts]), 200
        except TypeValueError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/accounts/customer_id/<customer_id>/account_id/<account_id>", methods=["GET"])
    def get_accounts_by_customer_id_and_account_id(customer_id: str, account_id: str):
        try:
            if not (customer_id.isnumeric() and account_id.isnumeric()):
                raise TypeValueError
            account = bank_account_service.retrieve_account_by_customer_id_and_bank_account_id(int(customer_id),
                                                                                               int(account_id))
            app.logger.info(f' get account with customer_id: {customer_id} and account_id: {account_id}')
            return jsonify(account.serialized())
        except TypeValueError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/accounts/customer_id/<customer_id>/account_id/<account_id>", methods=["PUT"])
    def update_accounts_by_customer_id_and_account_id(customer_id: str, account_id: str):
        try:
            if not (customer_id.isnumeric() and account_id.isnumeric()):
                raise TypeValueError
            account = BankAccount.deserialized(request.json)
            account = bank_account_service.update_account_by_customer_id_and_bank_account_id(account, int(customer_id),
                                                                                             int(account_id))
            app.logger.info(f' get account with customer_id: {customer_id} and account_id: {account_id}')
            return jsonify(account.serialized())
        except TypeValueError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/accounts/customer_id/<customer_id>/account_id/<account_id>", methods=["DELETE"])
    def delete_accounts_by_customer_id_and_account_id(customer_id: str, account_id: str):
        try:
            if not (customer_id.isnumeric() and account_id.isnumeric()):
                raise TypeValueError
            bank_account_service.remove_account_by_customer_id_and_bank_account_id(int(customer_id),
                                                                                   int(account_id))
            app.logger.info(f' deleted account with customer_id: {customer_id} and account_id: {account_id}')
            return f'account with customer_id: {customer_id} and account_id: {account_id} was deleted successfully'
        except TypeValueError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/accounts/customer_id/<customer_id>/account_id/<account_id>", methods=["PATCH"])
    def transaction_account_by_customer_id_and_account_id(customer_id: str, account_id: str):
        try:
            if not (customer_id.isnumeric() and account_id.isnumeric()):
                raise TypeValueError
            body = request.json
            deposit = withdraw = 0
            if "deposit" in body:
                deposit = int(body["deposit"])
            if "withdraw" in body:
                withdraw = int(body["withdraw"])
            account = bank_account_service.transaction_account_by_customer_id_and_account_id(int(customer_id),
                                                                                   int(account_id), withdraw, deposit)

            app.logger.info(
                f' transaction happened in  account with customer_id: {customer_id} and account_id: {account_id}')
            return jsonify(account.serialized())
        except TypeValueError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404
        except InsufficientBudget as e:
            return str(e), 402

    @app.route("/accounts/account1_id/<account1_id>/account2_id/<account2_id>", methods=["PATCH"])
    def transfer_amount_between_accounts_by_account_id(account1_id: str, account2_id: str):
        try:
            if not (account1_id.isnumeric() and account2_id.isnumeric()):
                raise TypeValueError
            body = request.json
            amount = body["amount"]
            res = bank_account_service.transfer_amount_between_accounts_with_account_id(int(account1_id),
                                                                                        int(account2_id), int(amount))

            app.logger.info(
                f' transformation happened in  accounts with account1_id: {account1_id} and account2_id: {account2_id}')
            return jsonify([account.serialized() for account in res])
        except TypeValueError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404
        except InsufficientBudget as e:
            return str(e), 422
