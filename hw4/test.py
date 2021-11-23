import subprocess
import os

os.system("iverilog *.v")

count = 0
total = 100

for i in range(total):
    os.system("python3 genCode.py > code.s")
    subprocess.getoutput("jupiter code.s --dump-code code.txt")
    os.system(f"python3 hexToBin.py code.txt > instruction.txt")

    subprocess.getoutput("./a.out")

    output = subprocess.getoutput("diff output.txt output_gen.txt")
    if output != "":
        count += 1
        os.system("cp code.s code{}.s".format(count))
        os.system("cp output.txt output{}.txt".format(count))
        os.system("cp output.txt output{}.txt".format(count))
        os.system("cp output_gen.txt output{}_ref.txt".format(count))
        with open("log{}.txt".format(count), "w") as fp:
            fp.write(output)
        print("test {} failed".format(i))
    else:
        print("test {} passed".format(i))

    os.system("rm code.s code.txt instruction.txt output_gen.txt output.txt")

print("run {} tests, {} passed, {} failed".format(total, total - count, count))
