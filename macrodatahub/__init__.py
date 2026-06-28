"""
MacroDataHub — 全球宏观经济数据自动化工具
========================================

一键获取、清洗、可视化全球宏观经济数据，支持：
- 世界银行 (World Bank) API
- IMF 国际货币基金组织数据
- FRED (美联储经济数据库)
- 中国国家统计局常用指标

提供统一接口，返回 pandas DataFrame，无缝对接计量分析流程。
"""

from .wb import WorldBank
from .fred import FRED
from .china import ChinaStats
from .utils import merge_datasets, resample_to_quarterly, resample_to_annual

__version__ = "1.0.0"
__author__ = "wzx11223344"
__all__ = ["WorldBank", "FRED", "ChinaStats", "merge_datasets", "resample_to_quarterly", "resample_to_annual"]
