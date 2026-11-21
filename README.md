# plantcell

[![CI](https://github.com/eastyou/plantcell/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/plantcell/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)

把植物细胞画成带编号的标注图，配上结构功能表与挖空练习，帮助学生分清动植物细胞共有的结构和植物细胞特有的结构。

## 安装

```bash
pip install -e .
```

只需要 Python 3.9+，零第三方依赖。

## 用法

```bash
# 生成植物细胞标注挂图
plantcell poster -o poster.html

# 列出全部结构
plantcell list
# 1. 细胞壁（植物细胞特有）：位于细胞最外层，起支持和保护作用。
# ...

# 对比植物特有与共有结构
plantcell compare
# 植物细胞特有：细胞壁、叶绿体、液泡
# 动植物细胞都有：细胞膜、细胞质、细胞核、线粒体

# 查询单个结构
plantcell show 细胞核

# 生成 6 道混合练习，附答案
plantcell sheet --count 6 --seed 1 --answers -o sheet.html

# 只练植物细胞特有的结构
plantcell sheet --count 6 --plant-only -o plant-only.html
```

## 功能

- SVG 植物细胞示意图：细胞壁、细胞膜、细胞质、细胞核、叶绿体、液泡、线粒体
- 七个结构统一编号，图例给出功能与存在范围
- 两种题型：看功能写名称、句子挖空
- 支持只练植物细胞特有的结构
- 动植物细胞共有 / 植物特有自动区分
- 题目去重，随机种子可复现
- A4 打印排版，答案单独一页

## 测试

```bash
python -m unittest discover -s tests -v
```

## 许可

[MIT](LICENSE) © 2026 eastyou
