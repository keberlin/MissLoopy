import unittest

from mask import *

class TestCases(unittest.TestCase):

  def test_email_regular(self):
    result = MaskEmailAddresses('keith.hollis@gmail.com')
    answer = '<blocked email address>'
    self.assertEqual(answer, result)

  def test_email_at(self):
    result = MaskEmailAddresses('keith.hollis at gmail.com')
    answer = '<blocked email address>'
    self.assertEqual(answer, result)
    result = MaskEmailAddresses('keith.hollis(at)gmail.com')
    answer = '<blocked email address>'
    self.assertEqual(answer, result)

  def test_email_no_extension(self):
    result = MaskEmailAddresses('keith.hollis@gmail')
    answer = '<blocked email address>'
    self.assertEqual(answer, result)
    result = MaskEmailAddresses('keith.hollis at yahoo')
    answer = '<blocked email address>'
    self.assertEqual(answer, result)

  def test_email_split_domain(self):
    result = MaskEmailAddresses('keith.hollis g/m/a/i/l/c/o/m')
    answer = '<blocked email address>'
    self.assertEqual(answer, result)
    result = MaskEmailAddresses('keith.hollis f.a.c.e.b.o.o.k.c.o.m')
    answer = '<blocked email address>'
    self.assertEqual(answer, result)

  def test_email_abbv_domain(self):
    result = MaskEmailAddresses('keith.hollis@yaho')
    answer = '<blocked email address>'
    self.assertEqual(answer, result)
    result = MaskEmailAddresses('keith.hollis@yah')
    answer = '<blocked email address>'
    self.assertEqual(answer, result)

  def test_email_zeros(self):
    result = MaskEmailAddresses('keith.hollis@yah00.com')
    answer = '<blocked email address>'
    self.assertEqual(answer, result)
