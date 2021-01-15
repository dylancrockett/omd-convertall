OMD Convert All
---------------
This repository contains the **convertall.py** script which can be used to convert an entire directory
of midi files into .omd files using OneTesla's [omd converter](https://github.com/stridera/oneTesla-Interrupter/tree/master/omd/omdconvert).

The script will find all midi files in the top level and immediate subdirectories of the specified
directory (by default the relative directory './midi') and convert all .mid files found into .omd files
using the aforementioned omd converter. The program will also create mirror subdirectories in the specified
output directory and then move all generated .omd files into the mirrored output directory.

An example directory without specifying the source and output would look like this:
```
/somefolder
|   convertall.py
|   omdconvert.exe
|
+---- /midi
|     |   coolsong.mid
|     |   favoritesong.mid
|     |   ...
|     |
|     +---- /newsongs
|           |   song1.mid
|           |   song2.mid
|           |   ...
|
+---- /omd (empty)
```

After running convertall.py the './omd' directory would be populated and the directory would look like this:
```
/somefolder
|   convertall.py
|   omdconvert.exe
|
+---- /midi
|     |   coolsong.mid
|     |   favoritesong.mid
|     |   ...
|     |
|     +---- /newsongs
|           |   song1.mid
|           |   song2.mid
|           |   ...
|
+---- /omd
|     |   coolsong.omd
|     |   favoritesong.omd
|     |   ...
|     |
|     +---- /newsongs
|           |   song1.omd
|           |   song2.omd
|           |   ...
```

If new songs are added/moved or the directory structure in the source directory changes, all you need to do is 
run convertall.py again and the output directory will be wiped and be re-populated to match the new structure of
the input directory.

Important Notes for Running:
- Requires omdconvert.exe to be located in the same directory as this program.
- Tested with Python 3.8, *should* work with Python 3.7 or newer.
- Does not support more than one level deep subdirectories in the source folder, this is because of the 
limitation 
- If run without arguments the directory used to source .mid files is the relative directory './midi' and output to
the relative directory './omd'.
- Midi source directory can be specified using the -s or -source flag, output directory can be specified using -o
or -output tag, verbose logging can be turned on by providing the -v or --verbose flag.
