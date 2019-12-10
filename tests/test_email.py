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

  def test_email_with_spaces(self):
    result = MaskEmailAddresses('N o o d l e a n g e l  @ y a h o o . c o m')
    answer = '<blocked email>'
    self.assertEqual(answer, result)
