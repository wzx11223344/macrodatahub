"""
中国宏观经济数据模块
====================

提供中国常用宏观经济指标的本地数据集和简易查询接口。
数据来源: 国家统计局年度公报、Wind 公开数据。

内置近 10 年中国关键经济指标，开箱即用。
"""

import pandas as pd
import numpy as np
from typing import Optional


# 内置中国宏观经济数据 (2000-2023)
# 来源: 国家统计局, World Bank
_CHINA_DATA = {
    "year": list(range(2000, 2024)),
    "gdp": [100280, 110863, 121717, 137422, 161840, 187319, 219439, 270092,
            319245, 348518, 412119, 487940, 538580, 592963, 643563, 688858,
            746395, 832036, 919281, 986515, 1013567, 1149237, 1204724, 1260582],
    "gdp_growth": [8.5, 8.3, 9.1, 10.0, 10.1, 11.4, 12.7, 14.2, 9.7, 9.4,
                   10.6, 9.6, 7.9, 7.8, 7.4, 7.0, 6.8, 6.9, 6.7, 6.0,
                   2.2, 8.4, 3.0, 5.2],
    "cpi": [0.4, 0.7, -0.8, 1.2, 3.9, 1.8, 1.5, 4.8, 5.9, -0.7,
            3.3, 5.4, 2.6, 2.6, 2.0, 1.4, 2.0, 1.6, 2.1, 2.9,
            2.5, 0.9, 2.0, 0.2],
    "unemployment_urban": [3.1, 3.6, 4.0, 4.3, 4.2, 4.2, 4.1, 4.0, 4.2, 4.3,
                           4.1, 4.1, 4.1, 4.1, 4.1, 4.1, 4.0, 3.9, 3.8, 3.6,
                           4.2, 4.0, 4.4, 5.1],
    "exports_usd": [249.2, 266.1, 325.6, 438.2, 593.3, 762.0, 968.9, 1220.5,
                    1430.7, 1201.6, 1577.8, 1898.4, 2048.9, 2209.0, 2342.3,
                    2273.5, 2097.6, 2263.3, 2486.7, 2498.6,
                    2590.6, 3364.0, 3583.6, 3380.0],
    "m2": [13.46, 15.83, 18.50, 22.12, 25.32, 29.88, 34.56, 40.34,
           47.52, 60.62, 72.59, 85.16, 97.41, 110.65, 122.84, 139.23,
           155.01, 167.68, 182.67, 198.65,
           218.68, 238.29, 266.43, 292.27],
    "fiscal_revenue": [1.34, 1.64, 1.89, 2.17, 2.64, 3.16, 3.88, 5.13,
                       6.13, 6.85, 8.31, 10.39, 11.72, 12.92, 14.04, 15.22,
                       15.96, 17.26, 18.34, 19.04,
                       18.29, 20.25, 20.37, 21.68],
}


class ChinaStats:
    """中国宏观经济数据查询。"""

    def __init__(self):
        self._df = pd.DataFrame(_CHINA_DATA).set_index("year")
        self._df.index.name = "year"

    def get_all(self) -> pd.DataFrame:
        """获取全部内置数据。

        返回
        ----
        pd.DataFrame
        """
        return self._df.copy()

    def get_indicator(self, name: str) -> pd.Series:
        """
        获取单个指标。

        参数
        ----
        name : str
            指标名称: "gdp", "gdp_growth", "cpi", "unemployment_urban",
            "exports_usd", "m2", "fiscal_revenue"

        返回
        ----
        pd.Series
        """
        if name not in self._df.columns:
            available = list(self._df.columns)
            raise KeyError(f"未知指标 '{name}'。可用指标: {available}")
        return self._df[name].copy()

    def gdp_summary(self) -> pd.DataFrame:
        """GDP 概览: GDP 总量、增长率、人均 GDP。"""
        df = self._df[["gdp", "gdp_growth"]].copy()
        df["gdp_per_capita"] = df["gdp"] * 1000 / 1400  # 近似人均 (元)
        df["gdp_trillion"] = df["gdp"] / 10000
        return df

    def inflation_summary(self) -> pd.DataFrame:
        """通胀概览。"""
        return self._df[["cpi"]].copy()

    def trade_summary(self) -> pd.DataFrame:
        """贸易概览。"""
        df = self._df[["exports_usd"]].copy()
        df["exports_growth"] = df["exports_usd"].pct_change() * 100
        return df

    def money_supply_summary(self) -> pd.DataFrame:
        """货币供应概览。"""
        df = self._df[["m2"]].copy()
        df["m2_growth"] = df["m2"].pct_change() * 100
        return df
