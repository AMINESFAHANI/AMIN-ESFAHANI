from daos.customer_dao import CustomerDao

from daos.customer_dao_postgres import CustomerDaoPostgres

from entities.customers import Customer
from exceptions.ResourceNotFoundError import ResourceNotFoundError

customer_dao: CustomerDao = CustomerDaoPostgres()
test_customer = Customer(0, "John Corly")


class TestCustomerDao:

    def test_create_customer(self):
        customer_dao.create_customer(test_customer)
        assert test_customer.customer_id != 0

    def test_get_all_customer(self):
        customers1 = customer_dao.get_all_customer()
        test_customer1 = Customer(0, "Jim Corly")
        test_customer2 = Customer(0, "eric scott")
        customer_dao.create_customer(test_customer1)
        customer_dao.create_customer(test_customer2)
        customers2 = customer_dao.get_all_customer()
        assert len(customers2) - len(customers1) >= 2

    def test_get_customer_with_id(self):
        test_id_customer = customer_dao.get_customer_with_id(test_customer.customer_id)
        assert test_id_customer.customer_name == test_customer.customer_name

    def test_get_customer_with_id_1(self):
        try:
            customer_dao.get_customer_with_id(8.9)
        except ResourceNotFoundError as e:
            print(e)

    def test_update_customer(self):
        test_customer.customer_name = "kim harry"
        updated_customer = customer_dao.update_customer(test_customer)
        assert updated_customer.customer_name == test_customer.customer_name

    def test_delete_customer_with_id(self):
        result = customer_dao.delete_customer_with_id(test_customer.customer_id)
        assert result == True

    def test_delete_customer_with_id1(self):
        try:
            customer_dao.delete_customer_with_id(0)
        except ResourceNotFoundError as e:
            print(e)
