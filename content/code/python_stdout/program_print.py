import sys

# keeping the original reference to the output destination
stdout = sys.stdout

print("Started script")

# redirecting the print statements to the file
f = open('log.txt', 'a')
sys.stdout = f

# main program execution, gets logged to a file
print("Getting work done")

# setting it to the original output destination
sys.stdout = stdout
f.close()

print("Finished script")
