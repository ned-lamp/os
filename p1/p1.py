def pass_one(lines):
    lc = 0
    symtab = {}
    littab = []
    intermediate = []

    mot = {
        "STOP": "00", "ADD": "01", "SUB": "02", "MULT": "03",
        "MOVER": "04", "MOVEM": "05", "COMP": "06", "BC": "07",
        "DIV": "08", "READ": "09", "PRINT": "10"
    }

    reg = {"AREG": "1", "BREG": "2", "CREG": "3"}

    for line in lines:
        parts = line.strip().split()
        if not parts: continue
        if parts[0] == "START":
            lc = int(parts[1])
            intermediate.append((lc, "AD", "01", parts[1]))
            continue
        elif parts[0] == "END":
            intermediate.append(("END",))
            break
        elif parts[0] == "DS":
            size = int(parts[1])
            symtab[last_symbol] = lc
            lc += size
            continue
        elif parts[0] == "DC":
            symtab[last_symbol] = lc
            lc += 1
            continue
        else:
            if parts[0][-1] == ':':  # Label
                last_symbol = parts[0][:-1]
                symtab[last_symbol] = lc
                parts = parts[1:]

            mnemonic = parts[0]
            opcode = mot.get(mnemonic)
            if not opcode:
                continue

            reg_code = reg.get(parts[1].replace(',', ''), '0')
            operand = parts[2] if len(parts) > 2 else None

            if operand and operand.startswith('='):
                littab.append((operand, None))
                operand_ref = f"L{len(littab)}"
            elif operand:
                if operand not in symtab:
                    symtab[operand] = None
                operand_ref = f"S{list(symtab.keys()).index(operand) + 1}"
            else:
                operand_ref = "0"

            intermediate.append((lc, opcode, reg_code, operand_ref))
            lc += 1

    # Assign literal addresses
    start_lit_addr = lc
    for i in range(len(littab)):
        littab[i] = (littab[i][0], start_lit_addr)
        start_lit_addr += 1

    # Assign unassigned symbols
    for s in symtab:
        if symtab[s] is None:
            symtab[s] = lc
            lc += 1

    return intermediate, symtab, littab


def pass_two(intermediate, symtab, littab):
    final_code = []
    lit_dict = {l[0]: l[1] for l in littab}
    sym_list = list(symtab.keys())

    for line in intermediate:
        if line[0] == "END":
            final_code.append("END")
            continue
        if line[1] == "AD":
            final_code.append(f"START {line[3]}")
            continue

        addr, opcode, reg, ref = line
        if ref.startswith('L'):
            lit_index = int(ref[1:]) - 1
            operand_addr = littab[lit_index][1]
        elif ref.startswith('S'):
            sym_index = int(ref[1:]) - 1
            sym = sym_list[sym_index]
            operand_addr = symtab[sym]
        else:
            operand_addr = 0

        final_code.append(f"{addr} {opcode} {reg} {operand_addr}")

    return final_code


def write_file(filename, data):
    with open(filename, 'w') as f:
        for line in data:
            if isinstance(line, tuple):
                f.write(' '.join(map(str, line)) + '\n')
            else:
                f.write(str(line) + '\n')


def assembler():
    with open('input.asm') as f:
        lines = f.readlines()

    inter, symtab, littab = pass_one(lines)
    code = pass_two(inter, symtab, littab)

    write_file("intermediate.txt", inter)
    write_file("symbol_table.txt", [f"{k} {v}" for k, v in symtab.items()])
    write_file("literal_table.txt", [f"{k} {v}" for k, v in littab])
    write_file("machine_code.txt", code)

    print("\n--- INTERMEDIATE ---")
    for i in inter: print(i)
    print("\n--- SYMBOL TABLE ---")
    for s, v in symtab.items(): print(s, v)
    print("\n--- LITERAL TABLE ---")
    for l, v in littab: print(l, v)
    print("\n--- FINAL MACHINE CODE ---")
    for c in code: print(c)


if __name__ == "__main__":
    assembler()
