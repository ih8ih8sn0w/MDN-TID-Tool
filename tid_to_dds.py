import sys, struct, subprocess, os

currentOffset = 0
output = (sys.argv[1].replace('.tid', '_conv.dds'))


with open(sys.argv[1], 'rb') as fp:
    if fp.read(3) != b'TID':
        sys.exit(sys.argv[1], "This is not a valid HDN/MDN texture (missing magic 'TID'")
    else:
        fp.seek(0)
        data = fp.read()
        magic = data.find(bytes.fromhex(('44585431')))
        fp.seek(magic)
        height = (magic - 32)
        width = (magic - 28)
        fp.seek(height)
        heightVal = fp.read(4)
        fp.seek(width)
        widthVal = fp.read(4)
        pitch = (((int.from_bytes(widthVal, 'big') + 3)//4) * 8)
        fp.seek(128)
        texture = fp.read()
        

with open(output, 'wb') as fpw: # converting tid to dds
    fpw.seek(0)
    fpw.write(bytes.fromhex('44445320')) # magic (0x00)
    fpw.write(bytes.fromhex('7C000000')) #dwSize (must be 124) (0x04)
    fpw.write(bytes.fromhex('07100800')) # flags ;-; (0x08)
    fpw.write(heightVal) # height (0x0C)
    
    fpw.write(widthVal) # width (0x10)
    fpw.write(int.to_bytes(pitch, 4, 'big')) #Pitch Or Linear Size (0x14)
    fpw.write(bytes(4)) # depth will probably always be 0 (0x18)
    fpw.write(bytes(4)) # Mip count will always be 0 (0x1C)
    
    fpw.write(bytes(4 * 11)) # reserved (0x20)
    
    fpw.write(bytes.fromhex('20000000')) # assuming format (0x4C)
    
    fpw.write(bytes.fromhex('04000000')) # Caps (whatever the hell that is) (0x50)
    fpw.write(bytes.fromhex('4458543100000000000000000000000000000000000000000010000000000000000000000000000000000000')) #Fuck it all (0x54)
    fpw.write(texture)
    