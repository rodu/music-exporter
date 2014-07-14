import unittest
import exporter

class ParserContentHandlerTest(unittest.TestCase):
  
  def setUp(self):
    self._parserContentHandler = exporter.ParserContentHandler()

  def test_ParserContentHandler_optimiseContent(self):
    # Tests that slashes are replaced with hyphens
    self.assertEquals(
      self._parserContentHandler.optimiseContent("ab/cd"),
      "ab-cd")

class ExporterTest(unittest.TestCase):

  def setUp(self):
    self.exporter = exporter.Exporter()

  def test_parsing_gernes(self):
    """
      The test ensures that genres are parsed correctly and the genres
      dictionary is built as expected given a testing data set
    """
    expected = [{
      "Blues": []
    }]
    actual = self.exporter._build_data_dictionary("test_data.xml")
    for i in range(len(actual)):
      self.assertEquals(actual[i].keys(), expected[i].keys())


if __name__ == '__main__':
  unittest.main()