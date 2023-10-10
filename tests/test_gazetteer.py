import unittest

from gazetteer import *


class TestCases(unittest.TestCase):
    def test_exact(self):
        answer = GazLocation("Canterbury, Kent, England, United Kingdom")
        result = [120216, 5698790, "Europe/London"]
        self.assertEqual(answer, result)

    def test_matches_quick(self):
        answer = GazClosestMatchesQuick("Canter", 5)
        result = [
            "Canterbury, Kent, England, United Kingdom",
            "Canterwood, Pierce County, Washington, United States",
            "Canterbury, Merrimack County, New Hampshire, United States",
            "Christchurch, Christchurch City, Canterbury, New Zealand",
            "Ashburton, Ashburton District, Canterbury, New Zealand",
        ]
        self.assertEqual(answer, result)

    def test_matches(self):
        answer = GazClosestMatches("Canter", 5)
        result = [
            "Christchurch, Christchurch City, Canterbury, New Zealand",
            "Canterbury, Kent, England, United Kingdom",
            "Ashburton, Ashburton District, Canterbury, New Zealand",
            "Timaru, Timaru District, Canterbury, New Zealand",
            "Kaiapoi, Waimakariri District, Canterbury, New Zealand",
        ]
        self.assertEqual(answer, result)

    def test_placename_1(self):
        answer = GazPlacename("Canterbury, Kent, England, United Kingdom", "Whistable, Kent, England, United Kingdom")
        result = "Canterbury"
        self.assertEqual(answer, result)

    def test_placename_2(self):
        answer = GazPlacename("Canterbury, Kent, England, United Kingdom", "Manchester, England, United Kingdom")
        result = "Canterbury, Kent"
        self.assertEqual(answer, result)

    def test_placename_3(self):
        answer = GazPlacename(
            "Canterbury, Kent, England, United Kingdom", "Livingston, West Lothian, Scotland, United Kingdom"
        )
        result = "Canterbury, Kent, England"
        self.assertEqual(answer, result)

    def test_placename_4(self):
        answer = GazPlacename("Canterbury, Kent, England, United Kingdom", "Dakar, Senegal")
        result = "Canterbury, Kent, England, United Kingdom"
        self.assertEqual(answer, result)


if __name__ == "__main__":
    unittest.main()
