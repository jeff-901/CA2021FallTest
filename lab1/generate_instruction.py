def reg_encode(register: str):
    """Register encoding, e.g. convert x6 to 00110"""
    return "{0:05b}".format(int(register[1:]))

def imm_encode(imm: str) -> str:
    """Encode immediate as 2's complement number, padding to 32 bits."""
    imm = int(imm)
    if imm == 0:
        return "0" * 32
    encoded = "{0:032b}".format(abs(imm))
    if imm < 0:
        idx = encoded.rindex("1")
        L = list()
        for i in range(idx - 1, -1, -1):
            if encoded[i] == "0":
                L.append("1")
            else:
                L.append("0")
        encoded = "".join(L)[::-1] + encoded[idx:]
    return encoded

def parse_imm_reg(s: str):
    """Parse immediate and register, e.g. input "8(x5)" will return (8, x5)"""
    l_idx = s.index("(")
    r_idx = s.index(")")
    imm = s[:l_idx].strip()
    reg = s[(l_idx + 1):r_idx].strip()
    return imm, reg

def assemble(instruction: str):
    """Assemble an instruction, return its assembly code."""
    assembly_table = {
        "and": "0000000_{rs2}_{rs1}_111_{rd}_0110011",
        "xor": "0000000_{rs2}_{rs1}_100_{rd}_0110011",
        "sll": "0000000_{rs2}_{rs1}_001_{rd}_0110011",
        "add": "0000000_{rs2}_{rs1}_000_{rd}_0110011",
        "sub": "0100000_{rs2}_{rs1}_000_{rd}_0110011",
        "mul": "0000001_{rs2}_{rs1}_000_{rd}_0110011",
        "addi": "{imm}_{rs1}_000_{rd}_0010011",
        "srai": "0100000_{imm}_{rs1}_101_{rd}_0010011",
        "lw": "{imm}_{rs1}_010_{rd}_0000011",
        "sw": "{imm_11_5}_{rs2}_{rs1}_010_{imm_4_0}_0100011",
        "beq": "{imm_12_10_5}_{rs2}_{rs1}_000_{imm_4_1_11}_1100011",
    }
    operation, rest = instruction.split(maxsplit=1)
    tokens = [x.strip() for x in "".join(rest).split(",")]
    assembly = assembly_table[operation]
    if operation == "addi":
        rd, rs1, imm = tokens
        rd = reg_encode(rd)
        rs1 = reg_encode(rs1)
        imm = imm_encode(imm)[-12:]
        assembly = assembly.format(rd=rd, rs1=rs1, imm=imm)
    elif operation == "srai":
        rd, rs1, imm = tokens
        rd = reg_encode(rd)
        rs1 = reg_encode(rs1)
        imm = imm_encode(imm)[-5:]
        assembly = assembly.format(rd=rd, rs1=rs1, imm=imm)
    elif operation == "lw":
        rd, imm_rs1 = tokens
        imm, rs1 = parse_imm_reg(imm_rs1)
        rd = reg_encode(rd)
        imm = imm_encode(imm)[-12:]
        rs1 = reg_encode(rs1)
        assembly = assembly.format(rd=rd, imm=imm, rs1=rs1)
    elif operation == "sw":
        rs2, imm_rs1 = tokens
        imm, rs1 = parse_imm_reg(imm_rs1)
        imm = imm_encode(imm)
        rs1 = reg_encode(rs1)
        rs2 = reg_encode(rs2)
        imm_11_5 = imm[-12:-5]
        imm_4_0 = imm[-5:]
        assembly = assembly.format(rs1=rs1, rs2=rs2,
                                   imm_11_5=imm_11_5,
                                   imm_4_0=imm_4_0)
    elif operation == "beq":
        rs1, rs2, imm = tokens
        rs1 = reg_encode(rs1)
        rs2 = reg_encode(rs2)
        imm = imm_encode(imm)
        imm_12_10_5 = imm[-13] + imm[-11:-5]
        imm_4_1_11 = imm[-5:-1] + imm[-12]
        assembly = assembly.format(rs1=rs1, rs2=rs2,
                                   imm_12_10_5=imm_12_10_5,
                                   imm_4_1_11=imm_4_1_11)
    else: # R type
        rd, rs1, rs2 = [reg_encode(x) for x in tokens]
        assembly = assembly.format(rd=rd, rs1=rs1, rs2=rs2)
    return assembly


if __name__ == "__main__":
    with open("instruction.txt") as fin, open("instruction_generated.txt", "w") as fout:
        for line in fin:
            assembly = assemble(line)
            fout.write(assembly.ljust(38) + "// " + line)