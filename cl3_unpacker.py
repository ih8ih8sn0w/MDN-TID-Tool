import sys, struct, subprocess, os, binascii
files = sys.argv[1:]
def main():
    for fn in files:
        with open(fn, "rb") as fp:
            if fp.read(4) != b"CL3L":
                sys.exit("This is not a valid MDN cl3 archive (missing magic 'CL3L')")
                # continue
            else:
                fp.seek(0x68)
                length_modifier = int.from_bytes(fp.read(4), "little")
                fp.seek(0x60)
                total_files = int.from_bytes(fp.read(4), "little")
                fp.seek(length_modifier)
                file_block_start = length_modifier
                for x in range(total_files):
                    fp.seek(file_block_start)
                    filename = file_name(file_block_start, fp)
                    dir = fn.replace(".cl3", "")
                    if not os.path.exists(dir):
                        os.mkdir(dir)
                    filename = os.path.join(dir, filename.decode("utf-8"))
                    fp.seek(0x204 + file_block_start)
                    start_pos = int.from_bytes(fp.read(4), "little") + length_modifier
                    file_len = int.from_bytes(fp.read(4), "little")
                    file_block_start += 0x230
                    file_out(fp, filename, start_pos, file_len)

    
def file_name(pos, fp):
    fp.seek(pos)
    byte = bytes(fp.read(1))
    str_len = 0
    while byte != bytes.fromhex("00"):
        byte = bytes(fp.read(1))
        str_len += 1
    fp.seek(pos)
    name = fp.read(str_len)
    return name
    
def logging(fp, fn, dir, length_modifier):
    log = "header.dat"
    log = os.path.join(dir, log)
    with open(fp, "wb+") as fpw:
        header = fp.read(length_modifier)
        fpw.write(header)
        
def file_out(fp, filename, offset, len):
    with open(filename, "wb+") as fpw:
        fp.seek(offset)
        content = fp.read(len)
        fpw.write(content)
    
	
main()