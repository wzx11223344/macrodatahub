# MacroDataHub — 全球宏观经济数据自动化工具

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![pandas](https://img.shields.io/badge/dependency-pandas-150458.svg)](https://pandas.pydata.org/)

**一键获取、清洗、分析全球宏观经济数据**，为经济学研究和计量分析提供统一的数据接口。

## ✨ 特性

- 🌍 **多源数据**: 世界银行 1000+ 指标、FRED 美国经济数据、中国宏观数据
- 📊 **统一接口**: 全部返回 pandas DataFrame，无缝对接计量分析流程
- 🇨🇳 **中国数据**: 内置近 24 年中国关键经济指标
- 🔧 **数据处理**: 频率转换、同比/环比计算、多源数据合并
- 🆓 **零成本**: 世界银行 API 无需 Key，中国数据本地内置

## 📦 安装

```bash
pip install macrodatahub
```

## 🚀 快速开始

```python
from macrodatahub import WorldBank, ChinaStats

# 世界银行数据
wb = WorldBank()
gdp = wb.get_indicator("NY.GDP.MKTP.CD", ["CN", "US"], 2010, 2023)
print(gdp / 1e12)  # 万亿美元

# 中国经济数据
cn = ChinaStats()
print(cn.gdp_summary().tail())
```

## 📚 数据源

| 模块 | 数据源 | 指标数 | 需要 Key |
|------|--------|--------|---------|
| `WorldBank` | World Bank API v2 | 1000+ | ❌ |
| `FRED` | Federal Reserve Economic Data | 800,000+ | ✅ (免费) |
| `ChinaStats` | 内置数据集 | 7 个核心指标 | ❌ |

## 📖 使用示例

```python
from macrodatahub import WorldBank

wb = WorldBank()

# 批量获取多国多指标
data = wb.get_multiple(
    ["NY.GDP.MKTP.KD.ZG", "FP.CPI.TOTL.ZG", "SL.UEM.TOTL.ZS"],
    ["CN", "US", "JP", "DE"], 2015, 2023
)

# 获取一国经济概况
cn_profile = wb.get_country_profile("CN")
print(cn_profile)
```

## 📄 许可证

MIT License © 2024 wzx11223344
