# iTunes Music Exporter

The music exporter is a Python program to faclilitate the physical
organization of a music collection using a descriptive folders / file names
structure.
The scope is to allow an easy browse of the music library on players such as car
stereos, advanced CD players and so on. These players rely on the folders/files
structure for the user to browse and select the desired traks.

The music exporter parses an xml file created from an export of the iTunes music
library, and organizes such export as a new copy of the files using a specific
naming pattern.
The pattern used will be: [export folder] / [genre] / [artist] - [trak name]

The genre, the artist and the track names will be checked for the presence of
invalid caracters which cannot be used on a given filesystem. The initial
filesystem target will be the HFS+ of Mac, but the program will allow to
easily add more character replacements to satisfy for example NTFS Windows
filesystem requirements.

The program uses the SAX XML parser in order to deal with libraries export of
any size, even quite large, without impacting on memory usage.

