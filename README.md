# MDN-TID-Tool
Basic TID to DDS converter for use with Megadimension Neptunia DXT1 formatted textures.

Pretty much just created as the existing tid converter failed to build these appropriately. It is really crappy as I don't really care, but it gets the job done. It is not meant to be use for anything else, and probably shouldn't be used as an example for anything.

Requires python 3.x, but not tested on anything besides 3.6.x

Just use the .tid as the first argument, and it will output as \[filename]\_converted.dds

There are an excessive number of assumptions made just because I didn't feel like figuring out stuff, but as long as the texture is dxt1, it should output fine. 
