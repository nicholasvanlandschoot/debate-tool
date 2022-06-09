import unittest
from src.gdrive import validate, ls


class TestDrive(unittest.TestCase):
    def test_validate(self):

        test = validate()

        self.assertIn("googleapiclient.discovery.Resource object", str(test))

    def test_ls(self):
        try:
            validate()
        except:
            return

        test = ls("1vZGvTgbHnOeJmO66wUQJEEucJqbWF9A8")

        self.assertEqual(
            test,
            [
                {
                    "id": "1hnoOVO2689-Zk_P-I_jP41jZmqsg6XCqQKTO21p9TTE",
                    "name": "Another Test",
                },
                {
                    "id": "1rMOVtlP0HcE42qOOgjbhsFDFfBZq8qFD3ZB_3B1IKCI",
                    "name": "Test Doc",
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
