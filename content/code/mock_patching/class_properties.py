class Process:
    def __init__(self, pid: int):
        self._pid = pid

    @property
    def pid(self):
        return self._pid

    def as_string(self):
        return f'Process({self.pid})'
