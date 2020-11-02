from pathlib import Path

CITY = None


def fetch(query):
    return


# class db:
#     @staticmethod
#     def get(value):
#         return


def validate_input(object_type, value):
    return


def get_customers(city: str):
    validate_input(object_type=CITY, value=city)
    customers = fetch(query=f'customers;city={city}')
    return customers
