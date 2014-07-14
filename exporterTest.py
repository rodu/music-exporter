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
    self.assertEquals(actual[0].keys(), expected[0].keys())

  def test_parsing_artist(self):
    """
      The test ensures that the Artist Name is parsed correctly and returned
      in the final dictionary as expected.
    """
    expected = [{
      "Unknown": [],
      "Blues": [{
          "Track ID": 3566,
          "Artist": "Hysteric Ego",
          "Name": "Want love",
          "Location": "file://localhost/Users/rob/Documents/from_Ubuntu/Documents/vari/Suoneria-Hysteric_Ego_Want_love.mp3"
        },{
          "Track ID": 3568,
          "Artist": "Junior Jack",
          "Name": "E Samba (Rasmus Fabers Canao D",
          "Location": "file://localhost/Users/rob/Documents/from_Ubuntu/Documents/vari/Suoneria-JJ_E_Samba.mp3"
        }],
    }]
    actual = self.exporter._build_data_dictionary("test_data.xml")
    
    self.assertTrue("Blues" in actual[0])
    self.assertEquals(len(expected), len(actual))
    self.assertEquals(len(actual[0]["Blues"]), len(expected[0]["Blues"]))
    # Checks the Artist value
    self.assertEquals(actual[0]["Blues"][0]["Artist"],
      expected[0]["Blues"][0]["Artist"])
    # Checks the Name
    self.assertEquals(actual[0]["Blues"][0]["Name"],
      expected[0]["Blues"][0]["Name"])
    # Checks the Location
    self.assertEquals(actual[0]["Blues"][0]["Location"],
      expected[0]["Blues"][0]["Location"])
    self.assertFalse("Vomitante" in actual[0],
      "An entry which does not have a location should not appear in the results")


if __name__ == '__main__':
  unittest.main()