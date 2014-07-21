from xml.sax import make_parser, handler
from optparse import OptionParser

class ParserContentHandler(handler.ContentHandler):

    def _get_parsed_names(self):
        return {
            "Genre": "",
            "Track ID": 0,
            "Artist": "",
            "Name": "",
            "Location": ""
        }

    def __init__(self):
        self._data_dictionary = []
        self._tags = ["dict", "key", "string", "integer"]
        self._parsed_flags = self._get_parsed_names().keys()
        self._parsed_values = self._get_parsed_names()
        self._is_content_dict = 0
        self._entries = {
            "Unknown": []
        }
        self._current = ""

    #def startElement(self, name, attrs):

    def characters(self, content):
        if (not content):
            return
        
        if (content in self._parsed_flags):
            self._is_content_dict = 1
            self._current = content
            return

        if (self._current and (self._current in self._parsed_flags)):
            # Optimize all fields but Location
            self._parsed_values[self._current] = self.optimiseContent(
                    content) if self._current != "Location" else content
            self._current = ""
            return

    def optimiseContent(self, content):
        if (content):
            return content.replace("/", "-")
        return "Unknown"

    def endElement(self, name):
        if (name in self._tags):
            #self._tags[name] = 0
            if (name in self._parsed_flags):
                return

            if (name == "dict"):
                if (self._is_content_dict):
                    # save the created entry
                    if (self._parsed_values["Location"]):
                        genre = (self._parsed_values["Genre"] or "Unknown")
                        if (genre not in self._entries):
                            self._entries[genre] = []

                        self._entries[genre].append({
                            "Track ID": self._parsed_values["Track ID"],
                            "Artist": self._parsed_values["Artist"] or "Unknown",
                            "Name": self._parsed_values["Name"] or "Unknown",
                            "Location": self._parsed_values["Location"]
                        })
                    self._parsed_values = self._get_parsed_names()
                    self._is_content_dict = 0
                    self._current = ""


    def store(self, list, key, value):
        pass

    def get_data_dictionary(self):
        self._data_dictionary.append(self._entries)
        #print self._data_dictionary
        return self._data_dictionary

import re
import os
import shutil
class FileCopier():

    def __init__(self, destination):
        if (not destination):
            raise Exception("destination parameter not provided")

        self.destination = destination
        print "[FileCopier] Initialized with destination " + destination

    def _extractFolderPath(self, filePath):
        """
        Receive a complete file path and returns a new path pointing to the
        folder containing the given file. The method returns 0 if operation
        fails.
        """
        if (not filePath or filePath.count("/") < 3):
            return 0

        return filePath[0:filePath.rfind("/")]

    def _makeFolder(self, folderPath):
        """
        Creates the folder with the given name parameter at the given path.
        It does nothing if such folder already exists at the given path.
        """
        if (os.path.isdir(folderPath)):
            return 1

        try:
            os.makedirs(folderPath)
        except OSError:
            return 0
        
        return 1

    def _buildFilePath(self, genre, artist, title):
        """
        Given genre, artist title and known destination the method builds the
        target to be used in the file copy.
        """
        return self.destination + genre + "/" + artist + " - " + title + ".mp3"

    def _dropFileProtocol(self, filePath):
        """
        If receiving a filePath containing a file:// protocol, it will return a
        new value without the protocol
        """
        if (re.match(r"(file:\/\/)", filePath)):
            return filePath[6:len(filePath)]

        return filePath

    def _sanitizeFileName(self, fileName):
        """
        Given the storage used as Fat32 for external USB drives, the file name
        must be free of invalid characters for such target filesystem
        """
        invalidChars = r"[\"*+,/:;<=>?\|]"
        return re.sub(invalidChars, r"_", fileName)


    def copy(self, filePath, genre, artist, title):
        """
        Copies the file given by file path to the current destination held.
        """
        sourcePath = self._dropFileProtocol(filePath)
        targetPath = self.destination + genre
        if (self._makeFolder(targetPath)):
            if (os.path.exists(sourcePath)):
                try:
                    shutil.copyfile(
                        sourcePath,
                        self._buildFilePath(
                            self._sanitizeFileName(genre),
                            self._sanitizeFileName(artist),
                            self._sanitizeFileName(title))
                        )
                except IOError:
                    print "[FileCopier] Error copying " + filePath
            else:
                print "[FileCopier] Not exists: " + sourcePath
        else:
            print "[FileCopier] Error creating folder " + targetPath

import sys
class Exporter():

    def __init__(self, destination, export_genres="", max_exports=0):
        self.destination = destination
        self.export_genres = export_genres.split(",")
        self.max_exports = max_exports

    def _build_data_dictionary(self, library_path):
        # The routine will parse the music library XML and will build a data
        # structure that will be used later to efficiently copy the files to their
        # new locations
        parser_content_handler = ParserContentHandler()
        parser = make_parser()
        parser.setContentHandler(parser_content_handler)
        parser.parse(library_path)

        return parser_content_handler.get_data_dictionary()

    def export_music_library(self, library_path):
        def read_attributes(entry):
            for attributes in entry:
                #print attributes
                self.i += 1
                if (self.max_exports > 0 and self.i > self.max_exports):
                    break
                fileCopier.copy(
                    attributes["Location"],
                    genre,
                    attributes["Artist"],
                    attributes["Name"])

        library_dict = self._build_data_dictionary(library_path)
        fileCopier = FileCopier(self.destination)
        # Loops over the library dictionary and copies the necessary files in
        # the appropriate destination
        print "[Exporter] Copying files..."
        filterGenres = len(self.export_genres) > 0
        self.i = 0
        for entry in library_dict:
            for genre in entry:
                if (filterGenres):
                    if (genre in self.export_genres):
                        read_attributes(entry[genre])
                else:
                    read_attributes(entry[genre])

def print_help():
    print "\nMusicExporter -"
    print "exporter.py [library path] [destination path] [max files export]"
    print "\n"

def main():
    """
    The method accepts and validates command line arguments. Then runs the
    exporter routines
    """
    args = sys.argv
    if (len(args) < 3):
        print "Invalid parameters."
        print_help()
        return 0

    optionParser = OptionParser()
    optionParser.add_option(
        "-l",
        "--library",
        action="store",
        type="string",
        dest="libraryPath")

    optionParser.add_option(
        "-d",
        "--destination",
        action="store",
        type="string",
        dest="destination")

    optionParser.add_option(
        "-g",
        "--genres",
        action="store",
        type="string",
        dest="export_genres")

    optionParser.add_option(
        "-m",
        "--max-exports",
        action="store",
        type="int",
        dest="max_exports",
        default=0)
    
    (options, args) = optionParser.parse_args()
    #print options
    #return 0
    
    if (not os.path.exists(options.libraryPath)):
        print "The library path is not valid."
        return 0

    if(not os.path.isdir(options.destination)):
        print "Destination not existing. Please create it first."
        return 0

    # Adds last slash if not provided
    if (options.destination[len(options.destination) - 1] != "/"):
        options.destination += "/"

    if (options.export_genres):
        options.export_genres = options.export_genres.replace("/", "-")

    exporter = Exporter(
        options.destination,
        options.export_genres,
        options.max_exports)
    exporter.export_music_library(options.libraryPath)

if __name__ == '__main__':
    main()