import sys
from io import StringIO

print("Started script")

# to capture anything that will be written to the stdout
buf = StringIO()
stdout = sys.stdout
sys.stdout = buf

print('Getting work done')

sys.stdout = stdout
# collecting what has been written into a variable
captured = buf.getvalue()

print("Finished script\n")
print(captured)
