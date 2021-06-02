from daos.customer_dao import CustomerDao
from entities.customers import Customer
from exceptions.ResourceNotFoundError import ResourceNotFoundError


class CustomerDaoLocal(CustomerDao):
    id_maker = 0
    customer_table = {}

    def create_customer(self, customer: Customer) -> Customer:
        CustomerDaoLocal.id_maker += 1
        customer.customer_id = CustomerDaoLocal.id_maker
        CustomerDaoLocal.customer_table[customer.customer_id] = customer
        return customer

    def get_all_customer(self) -> [Customer]:
        customer_list = list(CustomerDaoLocal.customer_table.values())
        return customer_list

    def get_customer_with_id(self, customer_id: int) -> Customer:
        try:
            customer = CustomerDaoLocal.customer_table[customer_id]
            return customer
        except KeyError:
            raise ResourceNotFoundError(f"Could not find customer of id {customer_id}")

    def update_customer(self, customer_id: int) -> Customer:
        try:
            customer = CustomerDaoLocal.customer_table[customer_id]
            return customer
        except KeyError:
            raise ResourceNotFoundError(f"Could not find customer of id {customer_id}")

    def delete_customer_with_id(self, customer_id: int) -> bool:
        try:
            del CustomerDaoLocal.customer_table[customer_id]
            return True
        except KeyError:
            raise ResourceNotFoundError(f"Could not find customer of id {customer_id}")
