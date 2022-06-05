import unittest
from src.cli import parse


class TestCli(unittest.TestCase):

    def test_parse(self):
        str, splitted, args, argdict, flags = parse("command -f flag independentArg -independentFlag")
        
        self.assertEqual(str, "command -f flag independentArg -independentFlag")
        self.assertEqual(splitted, ["command", "-f", "flag", "independentArg", "-independentFlag"])
        self.assertEqual(args, ["flag", "independentArg"])
        self.assertEqual(argdict, {"-f": "flag"})
        self.assertEqual(flags, ["-f", "-independentFlag"])

if __name__ == "__main__":
    unittest.main()
