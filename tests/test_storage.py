import unittest
from src.storage import store_root, objects, objects_all
from src.storage import DriveObject


class TestStorage(unittest.TestCase):
    def test_store_root(self):
        test1 = store_root("123456I")
        test2 = store_root(" ")
        self.assertEqual(test1, "123456I")
        self.assertEqual(test2, " ")

    def test_DriveObjectinit(self):
        obj = DriveObject("testname", "testid", "testpath")

        self.assertEqual(objects_all[len(objects_all) - 1], obj)

        self.assertIn(obj.name, objects["name"].keys())
        self.assertIn(obj.id, objects["id"].keys())
        self.assertIn(obj.path, objects["path"].keys())

    #! must be dependent on init
    def test_DriveObjectforget(self):
        obj = DriveObject("testname", "testid", "testpath")
        obj._forget()

        self.assertNotIn(obj, objects_all)

        self.assertNotIn(obj.name, objects["name"])
        self.assertNotIn(obj.id, objects["id"])
        self.assertNotIn(obj.path, objects["path"])


if __name__ == "__main__":
    unittest.main()
