"""细胞结构模型测试。"""

import unittest

from plantcell.model import (
    KINDS,
    ORGANELLES,
    ORGANELLE_MAP,
    CellError,
    CellQuiz,
    check_answer,
    generate_quiz,
    get_organelle,
    organelle_names,
    plant_only_names,
    shared_names,
)


class OrganelleDataTest(unittest.TestCase):
    """逐一检查七个细胞结构的数据。"""


def _make_data_test(item):
    def test(self):
        self.assertTrue(item.key)
        self.assertTrue(item.name)
        self.assertTrue(item.description)
        self.assertEqual(item.clue.count(item.name), 1)
        self.assertEqual(item.blank_clue.count("____"), 1)
        self.assertNotIn(item.name, item.blank_clue)
        self.assertIn(item.location, ("植物细胞特有", "动植物细胞都有", "动物细胞特有"))

    test.__doc__ = "%s 的数据完整性" % item.name
    return test


for _item in ORGANELLES:
    setattr(OrganelleDataTest, "test_%s" % _item.key, _make_data_test(_item))


class PlantOnlyTest(unittest.TestCase):
    def test_plant_only_flags(self):
        self.assertEqual(set(plant_only_names()), {"细胞壁", "叶绿体", "液泡"})

    def test_plant_only_count(self):
        self.assertEqual(len(plant_only_names()), 3)

    def test_plant_only_property(self):
        for item in ORGANELLES:
            self.assertEqual(
                item.plant_only,
                item.in_plant and not item.in_animal,
            )


class SharedTest(unittest.TestCase):
    def test_shared_names(self):
        self.assertEqual(set(shared_names()), {"细胞膜", "细胞质", "细胞核", "线粒体"})

    def test_shared_count(self):
        self.assertEqual(len(shared_names()), 4)

    def test_total_count(self):
        self.assertEqual(len(ORGANELLES), 7)
        self.assertEqual(len(set(organelle_names())), 7)
        self.assertEqual(len(ORGANELLE_MAP), 7)

    def test_location_text(self):
        self.assertEqual(get_organelle("叶绿体").location, "植物细胞特有")
        self.assertEqual(get_organelle("细胞核").location, "动植物细胞都有")


class LookupTest(unittest.TestCase):
    def test_by_name(self):
        self.assertEqual(get_organelle("细胞核").key, "nucleus")

    def test_by_key(self):
        self.assertEqual(get_organelle("vacuole").name, "液泡")

    def test_strip(self):
        self.assertEqual(get_organelle(" 线粒体 ").key, "mitochondrion")

    def test_unknown(self):
        with self.assertRaises(CellError):
            get_organelle("细胞壁壁")

    def test_empty(self):
        with self.assertRaises(CellError):
            get_organelle("   ")

    def test_not_string(self):
        with self.assertRaises(CellError):
            get_organelle(7)  # type: ignore[arg-type]


class QuizTest(unittest.TestCase):
    def test_function_prompt(self):
        item = CellQuiz("nucleus", "function")
        self.assertEqual(item.prompt, get_organelle("nucleus").description)
        self.assertEqual(item.answer, "细胞核")

    def test_blank_prompt(self):
        item = CellQuiz("chloroplast", "blank")
        self.assertIn("____", item.prompt)
        self.assertNotIn("叶绿体", item.prompt)
        self.assertEqual(item.answer, "叶绿体")

    def test_note(self):
        self.assertEqual(CellQuiz("vacuole", "blank").note, "植物细胞特有")

    def test_bad_key(self):
        with self.assertRaises(CellError):
            CellQuiz("cell_walll", "blank")

    def test_bad_kind(self):
        with self.assertRaises(CellError):
            CellQuiz("nucleus", "guess")

    def test_frozen(self):
        item = CellQuiz("nucleus", "blank")
        with self.assertRaises(AttributeError):
            item.kind = "function"  # type: ignore[misc]


class GenerateTest(unittest.TestCase):
    def test_count(self):
        self.assertEqual(len(generate_quiz(6, seed=1)), 6)

    def test_unique(self):
        items = generate_quiz(10, seed=2)
        keys = [(item.organelle_key, item.kind) for item in items]
        self.assertEqual(len(keys), len(set(keys)))

    def test_single_kind(self):
        items = generate_quiz(7, ["blank"], seed=3)
        self.assertTrue(all(item.kind == "blank" for item in items))

    def test_all_covered(self):
        items = generate_quiz(7, ["function"], seed=4)
        self.assertEqual({item.organelle_key for item in items}, set(ORGANELLE_MAP))

    def test_plant_only(self):
        items = generate_quiz(3, ["blank"], seed=5, plant_only=True)
        self.assertTrue(all(get_organelle(item.organelle_key).plant_only for item in items))

    def test_seed_reproducible(self):
        self.assertEqual(generate_quiz(6, seed=6), generate_quiz(6, seed=6))

    def test_seed_differs(self):
        self.assertNotEqual(generate_quiz(6, seed=6), generate_quiz(6, seed=7))

    def test_zero_count(self):
        with self.assertRaises(CellError):
            generate_quiz(0)

    def test_bool_count(self):
        with self.assertRaises(CellError):
            generate_quiz(True)

    def test_empty_kinds(self):
        with self.assertRaises(CellError):
            generate_quiz(3, [])

    def test_bad_kind(self):
        with self.assertRaises(CellError):
            generate_quiz(3, ["guess"])

    def test_too_many(self):
        with self.assertRaises(CellError):
            generate_quiz(15, ["blank"])

    def test_too_many_plant_only(self):
        with self.assertRaises(CellError):
            generate_quiz(7, ["blank"], plant_only=True)

    def test_capacity(self):
        self.assertEqual(len(generate_quiz(14, seed=8)), 14)

    def test_kinds_constant(self):
        self.assertEqual(set(KINDS), {"function", "blank"})


class AnswerTest(unittest.TestCase):
    def test_correct(self):
        self.assertTrue(check_answer(CellQuiz("nucleus", "blank"), "细胞核"))

    def test_strip(self):
        self.assertTrue(check_answer(CellQuiz("nucleus", "blank"), " 细胞核 "))

    def test_incorrect(self):
        self.assertFalse(check_answer(CellQuiz("nucleus", "blank"), "细胞质"))

    def test_bad_item(self):
        with self.assertRaises(CellError):
            check_answer("nucleus", "细胞核")

    def test_bad_answer(self):
        with self.assertRaises(CellError):
            check_answer(CellQuiz("nucleus", "blank"), 3)


if __name__ == "__main__":
    unittest.main()
