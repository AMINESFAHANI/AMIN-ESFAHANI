import logging

from flask import Flask, request
from routes.bank_account_rout import account_create_rout
from routes.customer_rout import customer_create_rout

app: Flask = Flask(__name__)


@app.get("/hello")
def hello():
    return "hello"


logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
customer_create_rout(app)
account_create_rout(app)

if __name__ == '__main__':
    app.run()
