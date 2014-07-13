from xml.sax import make_parser, handler
import io

class XMLParser(handler.ContentHandler):

    def startElement(self, name, attrs):
        pass

    def characters(self, content):
        pass

    def optimiseContent(self, content):
        pass

    def endElement(self, name):
        pass

    def store(self, list, key, value):
        pass

    