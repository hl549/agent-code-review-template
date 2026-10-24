import unittest

from analysis import summarize_displacements


class DisplacementTest(unittest.TestCase):
    def test_typical_samples(self):
        self.assertEqual(summarize_displacements([2.0, None, 0.0]), [100.0, 0.0, 0.0])

    def test_empty(self):
        self.assertEqual(summarize_displacements([]), [])


if __name__ == "__main__":
    unittest.main()
