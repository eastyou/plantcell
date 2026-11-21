"""命令行入口。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .model import (
    KINDS,
    CellError,
    generate_quiz,
    get_organelle,
    organelle_names,
    plant_only_names,
    shared_names,
)
from .render import render_poster, render_worksheet


def build_parser() -> argparse.ArgumentParser:
    """构造命令行解析器。"""
    parser = argparse.ArgumentParser(
        prog="plantcell",
        description="细胞结构：标注挂图、结构查询与练习纸",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    poster = subparsers.add_parser("poster", help="输出植物细胞标注图 HTML")
    poster.add_argument("--title", default="植物细胞结构", help="挂图标题")
    poster.add_argument("-o", "--output", default=None, help="输出文件")

    show = subparsers.add_parser("show", help="查询一个结构")
    show.add_argument("organelle", help="结构名称或键，如 细胞核 或 nucleus")

    subparsers.add_parser("list", help="列出全部结构")
    subparsers.add_parser("compare", help="列出植物特有与共有结构")

    sheet = subparsers.add_parser("sheet", help="生成 A4 练习纸")
    sheet.add_argument("--count", type=int, default=6, help="题目数量，默认 6")
    sheet.add_argument("--kinds", default=",".join(KINDS), help="题型，逗号分隔：function、blank")
    sheet.add_argument("--plant-only", action="store_true", help="只练植物细胞特有的结构")
    sheet.add_argument("--seed", type=int, default=None, help="随机种子")
    sheet.add_argument("--title", default="细胞结构练习", help="练习纸标题")
    sheet.add_argument("--answers", action="store_true", help="追加参考答案")
    sheet.add_argument("-o", "--output", default=None, help="输出文件")
    return parser


def _write_output(text: str, output: Optional[str]) -> None:
    if not output:
        print(text)
        return
    path = Path(output)
    if path.parent and str(path.parent) not in ("", "."):
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("已写入 %s" % path)


def _parse_kinds(text: str) -> List[str]:
    parts = [part.strip() for part in text.split(",") if part.strip()]
    if not parts:
        raise CellError("至少需要一种题型")
    return parts


def main(argv: Optional[List[str]] = None) -> int:
    """命令行主函数，返回进程退出码。"""
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "poster":
            _write_output(render_poster(args.title), args.output)
            return 0
        if args.command == "show":
            item = get_organelle(args.organelle)
            print("名称：%s" % item.name)
            print("功能：%s" % item.description)
            print("分布：%s" % item.location)
            print("提示：%s" % item.blank_clue)
            return 0
        if args.command == "list":
            for index, name in enumerate(organelle_names(), 1):
                item = get_organelle(name)
                print("%d. %s（%s）：%s" % (index, item.name, item.location, item.description))
            return 0
        if args.command == "compare":
            print("植物细胞特有：%s" % "、".join(plant_only_names()))
            print("动植物细胞都有：%s" % "、".join(shared_names()))
            return 0
        items = generate_quiz(
            args.count, _parse_kinds(args.kinds), args.seed, args.plant_only
        )
        _write_output(render_worksheet(items, args.title, args.answers), args.output)
        return 0
    except CellError as exc:
        print("错误：%s" % exc, file=sys.stderr)
        return 2
    except OSError as exc:
        print("写入失败：%s" % exc, file=sys.stderr)
        return 1
