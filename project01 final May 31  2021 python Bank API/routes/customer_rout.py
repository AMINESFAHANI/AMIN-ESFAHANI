from flask import Flask, request, jsonify, json
from daos.bank_account_dao import BankAccountDao
from daos.bank_account_dao_postgres import BankAccountDaoPostgres
from daos.customer_dao import CustomerDao
from daos.customer_dao_postgres import CustomerDaoPostgres
from entities.customers import Customer
from exceptions.ResourceNotFoundError import ResourceNotFoundError
from exceptions.value_type_error import TypeValueError
from service.bank_account_service import BankAccountService
from service.bank_account_service_impl import BankAccountServiceImpl
from service.customer_service import CustomerService
from service.customer_service_impl import CustomerServiceImpl

customer_dao: CustomerDao = CustomerDaoPostgres()
customer_service: CustomerService = CustomerServiceImpl(customer_dao)

bank_account_dao: BankAccountDao = BankAccountDaoPostgres()
bank_account_service: BankAccountService = BankAccountServiceImpl(bank_account_dao, customer_dao)


def customer_create_rout(app: Flask):
    @app.route('/customer', methods=['POST'])
    def post_customer():
        customer = Customer.deserialized(request.json)
        customer_service.register_customer(customer)
        app.logger.info(f'new customer registered ID: {customer.customer_id}')
        return jsonify(customer.serialized()), 201

    @app.route('/customer', methods=['GET'])
    def get_all_customer():
        try:
            customers = customer_service.retrieve_all_customer()
            app.logger.info(f' all customers ')
            return jsonify([customer.serialized() for customer in customers]), 200
        except ResourceNotFoundError as e:
            return str(e)

    @app.route("/customer/<customer_id>", methods=["GET"])
    def get_customer_by_id(customer_id: str):

        try:
            if not customer_id.isnumeric():
                raise TypeValueError
            customer = customer_service.retrieve_customer_with_id(int(customer_id))
            app.logger.info(f'get customer by ID: {customer.customer_id}')
            return jsonify(customer.serialized())
        except TypeValueError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/customer/<customer_id>", methods=["PUT"])
    def update_customer_by_id(customer_id):

        try:
            if not customer_id.isnumeric():
                raise TypeValueError
            customer_service.retrieve_customer_with_id(int(customer_id))
            customer = Customer.deserialized(request.json)
            customer.customer_id = int(customer_id)
            customer = customer_service.update_customer(customer)
            app.logger.info(f'updated customer by ID: {customer.customer_id}')
            return jsonify(customer.serialized())
        except TypeValueError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/customer/customer_id/<customer_id>", methods=["DELETE"])
    def delete_customer_by_id(customer_id: str):

        try:
            if not customer_id.isnumeric():
                raise TypeValueError
            bank_account_service.remove_account_by_customer_id(int(customer_id))
            if not customer_id.isnumeric():
                raise TypeValueError
            customer_service.remove_customer_with_id(int(customer_id))
            app.logger.info(f'deleted customer by ID: {int(customer_id)}')
            return f"Customer with ID: {int(customer_id)} Was Deleted successfully", 205
        except TypeValueError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404
