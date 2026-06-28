"""
FRED (Federal Reserve Economic Data) 模块
=========================================

通过 FRED API 获取美国宏观经济时序数据。
需要免费的 FRED API Key (https://fred.stlouisfed.org/docs/api/api_key.html)。

也可以用环境变量 FRED_API_KEY 或直接传入。
"""

import pandas as pd
import requests
from typing import Optional, List
import os


FRED_SERIES = {
    # GDP & 增长
    "GDP":          "国内生产总值 (十亿美元)",
    "GDPC1":        "实际 GDP (十亿美元, 2017年价)",
    "GDPPOT":       "潜在 GDP",
    # 价格
    "CPIAUCSL":     "CPI (城市消费者, 1982-84=100)",
    "CPILFESL":     "核心 CPI (不含食品能源)",
    "PCEPI":        "PCE 价格指数",
    "PCEPILFE":     "核心 PCE (美联储关注)",
    # 就业
    "UNRATE":       "失业率 (%)",
    "PAYEMS":       "非农就业人数 (千人)",
    "JTSJOL":       "JOLTS 职位空缺 (千人)",
    # 利率
    "FEDFUNDS":     "联邦基金利率 (%)",
    "DGS10":        "10年期国债收益率 (%)",
    "DGS2":         "2年期国债收益率 (%)",
    "T10Y2Y":       "10Y-2Y 利差 (%)",
    "DFF":          "有效联邦基金利率 (%)",
    # 货币与金融
    "M2SL":         "M2 货币供应量 (十亿美元)",
    "WM2NS":        "M2 货币供应量 (周度)",
    "TOTALSL":      "消费者信贷总额",
    # 贸易
    "BOPGSTB":      "贸易差额 (百万美元)",
    # 房地产
    "HOUST":        "新屋开工 (千套)",
    "MSPUS":        "房价中位数 (美元)",
    # 工业生产
    "INDPRO":       "工业生产力指数",
    "TCU":          "产能利用率 (%)",
    # 消费者
    "UMCSENT":      "密歇根消费者信心指数",
    "RSAFS":        "零售销售额 (百万美元)",
}


class FRED:
    """FRED 数据获取器。"""

    BASE_URL = "https://api.stlouisfed.org/fred"

    def __init__(self, api_key: Optional[str] = None):
        """
        参数
        ----
        api_key : str, optional
            FRED API Key。如不提供，从环境变量 FRED_API_KEY 读取。
        """
        self.api_key = api_key or os.environ.get("FRED_API_KEY", "")
        if not self.api_key:
            print("⚠ 未设置 FRED_API_KEY。部分功能不可用。")
            print("  免费获取: https://fred.stlouisfed.org/docs/api/api_key.html")

    def _request(self, endpoint: str, **params) -> dict:
        params["api_key"] = self.api_key
        params["file_type"] = "json"
        resp = requests.get(f"{self.BASE_URL}/{endpoint}", params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_series(self, series_id: str,
                   start_date: str = "2000-01-01",
                   end_date: str = "2024-12-31") -> pd.DataFrame:
        """
        获取单个时序数据。

        参数
        ----
        series_id : str
            FRED 序列代码，如 "GDP", "UNRATE"。
        start_date, end_date : str
            YYYY-MM-DD 格式。

        返回
        ----
        pd.DataFrame, columns = [series_id], index = date
        """
        data = self._request("series/observations",
                             series_id=series_id,
                             observation_start=start_date,
                             observation_end=end_date,
                             sort_order="asc")

        observations = data.get("observations", [])
        dates, values = [], []
        for obs in observations:
            if obs["value"] == ".":
                continue
            dates.append(obs["date"])
            values.append(float(obs["value"]))

        df = pd.DataFrame({series_id: values}, index=pd.to_datetime(dates))
        df.index.name = "date"
        return df

    def get_multiple(self, series_ids: List[str],
                     start_date: str = "2000-01-01",
                     end_date: str = "2024-12-31") -> pd.DataFrame:
        """
        批量获取多个时序，合并为一张表。
        """
        result = pd.DataFrame()
        for sid in series_ids:
            df = self.get_series(sid, start_date, end_date)
            result[sid] = df[sid]
        return result

    def get_us_macro_dashboard(self) -> pd.DataFrame:
        """一键获取美国宏观经济仪表板数据。"""
        key_series = [
            "GDPC1", "UNRATE", "CPIAUCSL", "FEDFUNDS",
            "DGS10", "M2SL", "INDPRO", "UMCSENT"
        ]
        return self.get_multiple(key_series)

    def search_series(self, keyword: str, limit: int = 10) -> pd.DataFrame:
        """搜索 FRED 序列。"""
        data = self._request("series/search", search_text=keyword, limit=limit)
        results = []
        for s in data.get("seriess", []):
            results.append({
                "id": s["id"],
                "title": s["title"],
                "frequency": s.get("frequency_short", ""),
                "units": s.get("units_short", ""),
                "popularity": s.get("popularity", 0),
            })
        return pd.DataFrame(results)
