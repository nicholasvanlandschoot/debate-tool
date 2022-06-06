import unittest
from src.storage import store_root

class TestStorage(unittest.TestCase):

    def test_store_root(self):
        test1 = store_root('123456I')
        test2 = store_root('')
        self.assertEqual(test1, '{"root": "123456I"}')
        self.assertEqual(test2, '{"root": ""}')

if __name__ == "__main__":
    unittest.main()
