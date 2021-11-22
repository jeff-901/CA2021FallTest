import random
import numpy as np

print(".globl __start")

print(".text")
print("__start:")

isa = ["and", "xor", "sll", "add", "sub", "mul", "addi", "srai"]
operator = {
    "and": "&",
    "xor": "^",
    "sll": "<<",
    "add": "+",
    "sub": "-",
    "mul": "*",
    "addi": "+",
    "srai": ">>",
}

PC = 0
fp = open("./output_gen.txt", "w")
num = 30  # num of instructions

reg = [0] * 32
reg = np.array(reg, np.int32)


def output():
    regStr = []
    for i in reg:
        regStr.append(str(i).rjust(10, " "))

    # fmt:off
    fp.write("PC = {}\n".format(str(PC).rjust(10, " ")))
    fp.write("Registers\n");
    fp.write("x0     = {}, x8(s0)  = {}, x16(a6) = {}, x24(s8)  = {}\n".format(regStr[0], regStr[8] , regStr[16], regStr[24]))
    fp.write("x1(ra) = {}, x9(s1)  = {}, x17(a7) = {}, x25(s9)  = {}\n".format(regStr[1], regStr[9] , regStr[17], regStr[25]))
    fp.write("x2(sp) = {}, x10(a0) = {}, x18(s2) = {}, x26(s10) = {}\n".format(regStr[2], regStr[10], regStr[18], regStr[26]))
    fp.write("x3(gp) = {}, x11(a1) = {}, x19(s3) = {}, x27(s11) = {}\n".format(regStr[3], regStr[11], regStr[19], regStr[27]))
    fp.write("x4(tp) = {}, x12(a2) = {}, x20(s4) = {}, x28(t3)  = {}\n".format(regStr[4], regStr[12], regStr[20], regStr[28]))
    fp.write("x5(t0) = {}, x13(a3) = {}, x21(s5) = {}, x29(t4)  = {}\n".format(regStr[5], regStr[13], regStr[21], regStr[29]))
    fp.write("x6(t1) = {}, x14(a4) = {}, x22(s6) = {}, x30(t5)  = {}\n".format(regStr[6], regStr[14], regStr[22], regStr[30]))
    fp.write("x7(t2) = {}, x15(a5) = {}, x23(s7) = {}, x31(t6)  = {}\n\n\n".format(regStr[7], regStr[15], regStr[23], regStr[31]))
    # fmt:on


while num > 0:
    output()
    ins = isa[random.randint(0, len(isa) - 1)]
    rd, rs1, rs2 = random.randint(1, 31), random.randint(0, 31), random.randint(0, 31)
    if ins == "addi":
        imm = random.randint(-(2 ** 11), 2 ** 11 - 1)
        print(f"\taddi x{rd}, x{rs1}, {imm}")
        reg[rd] = reg[rs1] + imm
    elif ins == "srai":
        imm = random.randint(0, 31)
        print(f"\tsrai x{rd}, x{rs1}, {imm}")
        reg[rd] = reg[rs1] >> imm
    elif ins == "sll":
        while reg[rs2] < 0:
            rs2 = random.randint(0, 31)
        print(f"\tsll x{rd}, x{rs1}, x{rs2}")
        reg[rd] = (reg[rs1] << reg[rs2]) & 0xFFFFFFFF
    else:
        print(f"\t{ins} x{rd}, x{rs1}, x{rs2}")
        operation = f"reg[rd] = reg[rs1] {operator[ins]} reg[rs2]"
        exec(operation)
    PC += 4
    num -= 1

fp.close()
