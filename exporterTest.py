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
      "Unknown": [],
      "Blues": []
    }]
    actual = self.exporter._build_data_dictionary("test_data.xml")
    
    self.assertTrue("Blues" in actual[0])
    self.assertEquals(len(actual), len(expected),
      "The list should have the correct number of items")
    self.assertEquals(actual[0].keys(), expected[0].keys(),
      "The second item should have the expected key")

  def test_parsing_artist(self):
    """
      The test ensures that the artist name is parsed correctly and returned
      in the final dictionary as expected.
    """
    expected = [{
      "Unknown": [],
      "Blues": [{
          "track_id": 3566,
          "artist": "Hysteric Ego",
          "name": "Want love"
        },{
          "track_id": 3568,
          "artist": "Junior Jack",
          "name": "E Samba (Rasmus Fabers Canao D"
        }],
    }]
    actual = self.exporter._build_data_dictionary("test_data.xml")
    
    self.assertTrue("Blues" in actual[0])
    self.assertEquals(len(expected), len(actual))
    self.assertEquals(len(actual[0]["Blues"]), len(expected[0]["Blues"]))
    # Checks the artist value
    self.assertEquals(actual[0]["Blues"][0]["artist"],
      expected[0]["Blues"][0]["artist"])
    # Checks the name
    self.assertEquals(actual[0]["Blues"][0]["name"],
      expected[0]["Blues"][0]["name"])
    #print(actual)


if __name__ == '__main__':
  unittest.main()