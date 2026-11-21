"""细胞结构渲染测试。"""

import unittest

from plantcell.model import ORGANELLES, CellError, generate_quiz, plant_only_names
from plantcell.render import render_diagram, render_poster, render_worksheet


class DiagramTest(unittest.TestCase):
    def test_svg(self):
        svg = render_diagram()
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn('viewBox="0 0 720 480"', svg)

    def test_badges(self):
        svg = render_diagram()
        self.assertEqual(svg.count('r="13"'), 7)
        for index in range(1, 8):
            self.assertIn(">%d</text>" % index, svg)

    def test_wall_and_membrane(self):
        svg = render_diagram()
        self.assertIn("68d391", svg)
        self.assertIn("4299e1", svg)

    def test_organelles_drawn(self):
        svg = render_diagram()
        self.assertIn("ellipse", svg)
        self.assertIn("circle", svg)

    def test_no_names_in_diagram(self):
        svg = render_diagram()
        for item in ORGANELLES:
            self.assertNotIn(item.name, svg)


class PosterTest(unittest.TestCase):
    def test_skeleton(self):
        page = render_poster()
        self.assertIn("<!DOCTYPE html>", page)
        self.assertTrue(page.rstrip().endswith("</html>"))

    def test_legend_items(self):
        page = render_poster()
        self.assertEqual(page.count('class="item"'), 7)

    def test_names_and_functions(self):
        page = render_poster()
        for item in ORGANELLES:
            self.assertIn(item.name, page)
            self.assertIn(item.description, page)

    def test_location_tags(self):
        page = render_poster()
        for name in plant_only_names():
            self.assertIn(name, page)
        self.assertIn("植物细胞特有", page)

    def test_custom_title(self):
        page = render_poster("七年级细胞结构")
        self.assertIn("七年级细胞结构", page)

    def test_escaping(self):
        page = render_poster("细胞 & 结构")
        self.assertIn("细胞 &amp; 结构", page)

    def test_hint_text(self):
        self.assertIn("叶绿体和液泡", render_poster())


class WorksheetTest(unittest.TestCase):
    def setUp(self):
        self.items = generate_quiz(6, seed=11)

    def test_skeleton(self):
        page = render_worksheet(self.items)
        self.assertIn("<!DOCTYPE html>", page)
        self.assertTrue(page.rstrip().endswith("</html>"))

    def test_cards(self):
        page = render_worksheet(self.items)
        self.assertEqual(page.count('class="card"'), 6)

    def test_word_bank(self):
        page = render_worksheet(self.items)
        self.assertIn("备选词", page)
        for item in ORGANELLES:
            self.assertIn(item.name, page)

    def test_no_answers(self):
        self.assertNotIn("参考答案", render_worksheet(self.items))

    def test_answers(self):
        page = render_worksheet(self.items, answers=True)
        self.assertIn("参考答案", page)
        self.assertEqual(page.count("<tr>"), 7)

    def test_notes_in_answers(self):
        page = render_worksheet(self.items, answers=True)
        self.assertIn("植物细胞特有", page)

    def test_custom_title(self):
        page = render_worksheet(self.items, title="四班细胞")
        self.assertIn("四班细胞", page)

    def test_empty(self):
        with self.assertRaises(CellError):
            render_worksheet([])

    def test_bad_item(self):
        with self.assertRaises(CellError):
            render_worksheet(["细胞核"])

    def test_prompts_present(self):
        page = render_worksheet(self.items)
        for item in self.items:
            self.assertIn(item.prompt, page)


if __name__ == "__main__":
    unittest.main()
