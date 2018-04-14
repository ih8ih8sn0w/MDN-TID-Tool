import sys, struct, subprocess, os, binascii
dir = sys.argv[1:]
def main():
    print(dir)
    for x in dir:
        out = x + ".cl3"
        with open(out, "wb+") as fpw:
            files = os.listdir(x)
            # header stuff
            fpw.write(0x434C334C.to_bytes(4, byteorder = "big")) # magic
            zeros(fpw, 4)
            fpw.write(0x03000000.to_bytes(4, byteorder = "big"))
            fpw.write(0x02000000.to_bytes(4, byteorder = "big"))
            fpw.write(0x40.to_bytes(1, byteorder = "big"))
            zeros(fpw, 7)
            fpw.write(0xFFFFFFFF.to_bytes(4, byteorder = "big"))
            zeros(fpw, 36)
            
            fpw.write("FILE_COLLECTION".encode("utf-8"))
            zeros(fpw, 0x11)
            fpw.write(len(files).to_bytes(4, byteorder = "little"))
            zeros(fpw, 0x4)
            fpw.write(0xE0000000.to_bytes(0x4, byteorder = "big"))
            zeros(fpw, 0x24)
            fpw.write("FILE_LINK".encode("utf-8"))
            zeros(fpw, 0x47)
            write_offset = 0x230 * len(files) + 0xE0 # offset for files themselves
            print("len files:", len(files))
            header_offset = 0xE0
            print("init write:", format(write_offset, "8x"), "init header:", format(header_offset, "8x"))
            old_offset = 0
            for fs in files:
                fn = os.path.join(x, fs)
                print(fn)
                with open(fn, "rb") as fp:
                    dn = fp.read()
                    fileinfo = os.stat(fn)
                    fpw.seek(header_offset)
                    fpw.write(fs.encode("utf-8"))
                    zeros(fpw, (0x208 - len(fs)))
                    offset_offset = fpw.tell() - 0x4 # place where the files starting position will be kept
                    fpw.write(int(fileinfo.st_size).to_bytes(0x4, byteorder = "little"))
                    zeros(fpw, 0x24)
                    header_offset += 0x230
                    fpw.seek(write_offset)
                    print("len dn:",format(len(dn), "8x"))
                    fpw.write(dn)
                    old_offset = write_offset
                    write_offset = fpw.tell()
                    fpw.seek(offset_offset)
                    fpw.write((old_offset - 0xE0).to_bytes(0x4, byteorder = "little"))
                    print("header_offset", format(header_offset, "8x"), "\nwrite_offset", format(write_offset, "8x"), "\nheader_offset", format(header_offset, "8x"))
            fpw.seek(0x64)
            fpw.write((write_offset - 0xE0).to_bytes(0x4, byteorder = "little"))
            fpw.seek(0xB8)
            fpw.write((write_offset).to_bytes(0x4, byteorder = "little"))
def zeros(fpw, num):
    x = 0
    while x < num:
        fpw.write(0x00.to_bytes(1, byteorder = "big"))
        x += 1


main()