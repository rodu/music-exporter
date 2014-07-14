from xml.sax import make_parser, handler

class ParserContentHandler(handler.ContentHandler):

    def __init__(self):
        self._data_dictionary = []
        self._tags = {
            "dict": 0,
            "key": 0,
            "string": 0,
            "integer": 0
        }
        self._is_key = 0
        self._is_value = 0
        
        self._is_dict = 0
        self._is_content_dict = 0
        self._is_genre = 0
        self._is_track_id = 0
        self._is_artist = 0
        self._is_name = 0
        
        self._entries = {
            "Unknown": []
        }
        self._track_id = 0
        self._genre = ""
        self._artist = ""
        self._name = ""

    def startElement(self, name, attrs):
        if (name in self._tags):
            self._tags[name] = 1

    def characters(self, content):
        if (content is None):
            return
        
        if (content == "Genre"):
            self._is_genre = self._is_content_dict = 1
            return

        if (content == "Track ID"):
            self._is_track_id = self._is_content_dict = 1
            return

        if (content == "Artist"):
            self._is_artist = self._is_content_dict = 1
            return

        if (content == "Name"):
            self._is_name = self._is_content_dict = 1
            return

        if (self._is_genre and self._tags["string"]):
            # Adds the genre as key of a new set of traks if it does not exists
            self._genre = self.optimiseContent(content)
            if (self._genre not in self._entries):
                # Adds a new genre to the dictionary
                self._entries[self._genre] = []
            return

        if (self._is_track_id and self._tags["integer"]):
            self._track_id = content
            return

        if (self._is_artist and self._tags["string"]):
            self._artist = self.optimiseContent(content)
            return

        if (self._is_name and self._tags["string"]):
            self._name = self.optimiseContent(content)
            return

    def optimiseContent(self, content):
        if (content):
            return content.replace("/", "-")
        return "Unknown"

    def endElement(self, name):
        #if (name in self._tags):
        #    self._tags[name] = 0
        if (name in self._tags):
            if (self._is_genre and name == "string"):
                self._is_genre = 0
                return

            if (self._is_track_id and name == "integer"):
                self._is_track_id = 0
                return

            if (self._is_artist and name == "string"):
                self._is_artist = 0
                return

            if (self._is_name and name == "string"):
                self._is_name = 0
                return

            if (name == "dict"):
                self._is_dict = 0
                if (self._is_content_dict):
                    # save the created entry
                    if (self._genre or self._artist or self._name):
                        self._entries[(self._genre or "Unknown")].append({
                            "track_id": int(self._track_id),
                            "artist": self._artist,
                            "name": self._name
                        })
                        self._track_id = 0
                        self._artist = ""
                        self._name = ""
                        self._is_content_dict = 0


    def store(self, list, key, value):
        pass

    def get_data_dictionary(self):
        self._data_dictionary.append(self._entries)
        return self._data_dictionary

class Exporter():

    def __init__(self):
        pass

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
        print self._build_data_dictionary(library_path)

def main():
    exporter = Exporter()
    exporter.export_music_library("../Library.xml")

if __name__ == '__main__':
    main()