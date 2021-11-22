import sys

with open(sys.argv[1], "r") as f:
    instructions = f.readlines()
    for i in instructions[2:]:
        print("{0:032b}".format(int(i[2:-1], 16)))
