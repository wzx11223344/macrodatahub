"""
MacroDataHub 使用示例
====================

演示如何获取、清洗和可视化宏观经济数据。
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from macrodatahub import WorldBank, ChinaStats

print("=" * 60)
print("示例 1: 世界银行数据 - 中美 GDP 对比")
print("=" * 60)

wb = WorldBank()

# 获取中美 GDP 数据
gdp = wb.get_indicator("NY.GDP.MKTP.CD", ["CN", "US"], 2010, 2023)
print("\nGDP (现价万亿美元):")
print((gdp / 1e12).round(2).to_string())

# 获取 GDP 增长率和通胀
print("\n" + "=" * 60)
print("示例 2: 中美经济指标对比")
print("=" * 60)

data = wb.get_multiple(
    ["NY.GDP.MKTP.KD.ZG", "FP.CPI.TOTL.ZG", "SL.UEM.TOTL.ZS"],
    ["CN", "US"], 2015, 2023
)

for ind, df in data.items():
    desc = wb.INDICATORS.get(ind, ind)
    print(f"\n{desc}:")
    print(df.round(2).to_string())

# 中国经济数据
print("\n" + "=" * 60)
print("示例 3: 中国经济概览 (内置数据集)")
print("=" * 60)

cn = ChinaStats()
print("\nGDP 概况:")
print(cn.gdp_summary().tail(5).round(2).to_string())

print("\n货币供应量:")
print(cn.money_supply_summary().tail(5).round(2).to_string())

print("\n" + "=" * 60)
print("示例 4: 搜索世界银行指标")
print("=" * 60)
indicators = wb.list_indicators("trade")
for ind in indicators[:5]:
    print(f"  {ind}")
