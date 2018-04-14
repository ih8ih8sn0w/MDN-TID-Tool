# TID to DDS
Basic TID to DDS converter for use with Megadimension Neptunia DXT1 formatted textures.

Pretty much just created as the existing tid converter failed to build these appropriately. It is really crappy as I don't really care, but it gets the job done. It is not meant to be use for anything else, and probably shouldn't be used as an example for anything.

Requires python 3.x, but not tested on anything besides 3.6.x

The script itself can take as many arguments as allowed, and it will convert all files that are a valid TID to DDS. Also outputs a dat file which is the original header (important for the other script)

# DDS to TID
Converts an edited DDS back to TID while using the original file's header. This is necessary as the game has flags which are dependent on what the texture is for. 

Takes any number of arguments and will convert each DDS back to a texture. You need to have the original .dat with the texture in order for it to correctly convert.

# CL3 Unpacker
Unpacks CL3 archives which are heavily used for textures. Puts them in a folder with the same name.

Takes any number of arguments, etc.

# CL3 Packer
Packs a folder into a valid CL3 archive so that it can be injected into the game. 

Takes any number of arguments, etc.
