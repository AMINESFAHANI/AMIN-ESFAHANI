from abc import ABC, abstractmethod
from entities.customers import Customer


class CustomerService(ABC):

    @abstractmethod
    def register_customer(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def retrieve_all_customer(self) -> [Customer]:
        pass

    @abstractmethod
    def retrieve_customer_with_id(self, customer_id: int) -> Customer:
        pass

    @abstractmethod
    def update_customer(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def remove_customer_with_id(self, customer_id: int) -> bool:
        pass
