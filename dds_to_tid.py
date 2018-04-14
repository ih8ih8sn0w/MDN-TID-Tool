import sys, struct, subprocess, os, binascii
files = sys.argv[1:]
magic = "rgba"
endianess = "big"
filesize = 0
def main():
    global filesize
    for fn in files:
        type = file_type_check(fn)
        fileinfo = os.stat(fn)
        filesize = int(fileinfo.st_size)
        
        with open(fn, 'rb') as fp:
            if type == "dds":
                outfile = fn.replace('.dds', '.tid')
                dds_to_tid(fp, outfile)
            else:
                print("This is not a valid dds texture. Missing magic 'DDS'")

def file_type_check(files):
    filename, extension = os.path.splitext(files)
    if extension == ".tid":
        return "tid"
    elif extension == ".dds":
        return "dds"
    else:
        print("This is not a valid image format that I can convert from (", extension, ")", sep="")

        
def dds_to_tid(fp, outfile):
    global magic
    fp.seek(0x0C)
    height = fp.read(4)
    width = fp.read(4)
    fp.seek(0x54)
    magic = fp.read(4)
    fp.seek(0x80)
    texture = fp.read()
    tid_out(outfile, texture, height, width)
    
def tid_out(fn, texture, height, width):
    global magic
    global filesize
    global endianess
    dat = fn.replace('.tid', '.dat')
    data = open(dat, "rb")
    header = data.read()
    parse_header(data)
    data.close()
    with open(fn, "wb") as fpw:
        filename = os.path.basename(fn)
        fpw.seek(0)
        fpw.write(header)
        #fpw.write(b"TID")
        #fpw.write(bytes.fromhex("9880000000800000000100000001000000200000000000000000000000"))# rest of the header
        fpw.seek(0x20)
        fpw.write(bytearray(filename, "utf-8")) # to cover the filename which might not even be relevant)
        # while len(filename) + 32 + counter <= 63:
            # fpw.write(bytes.fromhex('00'))
            # counter += 1
        fpw.seek(0x44)
        fpw.write(endian_handler(height))
        fpw.write(endian_handler(width))
        fpw.seek(0x80)
        fpw.write(texture)

def parse_header(data):
    data.seek(0x60)
    tex = data.read(4)
    if magic == (bytes.fromhex('44585431')): # BE DXT1
        endianess = "little"
        
    elif magic == (bytes.fromhex('44585435')): # BE DXT5
        endianess = "little"
        
    elif magic == (bytes.fromhex('31545844')): # LE DXT1
        endianess = "big"
        
    elif magic == (bytes.fromhex('35545844')): # LE DXT5
        endianess = "big"

def endian_handler(val):
    global endianess
    if endianess == "big":
        return val
    else: 
        return val[::-1]
main()
