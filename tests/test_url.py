import unittest

from mask import *

class TestCases(unittest.TestCase):

  def test_url_full(self):
    result = MaskUrls('http://www.wordpicker.net/index')
    answer = '<blocked url>'
    self.assertEqual(answer, result)

  def test_url_regular(self):
    result = MaskUrls('www.wordpicker.net/index')
    answer = '<blocked url>'
    self.assertEqual(answer, result)

  def test_url_facebook(self):
    result = MaskUrls('https://www.facebook.com/nawtyemoboy?ref=tn_tnmn')
    answer = '<blocked url>'+'?ref=tn_tnmn'
    self.assertEqual(answer, result)
    result = MaskUrls('https://www.facebook.com/ahmed.mohsen.92317')
    answer = '<blocked url>'
    self.assertEqual(answer, result)
