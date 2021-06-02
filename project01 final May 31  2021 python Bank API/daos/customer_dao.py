from abc import ABC, abstractmethod
from entities.customers import Customer


class CustomerDao(ABC):

    @abstractmethod
    def create_customer(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def get_all_customer(self) -> [Customer]:
        pass

    @abstractmethod
    def get_customer_with_id(self, customer_id: int) -> Customer:
        pass

    @abstractmethod
    def update_customer(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def delete_customer_with_id(self, customer_id: int) -> bool:
        pass
