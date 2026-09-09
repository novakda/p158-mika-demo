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

    def test_due_date_shown_and_sorted(self):
        self.run_cmd("add", "no date")
        self.assertEqual(self.run_cmd("add", "later", "--due", "2026-12-01"), "added 2: later (due 2026-12-01)\n")
        self.run_cmd("add", "--due", "2026-01-15", "soon")
        self.run_cmd("add", "also no date")
        self.assertEqual(
            self.run_cmd("list"),
            "  3 [ ] soon (due 2026-01-15)\n"
            "  2 [ ] later (due 2026-12-01)\n"
            "  1 [ ] no date\n"
            "  4 [ ] also no date\n",
        )

    def test_invalid_due_rejected(self):
        for bad in ("2026-13-01", "2026-02-30", "01/02/2026", "tomorrow"):
            with self.assertRaises(SystemExit) as cm:
                self.run_cmd("add", "x", "--due", bad)
            self.assertIn("invalid date", str(cm.exception))
        with self.assertRaises(SystemExit):
            self.run_cmd("add", "x", "--due")
        with self.assertRaises(SystemExit):
            self.run_cmd("add", "--due", "2026-01-01")
        self.assertFalse(os.path.exists(todo.TODO_FILE))

    def test_legacy_file_without_due(self):
        with open(todo.TODO_FILE, "w", encoding="utf-8") as f:
            f.write('[{"id": 1, "text": "old", "done": false}]')
        self.assertEqual(self.run_cmd("list"), "  1 [ ] old\n")
        self.run_cmd("add", "new", "--due", "2026-05-05")
        self.assertEqual(self.run_cmd("list"), "  2 [ ] new (due 2026-05-05)\n  1 [ ] old\n")

    def test_bad_id_and_usage(self):
        with self.assertRaises(SystemExit):
            self.run_cmd("done", "42")
        with self.assertRaises(SystemExit):
            self.run_cmd("bogus")


if __name__ == "__main__":
    unittest.main()
