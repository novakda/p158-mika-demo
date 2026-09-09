import contextlib
import io
import os
import tempfile
import unittest

import todo


class TodoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        todo.TODO_FILE = os.path.join(self.tmp.name, "todo.json")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cmd(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            todo.main(list(argv))
        return out.getvalue()

    def test_empty_file(self):
        self.assertEqual(self.run_cmd("list"), "")
        self.assertFalse(os.path.exists(todo.TODO_FILE))

    def test_add_and_list(self):
        self.assertEqual(self.run_cmd("add", "buy milk"), "added 1: buy milk\n")
        self.run_cmd("add", "walk", "dog")
        self.assertEqual(self.run_cmd("list"), "  1 [ ] buy milk\n  2 [ ] walk dog\n")

    def test_done(self):
        self.run_cmd("add", "a")
        self.assertEqual(self.run_cmd("done", "1"), "done 1\n")
        self.assertEqual(self.run_cmd("list"), "  1 [x] a\n")

    def test_remove(self):
        self.run_cmd("add", "a")
        self.run_cmd("add", "b")
        self.assertEqual(self.run_cmd("remove", "1"), "remove 1\n")
        self.assertEqual(self.run_cmd("list"), "  2 [ ] b\n")
        self.assertEqual(self.run_cmd("add", "c"), "added 3: c\n")

    def test_bad_id_and_usage(self):
        with self.assertRaises(SystemExit):
            self.run_cmd("done", "42")
        with self.assertRaises(SystemExit):
            self.run_cmd("bogus")


if __name__ == "__main__":
    unittest.main()
