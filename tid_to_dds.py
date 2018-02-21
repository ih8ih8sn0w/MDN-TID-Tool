import sys, struct, subprocess, os
files = sys.argv[1:]
blocksize = 0
magic = "rgba"
endianess = "big"
def main():
    global blocksize
    for fn in files:
        outfile = (fn.replace('.tid', '_conv.dds'))
        
        
        with open(fn, 'rb') as fp:
            if fp.read(3) != b'TID':
                sys.exit("This is not a valid HDN/MDN texture (missing magic 'TID')")
                continue
            else:
                fp.seek(0)
                data = fp.read()
                decypher_magic(fp)
                fp.seek(100)
                height = (68)
                width = (72)
                fp.seek(height)
                heightVal = fp.read(4)
                fp.seek(width)
                widthVal = fp.read(4)
                pitch = (((int.from_bytes(widthVal, endianess) + 3)//4) * blocksize)
                fp.seek(128)
                texture = fp.read()
        output(outfile, heightVal, widthVal, pitch, texture)

def decypher_magic(fp):
    global blocksize
    global magic
    global endianess
    fp.seek(100)
    magic = fp.read(4)
    if magic == (bytes.fromhex('44585431')):
        print("This is a BE DXT1 texture")
        blocksize = 8
        endianess = "big"
    elif magic == (bytes.fromhex('44585435')):
        print("This is a BE DXT5 texture")
        blocksize = 16
        endianess = "big"
    elif magic == (bytes.fromhex('31545844')):
        print("This is a LE DXT1 texture")
        blocksize = 8
        endianess = "little"
    elif magic == (bytes.fromhex('35545844')):
        print("This is a LE DXT5 texture")
        blocksize = 16
        endianess = "little"
    else: 
        print("This is an unknown format: ", magic, "\n Assuming blocksize is 16 and is big endian")
        blocksize = 16
        endianess = "big"

def output(outfile, heightVal, widthVal, pitch, texture):
    with open(outfile, 'wb') as fpw: # converting tid to dds
        fpw.seek(0)
        fpw.write(bytes.fromhex('44445320')) # magic (0x00)
        fpw.write(bytes.fromhex('7C000000')) # dwSize (must be 124) (0x04)
        fpw.write(bytes.fromhex('07100800')) # flags ;-; (0x08)
        fpw.write(heightVal) # height (0x0C)
        
        fpw.write(widthVal) # width (0x10)
        fpw.write(pitch.to_bytes(4, 'big')) #Pitch Or Linear Size (0x14)
        fpw.write(bytes(4)) # depth will probably always be 0 (0x18)
        fpw.write(bytes(4)) # Mip count will always be 0 (0x1C)
        
        fpw.write(bytes(4 * 11)) # reserved (0x20)
        
        fpw.write(bytes.fromhex('20000000')) # assuming format (0x4C)
        
        fpw.write(bytes.fromhex('04000000')) # Caps (whatever the hell that is) (0x50)
        fpw.write(magic) # writes the magic string (0x54)
        fpw.write(bytes.fromhex('00000000000000000000000000000000000000000010000000000000000000000000000000000000')) #Fuck it all (0x58)
        fpw.write(texture)

main()