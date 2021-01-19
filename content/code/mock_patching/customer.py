from typing import List


class City:
    def __init__(self, name: str):
        self.name = name


class Address:
    def __init__(self, address: List[str]):
        self.city = City(address[0])
        self.street = address[1]
        self.house = address[2]


class Customer:
    def __init__(self, address: List[str]):
        self.address = Address(str)

    def get_address(self):
        return self.address
