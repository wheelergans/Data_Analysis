import os

path = input("Enter Serial log path: ")

with open(path) as infile:
    for line in infile.readlines():
        if "ERROR" in line:
            print(line)

print("complete")
