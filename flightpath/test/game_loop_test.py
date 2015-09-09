import unittest

class TestGameLoop(unittest.TestCase):

  def test_canary(self):
    self.assertEqual(1, 2)
    self.assertTrue(2 == 2)
    self.assertFalse(1 == 2)
    with self.assertRaises(AssertionError):
      self.assertEqual(1, 2)

if __name__ == '__main__':
    unittest.main()
