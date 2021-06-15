import unittest
from sales import create_app


class TestEntryFile(unittest.TestCase):
    """common test cases """

    def test_config(self):
        self.assertFalse(create_app().testing)
        self.assertTrue(create_app({'TESTING': True}).testing)


if __name__ == '__main__':
    unittest.main()
