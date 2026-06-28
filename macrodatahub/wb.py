"""
World Bank API 数据获取模块
===========================

通过 World Bank API v2 获取各国宏观经济指标。
覆盖 GDP、通胀、贸易、人口等 1000+ 指标。

无需 API Key。
"""

import pandas as pd
import requests
from typing import List, Optional, Dict
import time


# 常用世界银行指标
INDICATORS = {
    # GDP & 增长
    "NY.GDP.MKTP.CD":   "GDP (现价美元)",
    "NY.GDP.MKTP.KD.ZG": "GDP 年增长率 (%)",
    "NY.GDP.PCAP.CD":   "人均 GDP (现价美元)",
    "NY.GDP.PCAP.KD.ZG": "人均 GDP 年增长率 (%)",
    # 通胀
    "FP.CPI.TOTL.ZG":   "CPI 通胀率 (%)",
    "NY.GDP.DEFL.KD.ZG":"GDP 平减指数 (%)",
    # 贸易
    "NE.EXP.GNFS.ZS":   "出口占 GDP (%)",
    "NE.IMP.GNFS.ZS":   "进口占 GDP (%)",
    "BN.CAB.XOKA.GD.ZS":"经常账户余额占 GDP (%)",
    # 人口与就业
    "SP.POP.TOTL":      "总人口",
    "SP.POP.GROW":      "人口增长率 (%)",
    "SL.UEM.TOTL.ZS":   "失业率 (%)",
    # 财政与金融
    "GC.DOD.TOTL.GD.ZS":"中央政府债务占 GDP (%)",
    "GC.TAX.TOTL.GD.ZS":"税收占 GDP (%)",
    "PA.NUS.FCRF":      "官方汇率 (本币/USD)",
    # 发展
    "SE.ADT.LITR.ZS":   "识字率 (%)",
    "IT.NET.USER.ZS":   "互联网使用率 (%)",
    "EG.USE.ELEC.KH.PC":"人均用电量 (kWh)",
}

# 常用国家/地区代码
COUNTRIES = {
    "CN": "中国", "US": "美国", "JP": "日本", "DE": "德国",
    "GB": "英国", "FR": "法国", "IN": "印度", "BR": "巴西",
    "RU": "俄罗斯", "KR": "韩国", "AU": "澳大利亚", "CA": "加拿大",
    "WLD": "世界", "EUU": "欧盟",
}


class WorldBank:
    """世界银行数据获取器。"""

    BASE_URL = "https://api.worldbank.org/v2"

    def __init__(self):
        self._cache = {}

    def get_indicator(self, indicator: str, countries: Optional[List[str]] = None,
                      start_year: int = 2000, end_year: int = 2024) -> pd.DataFrame:
        """
        获取指定指标的数据。

        参数
        ----
        indicator : str
            指标代码，如 "NY.GDP.MKTP.CD"。
        countries : list of str, optional
            国家代码列表，默认 ["CN", "US", "JP", "WLD"]。
        start_year, end_year : int

        返回
        ----
        pd.DataFrame, columns = countries, index = year
        """
        if countries is None:
            countries = ["CN", "US", "JP", "DE", "WLD"]

        country_str = ";".join(countries)
        url = (f"{self.BASE_URL}/country/{country_str}"
               f"/indicator/{indicator}"
               f"?format=json&per_page=5000"
               f"&date={start_year}:{end_year}")

        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise ConnectionError(f"World Bank API 请求失败: {e}")

        if len(data) < 2 or data[1] is None:
            return pd.DataFrame()

        records = data[1]
        result = {}
        for rec in records:
            if rec["value"] is None:
                continue
            year = int(rec["date"])
            country = rec["countryiso3code"]
            result.setdefault(country, {})[year] = float(rec["value"])

        df = pd.DataFrame(result).sort_index()
        df.index.name = "year"
        return df

    def get_multiple(self, indicators: List[str], countries: Optional[List[str]] = None,
                     start_year: int = 2000, end_year: int = 2024) -> Dict[str, pd.DataFrame]:
        """
        批量获取多个指标。

        返回
        ----
        Dict[str, pd.DataFrame]
        """
        results = {}
        for i, ind in enumerate(indicators):
            name = INDICATORS.get(ind, ind)
            print(f"  [{i+1}/{len(indicators)}] 获取 {name}...")
            results[ind] = self.get_indicator(ind, countries, start_year, end_year)
            if i < len(indicators) - 1:
                time.sleep(0.1)  # API 限速
        return results

    def get_country_profile(self, country: str) -> pd.DataFrame:
        """
        获取一个国家的主要经济指标概况。

        参数
        ----
        country : str
            国家代码，如 "CN"。

        返回
        ----
        pd.DataFrame
        """
        key_indicators = [
            "NY.GDP.MKTP.CD", "NY.GDP.MKTP.KD.ZG", "NY.GDP.PCAP.CD",
            "FP.CPI.TOTL.ZG", "SL.UEM.TOTL.ZS",
            "NE.EXP.GNFS.ZS", "BN.CAB.XOKA.GD.ZS",
            "GC.DOD.TOTL.GD.ZS", "SP.POP.TOTL",
        ]
        data = self.get_multiple(key_indicators, [country])
        result = pd.DataFrame()
        for ind, df in data.items():
            if not df.empty:
                result[INDICATORS.get(ind, ind)] = df.iloc[:, 0]
        return result

    def list_indicators(self, search: str = "") -> List[str]:
        """搜索指标代码。"""
        matches = []
        for code, desc in INDICATORS.items():
            if search.lower() in code.lower() or search.lower() in desc.lower():
                matches.append(f"{code}: {desc}")
        return matches
