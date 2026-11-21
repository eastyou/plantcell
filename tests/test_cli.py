"""命令行行为测试。"""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from plantcell.cli import main


def run(args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(args)
    return code, out.getvalue(), err.getvalue()


class CliTest(unittest.TestCase):
    def test_help(self):
        with self.assertRaises(SystemExit) as ctx:
            main(["--help"])
        self.assertEqual(ctx.exception.code, 0)

    def test_poster_stdout(self):
        code, out, _ = run(["poster"])
        self.assertEqual(code, 0)
        self.assertIn("<svg", out)

    def test_poster_to_file(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "poster.html"
            code, out, _ = run(["poster", "-o", str(target)])
            self.assertEqual(code, 0)
            self.assertTrue(target.exists())
            self.assertIn("已写入", out)

    def test_show(self):
        code, out, _ = run(["show", "细胞核"])
        self.assertEqual(code, 0)
        self.assertIn("名称：细胞核", out)
        self.assertIn("____", out)

    def test_show_key(self):
        code, out, _ = run(["show", "vacuole"])
        self.assertEqual(code, 0)
        self.assertIn("名称：液泡", out)
        self.assertIn("植物细胞特有", out)

    def test_show_unknown(self):
        code, _, err = run(["show", "细胞壁壁"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)

    def test_list(self):
        code, out, _ = run(["list"])
        self.assertEqual(code, 0)
        self.assertEqual(len(out.strip().splitlines()), 7)
        self.assertIn("1. 细胞壁", out)

    def test_compare(self):
        code, out, _ = run(["compare"])
        self.assertEqual(code, 0)
        self.assertIn("植物细胞特有：细胞壁、叶绿体、液泡", out)
        self.assertIn("细胞膜", out)

    def test_sheet_stdout(self):
        code, out, _ = run(["sheet", "--count", "3", "--seed", "1"])
        self.assertEqual(code, 0)
        self.assertEqual(out.count('class="card"'), 3)

    def test_sheet_answers(self):
        code, out, _ = run(["sheet", "--count", "3", "--seed", "2", "--answers"])
        self.assertEqual(code, 0)
        self.assertIn("参考答案", out)

    def test_sheet_plant_only(self):
        code, out, _ = run(
            ["sheet", "--count", "3", "--plant-only", "--kinds", "blank", "--seed", "3"]
        )
        self.assertEqual(code, 0)
        self.assertEqual(out.count('class="card"'), 3)
        self.assertIn("备选词", out)

    def test_sheet_plant_only_overflow(self):
        code, _, err = run(["sheet", "--count", "7", "--plant-only"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)

    def test_sheet_bad_kind(self):
        code, _, err = run(["sheet", "--kinds", "guess"])
        self.assertEqual(code, 2)
        self.assertIn("题型", err)

    def test_sheet_empty_kinds(self):
        code, _, err = run(["sheet", "--kinds", " , "])
        self.assertEqual(code, 2)
        self.assertIn("题型", err)

    def test_sheet_too_many(self):
        code, _, err = run(["sheet", "--count", "99"])
        self.assertEqual(code, 2)
        self.assertIn("错误", err)

    def test_sheet_to_file(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "sheet.html"
            code, _, _ = run(["sheet", "--count", "4", "--seed", "5", "-o", str(target)])
            self.assertEqual(code, 0)
            self.assertEqual(target.read_text(encoding="utf-8").count('class="card"'), 4)

    def test_nested_output(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "a" / "poster.html"
            code, _, _ = run(["poster", "-o", str(target)])
            self.assertEqual(code, 0)
            self.assertTrue(target.exists())


if __name__ == "__main__":
    unittest.main()
