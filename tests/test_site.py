import unittest

from mask import *

class TestCases(unittest.TestCase):

  def test_site_regular(self):
    result = MaskSites('www.wordpicker.net')
    answer = '<blocked website>'
    self.assertEqual(answer, result)
