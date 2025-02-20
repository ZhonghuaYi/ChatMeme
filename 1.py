import os

file = "data/index1.txt"
file1 = "data/database1.txt"

with open(file, "r") as f:
    lines = [line.strip() for line in f.readlines()]
    # remove empty lines
    lines = [line for line in lines if line]

with open(file1, "r") as f:
    lines1 = [line.strip() for line in f.readlines()]
    # remove empty lines
    lines1 = [line for line in lines1 if line]

print(len(lines))
print(len(lines1))

print(lines[:3])
print(lines1[:3])


