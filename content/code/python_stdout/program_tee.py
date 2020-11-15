import sys
from io import StringIO


class StdOutTee:
    def __init__(self, *authors):
        self.authors = authors

    def write(self, text):
        for author in self.authors:
            author.write(text)


print("Started script")

# to capture anything that will be written to the stdout
buf = StringIO()
stdout = sys.stdout
sys.stdout = StdOutTee(buf, stdout)

print('Getting work done 1')
print('Getting work done 2')

sys.stdout = stdout
# collecting what has been written into a variable
captured = buf.getvalue()

print("Finished script\n")

print(captured)