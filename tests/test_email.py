import unittest

from mask import *

class TestCases(unittest.TestCase):

  def test_email(self):
    result = MaskEmailAddresses('keith.hollis@gmail.com')
    answer = '<blocked email>'
    self.assertEqual(answer, result)
    result = MaskEmailAddresses('keith.hollis@gmail.co.in')
    answer = '<blocked email>'
    self.assertEqual(answer, result)
