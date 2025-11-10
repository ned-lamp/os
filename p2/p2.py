# two_pass_macro_processor.py

def trim(s):
    return s.strip()

# PASS I
def pass_one(lines):
    """
    Returns:
      mnt: dict -> name: {'params': [p1,p2,...], 'mdt_index': idx}
      mdt: list of (macro_name, line) -- body lines stored with parameters like &ARG
      intermediate: list of lines where macro definitions removed (macro calls preserved)
    """
    mnt = {}
    mdt = []
    intermediate = []

    i = 0
    while i < len(lines):
        line = trim(lines[i])
        if not line or line.startswith(';'):
            intermediate.append(lines[i].rstrip('\n'))
            i += 1
            continue

        tokens = line.split()
        first = tokens[0]

        if first == 'MACRO':
            # next line must be macro header: name [params]
            i += 1
            header = trim(lines[i])
            header_parts = header.split()
            macro_name = header_parts[0]

            # parse parameters: everything after macro_name separated by commas
            params = []
            if len(header_parts) > 1:
                # reconstruct the parameter string portion (in case of spaces)
                after_name = header[len(macro_name):].strip()
                # split by comma
                raw_params = after_name.split(',')
                for p in raw_params:
                    p = trim(p)
                    if p:
                        params.append(p)  # e.g. &ARG1
            # record start index in mdt
            mnt[macro_name] = {'params': params, 'mdt_index': len(mdt)}
            # now read macro body until MEND
            i += 1
            while i < len(lines):
                body_line = trim(lines[i])
                if body_line == 'MEND':
                    # store MEND marker in MDT (optional, helps during expansion)
                    mdt.append((macro_name, 'MEND'))
                    break
                else:
                    # store body as-is (parameters remain as &X)
                    mdt.append((macro_name, lines[i].rstrip('\n')))
                i += 1
            # skip past MEND
            i += 1
            # do not copy macro definition to intermediate
            continue
        else:
            # normal line or macro call (leave macro call in intermediate)
            intermediate.append(lines[i].rstrip('\n'))
            i += 1

    return mnt, mdt, intermediate

# PASS II
def pass_two(mnt, mdt, intermediate):
    """
    Expand macros using mnt and mdt.
    Returns expanded list of lines (final code).
    """
    expanded = []

    # Build quick access map from macro name to its MDT slice (start..end)
    mdt_map = {}
    idx = 0
    while idx < len(mdt):
        macro_name, entry = mdt[idx]
        start = idx
        # collect until MEND
        while idx < len(mdt) and not (mdt[idx][1] == 'MEND'):
            idx += 1
        # idx now at MEND (or end)
        end = idx  # MEND index
        # slice from start to end-1 (body)
        body_lines = [mdt[j][1] for j in range(start, end)]
        mdt_map[macro_name] = body_lines
        idx += 1  # move past MEND

    # Now process intermediate and expand macro calls
    for line in intermediate:
        sline = trim(line)
        if not sline or sline.startswith(';'):
            expanded.append(line)
            continue
        parts = sline.split()
        first = parts[0]
        if first in mnt:
            # macro call
            # parse actual args (if any) - rest of the line after macro name
            actual_args = []
            rest = sline[len(first):].strip()
            if rest:
                # split by comma
                raw_args = rest.split(',')
                for a in raw_args:
                    actual_args.append(trim(a))
            # mapping: formal param -> actual arg
            formal_params = mnt[first]['params']
            param_map = {}
            for idxp, fp in enumerate(formal_params):
                if idxp < len(actual_args):
                    param_map[fp] = actual_args[idxp]
                else:
                    param_map[fp] = ''  # no argument provided

            # expand the macro body lines by substituting parameters
            body = mdt_map.get(first, [])
            for bline in body:
                # for each formal param replace all occurrences in the line (simple string replace)
                out_line = bline
                for fp, actual in param_map.items():
                    # replace exact token occurrences (fp like &ARG)
                    # simple replace is fine since we are not using regex
                    out_line = out_line.replace(fp, actual)
                expanded.append(out_line)
        else:
            # not a macro call - copy as-is
            expanded.append(line)

    return expanded

# UTIL: write lists to files
def write_lines_file(fname, lines):
    with open(fname, 'w') as f:
        for L in lines:
            f.write(str(L) + '\n')

def dump_mnt_mdt(mnt, mdt):
    # write MNT
    mnt_lines = []
    for name, info in mnt.items():
        params_str = ','.join(info['params']) if info['params'] else ''
        mnt_lines.append(f"{name}\t{info['mdt_index']}\t{params_str}")
    write_lines_file('mnt.txt', mnt_lines)

    # write MDT with index
    mdt_lines = []
    for idx, (mname, entry) in enumerate(mdt):
        mdt_lines.append(f"{idx}\t{mname}\t{entry}")
    write_lines_file('mdt.txt', mdt_lines)

# MAIN (example usage)
def main():
    # example input with a simple macro
    asm_lines = [
        "MACRO",
        "INCR &ARG",
        "LOAD &ARG",
        "ADD =1",
        "STORE &ARG",
        "MEND",
        "",
        "START 100",
        "INCR A",
        "INCR B",
        "MOVEM A, VAR1",
        "MACRO",
        "SWAP &X,&Y",
        "LOAD &X",
        "STORE TEMP",
        "LOAD &Y",
        "STORE &X",
        "LOAD TEMP",
        "STORE &Y",
        "MEND",
        "SWAP A,B",
        "END"
    ]

    # Pass I
    mnt, mdt, intermediate = pass_one(asm_lines)
    # write outputs of pass1
    dump_mnt_mdt(mnt, mdt)
    write_lines_file('intermediate.txt', intermediate)

    # Display pass1 outputs
    print("MNT (macro name table):")
    for name, info in mnt.items():
        print(name, "mdt_index=", info['mdt_index'], "params=", info['params'])
    print("\nMDT (macro definition table):")
    for idx, (mn, entry) in enumerate(mdt):
        print(idx, mn, ":", entry)
    print("\nIntermediate (macros removed):")
    for l in intermediate:
        print(l)

    # Pass II
    expanded = pass_two(mnt, mdt, intermediate)
    write_lines_file('expanded.txt', expanded)

    # Display expanded program
    print("\nExpanded program (after macro expansion):")
    for l in expanded:
        print(l)

    print("\nFiles written: mnt.txt, mdt.txt, intermediate.txt, expanded.txt")

if __name__ == "__main__":
    main()
