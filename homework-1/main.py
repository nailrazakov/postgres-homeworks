"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import csv
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv('key')

employees_list = []
customers_list = []
orders_list = []
with open('north_data/customers_data.csv', 'r') as csvfile:
    customers = list(csv.DictReader(csvfile))
    for item in customers:
        customers_list.append((item['customer_id'], item['company_name'], item['contact_name']))
with open('north_data/employees_data.csv', 'r') as csvfile:
    employees = list(csv.DictReader(csvfile))
    for item in employees:
        employees_list.append((int(item['employee_id']), item['first_name'], item['last_name'],
                               item['title'], item['birth_date'], item['notes']))
with open('north_data/orders_data.csv', 'r') as csvfile:
    orders = list(csv.DictReader(csvfile))
    for item in orders:
        orders_list.append((int(item["order_id"]), item["customer_id"], int(item["employee_id"]), item["order_date"],
                            item["ship_city"]))

conn = psycopg2.connect(host="localhost", database="north", user="postgres",
                        password=key)

try:
    with conn:
        with conn.cursor() as curs:
            curs.executemany('INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)',
                             employees_list)
            curs.executemany('INSERT INTO customers VALUES (%s, %s, %s)', customers_list)
            curs.executemany('INSERT INTO orders VALUES (%s, %s, %s, %s, %s)', orders_list)
finally:
    conn.close()
