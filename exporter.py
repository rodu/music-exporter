from xml.sax import make_parser, handler

class ParserContentHandler(handler.ContentHandler):

    def __init__(self):
        self._data_dictionary = []
        self._genre_count = 0
        self._tags = {
            "key": 0,
            "string": 0
        }
        self._is_key = 0
        self._is_value = 0
        self._is_genre = 0
        self._genres = {}

    def startElement(self, name, attrs):
        if (name in self._tags):
            self._tags[name] = 1

    def characters(self, content):
        if (content is not None and content.lower() == "genre"):
            self._genre_count += 1
            self._is_genre = 1
            return

        if (self._is_genre and self._tags["string"]):
            # Adds the genre as key of a new set of traks if it does not exists
            if (content not in self._genres):
                # Adds a new genre to the dictionary
                self._genres[self.optimiseContent(content)] = []

    def optimiseContent(self, content):
        return content.replace("/", "-")

    def endElement(self, name):
        if (name in self._tags):
            self._tags[name] = 0
        if (self._is_genre and name == "string"):
            self._is_genre = 0

    def store(self, list, key, value):
        pass

    def get_data_dictionary(self):
        self._data_dictionary.append(self._genres)
        return self._data_dictionary

def build_data_dictionary(library_path):
    # The routine will parse the music library XML and will build a data
    # structure that will be used later to efficiently copy the files to their
    # new locations
    parser_content_handler = ParserContentHandler()
    parser = make_parser()
    parser.setContentHandler(parser_content_handler)
    parser.parse(library_path)

    return parser_content_handler.get_data_dictionary()

def export_music_library(data_dictionary):
    print data_dictionary

def get_library_path():
    # Reads and validate the path to the library file as passed on the command
    # line
    return "../Library.xml"
    
def main():
    export_music_library(
        build_data_dictionary(
            get_library_path()
        )
    )

if __name__ == '__main__':
    main()