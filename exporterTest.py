import unittest
from exporter import ParserContentHandler

class ExporterTest(unittest.TestCase):
  
  def setUp(self):
    self._parserContentHandler = ParserContentHandler()

  def test_ParserContentHandler_optimiseContent(self):
    # Tests that slashes are replaced with hyphens
    self.assertEquals(
      self._parserContentHandler.optimiseContent("ab/cd"),
      "ab-cd")

if __name__ == '__main__':
  unittest.main()