import unittest
import exporter
import os

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
    self.exporter = exporter.Exporter(
        "/home/rob/music-exporter-tests/"
      )

  def test_parsing_gernes(self):
    """
      The test ensures that genres are parsed correctly and the genres
      dictionary is built as expected given a testing data set
    """
    expected = [{
      "Unknown": [],
      "Blues": [],
      "House-Vocal": []
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
          "Location": "file://home/rob/music-exporter-tests/vari/Suoneria-Hysteric_Ego_Want_love.mp3"
        },{
          "Track ID": 3568,
          "Artist": "Junior Jack",
          "Name": "E Samba (Rasmus Fabers Canao D",
          "Location": "file://home/rob/music-exporter-tests/vari/Suoneria-JJ_E_Samba.mp3"
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

class FileCopierTest(unittest.TestCase):

    def setUp(self):
        self.destination = os.environ["HOME"] + "/music-exporter-tests/"
        self.fileCopier = exporter.FileCopier(self.destination)

    def test_extractValidFolderPath(self):
        folderPath = "file://home/rob/music-exporter-tests/vari/Suoneria-Hysteric_Ego_Want_love.mp3"
        self.assertEquals(
            "file://home/rob/music-exporter-tests/vari",
            self.fileCopier._extractFolderPath(folderPath))

    def test_extractNonValidFolderPath(self):
        self.assertEquals(0, self.fileCopier._extractFolderPath(""))
        self.assertEquals(0, self.fileCopier._extractFolderPath("file://"))

    def test_makeFolder_Returns1IfFolderAlreadyExists(self):
        folderPath = self.destination
        self.assertEquals(1, self.fileCopier._makeFolder(folderPath))

    def test_makeFolder_createsFolderAtGivenDestination(self):
        folderPath = self.destination + "house-tribal-deep"
        self.assertEquals(1, self.fileCopier._makeFolder(folderPath))
        # Check that the folder was actually created
        self.assertTrue(os.path.isdir(folderPath))

    def test_dropFileProtocol_removesTheProtocol(self):
        filePath = "file://home/rob/music-exporter-tests/vari/Suoneria-JJ_E_Samba.mp3"
        self.assertEquals(
            "/home/rob/music-exporter-tests/vari/Suoneria-JJ_E_Samba.mp3",
            self.fileCopier._dropFileProtocol(filePath))

        filePath = "file://localhost/home/rob/music-exporter-tests/vari/Suoneria-JJ_E_Samba.mp3"
        self.assertEquals(
            "/home/rob/music-exporter-tests/vari/Suoneria-JJ_E_Samba.mp3",
            self.fileCopier._dropFileProtocol(filePath))

        filePath = "file://localhost/home/rob/music%20exporter%20tests/vari/Suoneria-JJ_E_Samba.mp3"
        self.assertEquals(
            "/home/rob/music exporter tests/vari/Suoneria-JJ_E_Samba.mp3",
            self.fileCopier._dropFileProtocol(filePath))

    def test_sanitizeName_replacesInvalidChars(self):
        self.assertEquals("hello_", self.fileCopier._sanitizeName("hello?"))
        self.assertEquals(
            "he_llo_ my na_me",
            self.fileCopier._sanitizeName("he*llo? my na+me"))

    def test_buildFilePath_constructsCorrectPath(self):
        genre = "house-tribal"
        artist = "Kenny Dope"
        title = "When the morning comes (Kenny Mix)"
        
        expectedPath = self.destination + \
            genre + "/" + artist + " - " + title + ".mp3"
        
        self.assertEquals(
            expectedPath,
            self.fileCopier._buildFilePath(genre, artist, title))

if __name__ == '__main__':
  unittest.main()