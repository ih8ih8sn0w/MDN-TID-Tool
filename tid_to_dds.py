import sys, struct, subprocess, os, binascii
files = sys.argv[1:]
blocksize = 0
magic = "rgba"
endianess = "big"
filename = "none"
def main():
    global blocksize
    global filename
    for fn in files:
        filename = fn
        type = file_type_check(fn)
        fileinfo = os.stat(fn)
        filesize = int(fileinfo.st_size)
        
        with open(fn, 'rb') as fp:
            if type == "tid":
                outfile = (fn.replace('.tid', '.dds'))
                data = tid_to_dds(fp, outfile, filesize)
                datafile = (fn.replace('.tid', '.dat'))
                with open(datafile, 'wb') as dat:
                    dat.write(data)
            else:
                print("This is not a valid TID texture. Missing magic 'TID'")
            #dds_out(outfile, widthVal, pitch, texture, filesize, heightValHex, widthValHex)

def decypher_magic(fp):
    global blocksize
    global magic
    global endianess
    global filename
    fp.seek(100)
    magic = fp.read(4)
    if magic == (bytes.fromhex('44585431')):
        print(filename, "is a BE DXT1 texture")
        blocksize = 8
        endianess = "big"
    elif magic == (bytes.fromhex('44585435')):
        print(filename, "is a BE DXT5 texture")
        blocksize = 16
        endianess = "big"
    elif magic == (bytes.fromhex('31545844')):
        print(filename, "is a LE DXT1 texture")
        blocksize = 8
        endianess = "little"
        magic = bytes.fromhex(('44585431'))
    elif magic == (bytes.fromhex('35545844')):
        print(filename, "is a LE DXT5 texture")
        blocksize = 16
        endianess = "little"
        magic = bytes.fromhex(('44585435'))
    else: 
        print(outfile, " is an unknown format: ", magic, "\n Assuming blocksize is 16 and is big endian", sep="")
        blocksize = 16
        endianess = "big"
def file_type_check(files):
    filename, extension = os.path.splitext(files)
    if extension == ".tid":
        return "tid"
    elif extension == ".dds":
        return "dds"
    else:
        print("This is not a valid image format that I can convert from (", extension, ")", sep="")

def tid_to_dds(fp, outfile, filesize):
    if fp.read(3) != b'TID':
        sys.exit("This is not a valid HDN/MDN texture (missing magic 'TID')")
    else:
        fp.seek(0)
        header = fp.read(0x80)
        decypher_magic(fp) # this also should determine if the file is BE or LE
        fp.seek(100)
        height = (68)
        width = (72)
        fp.seek(height)
        fp.seek(height)
        heightValHex = fp.read(4)
        fp.seek(width)
        widthVal = int.from_bytes(fp.read(4), endianess)
        fp.seek(width)
        widthValHex = fp.read(4)
        pitch = (((widthVal + 3)//4) * blocksize)
        if pitch >= 4294967296:
            pitch = (((128 + 3)//4) * 16)
        fp.seek(128)
        # if endianess == "big"
        texture = fp.read()
        dds_out(outfile, pitch, texture, filesize, heightValHex, widthValHex, fp)
        return header

def dds_out(outfile, pitch, texture, filesize, heightValHex, widthValHex, fp):
    with open(outfile, 'wb') as fpw: # converting tid to dds
        fpw.seek(0)
        fpw.write(bytes.fromhex('44445320')) # magic (0x00)
        fpw.write(bytes.fromhex('7C000000')) # dwSize (must be 124) (0x04)
        fpw.write(bytes.fromhex('07100800')) # flags ;-; (0x08)
        fpw.write(endian_handler(heightValHex)) # height (set to big as conversion already took place) (0x0C)
        
        fpw.write(endian_handler(widthValHex)) # width (0x10)
        fpw.write(pitch.to_bytes(4, endianess)) #Pitch Or Linear Size (0x14)
        fpw.write(bytes(4)) # depth will probably always be 0 (0x18)
        fpw.write(bytes(4)) # Mip count will always be 0 (0x1C)
        
        fpw.write(bytes(4 * 11)) # reserved (0x20)
        
        fpw.write(bytes.fromhex('20000000')) # assuming format (0x4C)
        
        fpw.write(bytes.fromhex('04000000')) # Caps (whatever the hell that is) (0x50)
        fpw.write(magic) # writes the magic string (0x54)
        fpw.write(bytes.fromhex('00000000000000000000000000000000000000000010000000000000000000000000000000000000')) #Fuck it all (0x58)
        fpw.write(texture)


def endian_handler(val):
    global endianess
    if endianess == "big":
        return val
    else: 
        return val[::-1]

main()