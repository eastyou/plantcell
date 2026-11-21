"""细胞结构的数据模型。"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Optional, Sequence

KINDS = ("function", "blank")


class CellError(ValueError):
    """细胞结构相关的输入错误。"""


@dataclass(frozen=True)
class Organelle:
    """细胞中的一个结构。"""

    key: str
    name: str
    description: str
    clue: str
    in_plant: bool
    in_animal: bool

    def __post_init__(self) -> None:
        if not self.key or not self.name:
            raise CellError("结构必须有键和名称")
        if not self.clue:
            raise CellError("%s 缺少提示句" % self.name)
        if self.clue.count(self.name) != 1:
            raise CellError("%s 的提示句必须恰好包含一次名称" % self.name)
        if not self.in_plant and not self.in_animal:
            raise CellError("%s 至少要存在于一种细胞中" % self.name)

    @property
    def plant_only(self) -> bool:
        """是否只存在于植物细胞。"""
        return self.in_plant and not self.in_animal

    @property
    def blank_clue(self) -> str:
        """把名称挖空的提示句。"""
        return self.clue.replace(self.name, "____")

    @property
    def location(self) -> str:
        """存在范围的中文描述。"""
        if self.plant_only:
            return "植物细胞特有"
        if self.in_plant and self.in_animal:
            return "动植物细胞都有"
        return "动物细胞特有"


ORGANELLES = (
    Organelle(
        "cell_wall",
        "细胞壁",
        "位于细胞最外层，起支持和保护作用。",
        "位于细胞最外层、起支持和保护作用的结构是细胞壁。",
        True,
        False,
    ),
    Organelle(
        "cell_membrane",
        "细胞膜",
        "紧贴细胞壁内侧，控制物质进出细胞。",
        "紧贴细胞壁内侧、控制物质进出的结构是细胞膜。",
        True,
        True,
    ),
    Organelle(
        "cytoplasm",
        "细胞质",
        "充满细胞内部的胶状物质，多种生命活动在这里进行。",
        "充满细胞内部、多种生命活动在此进行的胶状物质是细胞质。",
        True,
        True,
    ),
    Organelle(
        "nucleus",
        "细胞核",
        "含有遗传物质，是细胞的控制中心。",
        "含有遗传物质、被称为细胞控制中心的结构是细胞核。",
        True,
        True,
    ),
    Organelle(
        "chloroplast",
        "叶绿体",
        "进行光合作用，把光能转变成化学能。",
        "能把光能转变成化学能、进行光合作用的结构是叶绿体。",
        True,
        False,
    ),
    Organelle(
        "vacuole",
        "液泡",
        "储存水分和营养物质，维持细胞的形态。",
        "储存水分和营养物质、维持细胞形态的结构是液泡。",
        True,
        False,
    ),
    Organelle(
        "mitochondrion",
        "线粒体",
        "分解有机物释放能量，被称为细胞的“动力车间”。",
        "分解有机物释放能量、被称为细胞“动力车间”的结构是线粒体。",
        True,
        True,
    ),
)

ORGANELLE_MAP = {item.key: item for item in ORGANELLES}


def organelle_names() -> List[str]:
    """按顺序返回全部结构名称。"""
    return [item.name for item in ORGANELLES]


def plant_only_names() -> List[str]:
    """返回植物细胞特有的结构名称。"""
    return [item.name for item in ORGANELLES if item.plant_only]


def shared_names() -> List[str]:
    """返回动植物细胞共有的结构名称。"""
    return [item.name for item in ORGANELLES if item.in_plant and item.in_animal]


def get_organelle(value: str) -> Organelle:
    """按名称或键查找结构。"""
    if not isinstance(value, str):
        raise CellError("结构必须是字符串")
    text = value.strip()
    if not text:
        raise CellError("结构不能为空")
    for item in ORGANELLES:
        if text == item.name or text == item.key:
            return item
    raise CellError("未知结构：%s" % text)


@dataclass(frozen=True)
class CellQuiz:
    """一道细胞结构练习题。"""

    organelle_key: str
    kind: str

    def __post_init__(self) -> None:
        if self.organelle_key not in ORGANELLE_MAP:
            raise CellError("未知结构：%s" % self.organelle_key)
        if self.kind not in KINDS:
            raise CellError("题型只能是 function 或 blank")

    @property
    def organelle(self) -> Organelle:
        """题目对应的结构。"""
        return ORGANELLE_MAP[self.organelle_key]

    @property
    def prompt(self) -> str:
        """题干文本。"""
        if self.kind == "blank":
            return self.organelle.blank_clue
        return self.organelle.description

    @property
    def answer(self) -> str:
        """标准答案。"""
        return self.organelle.name

    @property
    def note(self) -> str:
        """补充说明。"""
        return self.organelle.location


def generate_quiz(
    count: int = 6,
    kinds: Sequence[str] = KINDS,
    seed: Optional[int] = None,
    plant_only: bool = False,
) -> List[CellQuiz]:
    """随机生成不重复的细胞结构题。"""
    if isinstance(count, bool) or not isinstance(count, int):
        raise CellError("题目数量必须是整数")
    if count < 1:
        raise CellError("题目数量至少为 1")
    chosen = list(kinds)
    if not chosen:
        raise CellError("至少需要一种题型")
    for kind in chosen:
        if kind not in KINDS:
            raise CellError("未知题型：%s" % kind)
    pool = [item for item in ORGANELLES if item.plant_only] if plant_only else list(ORGANELLES)
    if plant_only and not pool:
        raise CellError("没有植物细胞特有的结构")
    capacity = len(pool) * len(chosen)
    if count > capacity:
        raise CellError("题目数量不能超过 %d" % capacity)

    combos = [(item.key, kind) for kind in chosen for item in pool]
    rng = random.Random(seed)
    rng.shuffle(combos)
    return [CellQuiz(key, kind) for key, kind in combos[:count]]


def check_answer(item: CellQuiz, answer: str) -> bool:
    """判断作答是否正确。"""
    if not isinstance(item, CellQuiz):
        raise CellError("题目必须是 CellQuiz")
    if not isinstance(answer, str):
        raise CellError("答案必须是字符串")
    return item.answer == answer.strip()
