import os
import sys
import random


def generate():
    n = 1000
    input_data = ""
    ans = ""
    for _ in range(n):
        num1 = random.randint(0, 1024)
        op = random.randint(0, 4)
        num2 = random.randint(0, 1024)
        input_data += f"{num1} {op} {num2}\n"
        if op == 0:
            ans += f"{num1+num2}\n"
        elif op == 1:
            ans += f"{num1-num2}\n"
        elif op == 2:
            ans += f"{num1*num2}\n"
        elif op == 3:
            if num2 == 0:
                ans += "division by zero\n"
            else:
                ans += f"{num1//num2}\n"
        else:
            if num2 == 0:
                ans += "remainder by zero\n"
            else:
                ans += f"{num1%num2}\n"
    for num in range(1, 12):
        num1 = num
        op = 6
        num2 = 0
        input_data += f"{num1} {op} {num2}\n"
        tmp = 1
        for i in range(1, num1 + 1):
            tmp *= i
        ans += f"{tmp}\n"
    for _ in range(50):
        num1 = random.randint(0, 1024)
        op = 5
        num2 = random.randint(0, 30)
        while num1 ** (num2) > 2147483647:
            num1 = random.randint(0, 1024)
            num2 = random.randint(0, 30)
        input_data += f"{num1} {op} {num2}\n"
        ans += f"{num1**num2}\n"
    input_data += "0 5 1024\n1 5 1024\n"
    ans += "0\n1\n"
    input_data += "123 3 0\n1 4 0\n"
    ans += "division by zero\nremainder by zero\n"
    return input_data, ans


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [name]")
        sys.exit(1)

    name = sys.argv[1]

    input_dir = "input"
    output_dir = "output"
    if not os.path.exists(input_dir):
        os.mkdir(input_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    input_path = os.path.join(input_dir, f"{name}.txt")
    output_path = os.path.join(output_dir, f"{name}.txt")

    if os.path.exists(input_path):
        print(f"The file {input_path} already exists!")
        sys.exit(1)
    if os.path.exists(output_path):
        print(f"The file {output_path} already exists!")
        sys.exit(1)

    input_data, ans = generate()

    with open(input_path, "w") as fout:
        fout.write(input_data)

    with open(output_path, "w") as fout:
        fout.write(ans)
