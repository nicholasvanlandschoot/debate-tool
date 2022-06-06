import unittest
from src.gdrive import validate


class TestDrive(unittest.TestCase):
    def test_validate(self):
        test = validate()

        self.assertIn("googleapiclient.discovery.Resource object", str(test))


if __name__ == "__main__":
    unittest.main()
