from datetime import datetime


class Client:
    def __init__(self, guid):
        self.guid = guid
        self.visited = False
        self.last_time_visited = None

    def visit(self):
        self.visited = True
        self.last_time_visited = datetime.now()

    def process(self):
        self.visit()
