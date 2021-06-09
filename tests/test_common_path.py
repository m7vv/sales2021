import unittest
from sales import create_app


class TestEntryFile(unittest.TestCase):

    def test_config(self):
        self.assertFalse(create_app().testing)
        self.assertTrue(create_app({'TESTING': True}).testing)

    def test_about(self):
        app = create_app({'TESTING': True})
        response = app.test_client().get('/about')
        self.assertEqual(response.data, b'This is pet project')


if __name__ == '__main__':
    unittest.main()
