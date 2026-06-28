"""
数据处理工具函数
================

提供数据合并、频率转换等常用操作。
"""

import pandas as pd
import numpy as np
from typing import List, Optional


def merge_datasets(*dfs: pd.DataFrame, how: str = "outer") -> pd.DataFrame:
    """
    按索引合并多个数据集。

    参数
    ----
    *dfs : pd.DataFrame
        多个 DataFrame，按索引对齐合并。
    how : str
        合并方式: "inner", "outer" (默认)

    返回
    ----
    pd.DataFrame
    """
    if not dfs:
        return pd.DataFrame()
    result = dfs[0]
    for i, df in enumerate(dfs[1:], 1):
        result = result.join(df, how=how, rsuffix=f"_{i}")
    return result


def resample_to_quarterly(df: pd.DataFrame, method: str = "mean") -> pd.DataFrame:
    """
    将月度/日度数据重采样为季度。

    参数
    ----
    df : pd.DataFrame
        需要有 DatetimeIndex。
    method : str
        "mean", "sum", "last" 等。

    返回
    ----
    pd.DataFrame
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("DataFrame 需要有 DatetimeIndex")
    resampler = df.resample("QE")
    if method == "sum":
        return resampler.sum()
    elif method == "last":
        return resampler.last()
    else:
        return resampler.mean()


def resample_to_annual(df: pd.DataFrame, method: str = "mean") -> pd.DataFrame:
    """
    将月度/季度数据重采样为年度。

    参数
    ----
    df : pd.DataFrame
    method : str

    返回
    ----
    pd.DataFrame
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("DataFrame 需要有 DatetimeIndex")
    resampler = df.resample("YE")
    if method == "sum":
        return resampler.sum()
    elif method == "last":
        return resampler.last()
    else:
        return resampler.mean()


def growth_rate(series: pd.Series, periods: int = 1) -> pd.Series:
    """
    计算同比增长率。

    参数
    ----
    series : pd.Series
    periods : int
        滞后周期数。

    返回
    ----
    pd.Series
    """
    return series.pct_change(periods) * 100


def yoy_growth(series: pd.Series) -> pd.Series:
    """
    计算同比 (Year-over-Year) 增长率。
    适用于月度或季度数据，比较 12 个月或 4 个季度前。
    """
    return series.pct_change(12) * 100


def moving_average(series: pd.Series, window: int = 4) -> pd.Series:
    """移动平均。"""
    return series.rolling(window=window).mean()
