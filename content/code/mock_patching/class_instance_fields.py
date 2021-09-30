# country:capital mapping
countries_capitals = {"France": "Paris"}


class City:
    def __init__(self, name: str):
        self.name = name


def get_capital(country: str):
    city = get_city(countries_capitals.get(country))
    return city.name


def get_city(name: str):
    return City(name)
