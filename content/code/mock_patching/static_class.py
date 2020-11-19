from typing import Tuple


class Address:

    def __init__(self, house: str, street: str, postal_code: str, city: str):
        self.house = Address.numerize(house)
        self.street = street
        self.postal_code = postal_code
        self.city = city

    @classmethod
    def from_tuple(cls, *address_tuple: Tuple):
        return Address(*address_tuple)

    @staticmethod
    def numerize(value):
        return int(value)

    def to_string(self):
        return f"{self.house}{self.street}\n{self.postal_code}\n{self.city}"

    def print(self):
        fmt = self.to_string()
        print(fmt)
        return fmt

def is_valid_address(address_tuple):
    try:
        Address.from_tuple(*address_tuple)
        return True
    except Exception:
        return False
