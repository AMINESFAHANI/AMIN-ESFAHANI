class Customer:
    def __init__(self, customer_id: int, customer_name: str):
        self.customer_id = customer_id
        self.customer_name = customer_name

    def __str__(self):
        return f"customer_id={self.customer_id},customer_name={self.customer_name}"


    def serialized(self) -> dict:
        return {"customerId": self.customer_id, "customerName": self.customer_name}

    @staticmethod
    def deserialized(dic: dict):
        customer = Customer(0, "")
        customer.customer_id = dic["customerId"]
        customer.customer_name = dic["customerName"]
        return customer
