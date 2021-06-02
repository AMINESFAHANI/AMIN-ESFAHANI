from exceptions.ResourceNotFoundError import ResourceNotFoundError
from utiles.connection_util import connection
from daos.customer_dao import CustomerDao
from entities.customers import Customer


class CustomerDaoPostgres(CustomerDao):
    def create_customer(self, customer: Customer) -> Customer:
        sql = """insert into customer (customer_name) values (%s) RETURNING customer_id"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer.customer_name])
        connection.commit()
        customer.customer_id = cursor.fetchone()[0]
        return customer

    def get_all_customer(self) -> [Customer]:
        sql = """select * from customer"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        customers = [Customer(*record) for record in records]
        if len(customers) == 0:
            raise ResourceNotFoundError("There is not any customer in records")
        else:
            return customers


    def get_customer_with_id(self, customer_id: int) -> Customer:
        sql = """select * from customer where customer_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id])
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError
        else:
            customer = Customer(*record)
            return customer

    def update_customer(self, customer: Customer) -> Customer:
        sql = """update customer set customer_name=%s where customer_id =%s"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer.customer_name, customer.customer_id])
        connection.commit()
        return customer

    def delete_customer_with_id(self, customer_id: int) -> bool:
        sql = """delete from customer where customer_id =%s"""
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id])
        connection.commit()
        return True
