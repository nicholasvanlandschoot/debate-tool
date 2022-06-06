import unittest
from src.user import URoot

class TestCli(unittest.TestCase):

    def test_root(self):
        tests = [('root -u asdasd', ['root', '-u', 'asdasd'], ['asdasd'], {'-u': 'asdasd'}, ['-u']),
                 ('root -l asdasd', ['root', '-l', 'asdasd'], ['asdasd'], {'-l': 'asdasd'}, ['-l']), 
                 ('root -l asdasd -l', ['root', '-l', 'asdasd', '-l'], ['asdasd'], {'-l': 'asdasd'}, ['-l', '-l'])]
        results = ['-u', 'asdasd', 'asdasd']
        
        for i, y in zip(tests, results):
            self.assertEqual(URoot(i), y)

if __name__ == "__main__":
    unittest.main()

