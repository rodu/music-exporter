from xml.sax import make_parser, handler

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

    def copy(self, filePath, genre, artist, title):
        """
        Copies the file given by file path to the current destination held.
        """
        targetPath = self.destination + genre
        if (self._makeFolder(targetPath)):
            try:
                shutil.copyfile(
                    self._dropFileProtocol(filePath),
                    self._buildFilePath(genre, artist, title))
            except IOError:
                print "[FileCopier] Error copying " + filePath
        else:
            print "[FileCopier] Error creating folder " + targetPath


class Exporter():

    def __init__(self):
        self.destination = "/home/rob/music-exporter-tests/"

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
        library_dict = self._build_data_dictionary(library_path)
        fileCopier = FileCopier(self.destination)
        # Loops over the library dictionary and copies the necessary files in
        # the appropriate destination
        print "[Exporter] Copying files..."
        for entry in library_dict:
            for genre in entry:
                for attributes in entry[genre]:
                    #print attributes
                    fileCopier.copy(
                        attributes["Location"],
                        genre,
                        attributes["Artist"],
                        attributes["Name"])
                #break


def main():
    exporter = Exporter()
    exporter.export_music_library("test_data.xml")

if __name__ == '__main__':
    main()