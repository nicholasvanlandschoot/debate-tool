import unittest
from src.cli import parse, cd, ls


class TestCli(unittest.TestCase):
    def test_parse(self):
        str, splitted, args, argdict, flags = parse(
            "command -f flag independentArg -independentFlag"
        )

        self.assertEqual(str, "command -f flag independentArg -independentFlag")
        self.assertEqual(
            splitted, ["command", "-f", "flags", "independentArg", "-independentFlag"]
        )
        self.assertEqual(args, ["flag", "independentArg"])
        self.assertEqual(argdict, {"-f": "flag"})
        self.assertEqual(flags, ["-f", "-independentFlag"])

    def test_cd(self):
        self.assertEqual(cd("root"), None)

    def test_ls(self):
        self.assertEqual(ls("root"), None)


if __name__ == "__main__":
    unittest.main()
