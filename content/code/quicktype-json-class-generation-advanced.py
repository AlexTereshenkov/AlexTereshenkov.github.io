import requests
from typing import Optional
from datetime import datetime
from dateutil import parser


class Page:
    id: Optional[str]
    name: Optional[str]
    url: Optional[str]
    time_zone: Optional[str]
    updated_at: Optional[datetime]

    def __init__(self, id: Optional[str], name: Optional[str], url: Optional[str],
                 time_zone: Optional[str], updated_at: Optional[str]):
        self.id = id
        self.name = name
        self.url = url
        self.time_zone = time_zone
        self.updated_at = parser.parse(updated_at)


class Status:
    indicator: Optional[str]
    description: Optional[str]

    def __init__(self, indicator: Optional[str], description: Optional[str]):
        self.indicator = indicator
        self.description = description


class System:
    page: Optional[Page]
    status: Optional[Status]

    def __init__(self, data):
        self.page = Page(**data['page'])
        self.status = Status(**data['status'])


data = requests.get('https://s2k7tnzlhrpw.statuspage.io/api/v2/status.json').json()
system = System(data)
status = system.status.description
updated_at = system.page.updated_at.strftime('%d/%m/%Y')
print(f"Status: {status}\nUpdated at: {updated_at}")
