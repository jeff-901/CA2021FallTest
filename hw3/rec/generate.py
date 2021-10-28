import os
import sys
import random

def recaman(n):
    series = [0 for _ in range(n)]
    series[0] = 0
    for i in range(1, n):
        if series[i - 1] - i > 0 and series[i - 1] - i not in series:
            series[i] = series[i - 1] - i
        else:
            series[i] = series[i - 1] + i
    return series


def generate():
    n = 201
    input_data = "\n".join(str(i) for i in range(n))
    ans = "\n".join(str(i) for i in recaman(n))

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
