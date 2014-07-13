from xml.sax import make_parser, handler
import io

class ParserContentHandler(handler.ContentHandler):

    def __init__(self):
        self._data_dictionary = []

    def start_element(self, name, attrs):
        pass

    def characters(self, content):
        pass

    def optimise_content(self, content):
        pass

    def end_element(self, name):
        pass

    def store(self, list, key, value):
        pass

    def get_data_dictionary(self):
        return self._data_dictionary

def build_data_dictionary(library_path):
    # The routine will parse the music library XML and will build a data
    # structure that will be used later to efficiently copy the files to their
    # new locations
    parser_content_handler = ParserContentHandler()
    parser = make_parser()
    parser.setContentHandler(parser_content_handler)
    parser.parse(get_library_path())

    return parser_content_handler.get_data_dictionary()

def export_music_library(data_dictionary):
    print data_dictionary

def get_library_path():
    # Reads and validate the path to the library file as passed on the command
    # line
    return "Library.xml"
    
def main():
    export_music_library(
        build_data_dictionary(
            get_library_path()
        )
    )

if __name__ == '__main__':
    main()