from daos.customer_dao import CustomerDao
from entities.customers import Customer
from service.customer_service import CustomerService


class CustomerServiceImpl(CustomerService):

    def __init__(self, customer_dao: CustomerDao):
        self.customer_dao = customer_dao

    def register_customer(self, customer: Customer) -> Customer:
        return self.customer_dao.create_customer(customer)

    def retrieve_all_customer(self) -> [Customer]:
        return self.customer_dao.get_all_customer()

    def retrieve_customer_with_id(self, customer_id: int) -> Customer:
        return self.customer_dao.get_customer_with_id(customer_id)

    def update_customer(self, customer: Customer) -> Customer:
        return self.customer_dao.update_customer(customer)


    def remove_customer_with_id(self, customer_id: int) -> bool:
        self.customer_dao.get_customer_with_id(customer_id)
        self.customer_dao.delete_customer_with_id(customer_id)
        return True
