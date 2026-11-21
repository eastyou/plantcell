"""细胞结构示意图与练习纸渲染。"""

from __future__ import annotations

import html
from typing import List, Sequence

from .model import ORGANELLES, CellError, CellQuiz

_POSITIONS = {
    "cell_wall": (96, 64),
    "cell_membrane": (120, 104),
    "cytoplasm": (180, 402),
    "nucleus": (250, 210),
    "chloroplast": (392, 134),
    "vacuole": (478, 270),
    "mitochondrion": (618, 332),
}


def _badge(index: int, key: str) -> str:
    x, y = _POSITIONS[key]
    return (
        '<g><circle cx="%d" cy="%d" r="13" fill="#ffffff" stroke="#2b6cb0" stroke-width="2"/>'
        '<text x="%d" y="%d" font-size="13" text-anchor="middle" fill="#2b6cb0" '
        'font-family="Helvetica, Arial, sans-serif">%d</text></g>' % (x, y, x, y + 5, index)
    )


def render_diagram() -> str:
    """绘制植物细胞结构示意图。"""
    parts: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 480" width="100%" '
        'role="img" aria-label="植物细胞结构示意图">',
        "<title>植物细胞结构示意图</title>",
        '<rect x="0" y="0" width="720" height="480" fill="#ffffff"/>',
        '<rect x="60" y="40" width="600" height="400" rx="30" fill="#f0fff4" '
        'stroke="#68d391" stroke-width="16"/>',
        '<rect x="78" y="58" width="564" height="364" rx="22" fill="#fefcbf" '
        'fill-opacity="0.55" stroke="#4299e1" stroke-width="4"/>',
        '<circle cx="250" cy="210" r="72" fill="#bee3f8" stroke="#3182ce" stroke-width="3"/>',
        '<circle cx="250" cy="210" r="24" fill="#63b3ed"/>',
        '<ellipse cx="470" cy="270" rx="125" ry="90" fill="#bee3f8" fill-opacity="0.55" '
        'stroke="#63b3ed" stroke-width="3"/>',
        '<g fill="#68d391" stroke="#2f855a" stroke-width="2">',
        '<ellipse cx="160" cy="340" rx="34" ry="18" transform="rotate(-20 160 340)"/>',
        '<ellipse cx="392" cy="134" rx="34" ry="18" transform="rotate(15 392 134)"/>',
        '<ellipse cx="560" cy="164" rx="30" ry="16" transform="rotate(-10 560 164)"/>',
        "</g>",
        '<g fill="#f6ad55" stroke="#c05621" stroke-width="2">',
        '<ellipse cx="616" cy="330" rx="38" ry="20" transform="rotate(18 616 330)"/>',
        '<ellipse cx="200" cy="120" rx="30" ry="16" transform="rotate(-15 200 120)"/>',
        "</g>",
        '<path d="M598,322 q10,8 20,0 q10,-8 20,0" fill="none" stroke="#c05621" '
        'stroke-width="2"/>',
        '<path d="M186,114 q8,7 16,0 q8,-7 16,0" fill="none" stroke="#c05621" '
        'stroke-width="2"/>',
    ]
    for index, item in enumerate(ORGANELLES, 1):
        parts.append(_badge(index, item.key))
    parts.append("</svg>")
    return "\n".join(parts)


_CSS = """
@page { size: A4; margin: 12mm; }
* { box-sizing: border-box; }
body { margin: 0; font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
       color: #1f2933; background: #fff; }
.sheet { padding: 4mm; }
h1 { margin: 0 0 2mm; font-size: 22px; text-align: center; letter-spacing: 2px; }
.meta { margin: 0 0 4mm; text-align: center; color: #616e7c; font-size: 12px; }
.diagram { border: 1px solid #cbd2d9; border-radius: 3mm; overflow: hidden; }
.legend { display: grid; grid-template-columns: 1fr 1fr; gap: 2mm 5mm; margin-top: 4mm; }
.legend .item { font-size: 13px; line-height: 1.6; }
.legend .no { display: inline-block; width: 20px; height: 20px; line-height: 20px;
              text-align: center; border-radius: 50%; background: #2b6cb0; color: #fff;
              font-size: 12px; margin-right: 2mm; }
.tag { display: inline-block; margin-left: 2mm; padding: 0 2mm; border-radius: 2mm;
       background: #c6f6d5; color: #22543d; font-size: 11px; }
.cards { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }
.card { border: 1px solid #cbd2d9; border-radius: 3mm; padding: 4mm; page-break-inside: avoid; }
.prompt { font-size: 15px; line-height: 1.7; margin: 0 0 3mm; }
.answer-line { border-bottom: 1px dashed #9aa5b1; height: 28px; }
.answers { page-break-before: always; margin-top: 6mm; }
.answers h2 { font-size: 18px; border-left: 4px solid #2f855a; padding-left: 3mm; color: #276749; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td { border: 1px solid #cbd2d9; padding: 2mm 3mm; text-align: left; }
th { background: #f5f7fa; }
@media print { .sheet { padding: 0; } }
""".strip()


def render_poster(title: str = "植物细胞结构") -> str:
    """生成可打印的细胞结构挂图。"""
    legend = "\n".join(
        '<div class="item"><span class="no">%d</span><strong>%s</strong>'
        '<span class="tag">%s</span><br>%s</div>'
        % (index, html.escape(item.name), html.escape(item.location), html.escape(item.description))
        for index, item in enumerate(ORGANELLES, 1)
    )
    return "\n".join(
        [
            "<!DOCTYPE html>",
            '<html lang="zh-CN"><head><meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            "<title>%s</title>" % html.escape(title),
            "<style>%s</style></head><body>" % _CSS,
            '<main class="sheet">',
            "<h1>%s</h1>" % html.escape(title),
            '<p class="meta">对照编号认识细胞结构，注意叶绿体和液泡是植物细胞特有的。</p>',
            '<section class="diagram">%s</section>' % render_diagram(),
            '<section class="legend">%s</section>' % legend,
            "</main></body></html>",
        ]
    )


def render_worksheet(
    items: Sequence[CellQuiz],
    title: str = "细胞结构练习",
    answers: bool = False,
) -> str:
    """生成可打印的细胞结构练习纸。"""
    problems = list(items)
    if not problems:
        raise CellError("至少需要一道题")
    for item in problems:
        if not isinstance(item, CellQuiz):
            raise CellError("题目必须是 CellQuiz")

    cards = [
        '<div class="card"><p class="prompt">%d. %s</p><div class="answer-line"></div></div>'
        % (index, html.escape(item.prompt))
        for index, item in enumerate(problems, 1)
    ]

    bank = "　".join(html.escape(name) for name in [item.name for item in ORGANELLES])
    sections = [
        "<!DOCTYPE html>",
        '<html lang="zh-CN"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>%s</title>" % html.escape(title),
        "<style>%s</style></head><body>" % _CSS,
        '<main class="sheet">',
        "<h1>%s</h1>" % html.escape(title),
        '<p class="meta">姓名：__________　班级：__________　日期：__________</p>',
        '<p class="meta">备选词：%s</p>' % bank,
        '<section class="cards">',
        "\n".join(cards),
        "</section>",
    ]

    if answers:
        rows = [
            "<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td></tr>"
            % (index, html.escape(item.prompt), html.escape(item.answer), html.escape(item.note))
            for index, item in enumerate(problems, 1)
        ]
        sections.append(
            '<section class="answers"><h2>参考答案</h2>'
            "<table><thead><tr><th>题号</th><th>题目</th><th>答案</th><th>说明</th></tr></thead>"
            "<tbody>%s</tbody></table></section>" % "\n".join(rows)
        )

    sections.append("</main></body></html>")
    return "\n".join(sections)
