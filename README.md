# <img src="https://img.icons8.com/color/48/data-configuration.png" width="32" /> MacroDataHub

<p align="center">
  <b>全球宏观经济数据自动化获取、清洗与可视化工具 — 一站式数据管道</b>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"></a>
  <a href="https://pypi.org/project/macrodatahub/"><img src="https://img.shields.io/badge/pypi-v1.0.0-blue?logo=pypi&logoColor=white" alt="PyPI"></a>
  <a href="https://github.com/wzx11223344/macrodatahub"><img src="https://img.shields.io/badge/stars-%E2%98%85%E2%98%85%E2%98%85-yellow?logo=github" alt="GitHub Stars"></a>
  <a href="https://pandas.pydata.org/"><img src="https://img.shields.io/badge/pandas-%E2%9C%93-150458?logo=pandas&logoColor=white" alt="pandas"></a>
</p>

---

## 目录

- [简介](#简介)
- [安装](#-安装)
- [快速开始](#-快速开始)
- [API 参考](#-api-参考)
- [数据源详解](#-数据源详解)
- [数据处理工具](#-数据处理工具)
- [使用场景](#-使用场景)
- [参考文档](#-参考文档)
- [贡献指南](#-贡献指南)
- [参考文献](#-参考文献)
- [许可证](#-许可证)

---

## 简介

**MacroDataHub** 是一个全球宏观经济数据的统一获取接口。通过抽象层封装世界银行、美联储 FRED 和中国国家统计局三大核心数据源，所有调用返回标准化的 pandas DataFrame，可直接接入计量分析工作流（如 pyconometrics、statsmodels、linearmodels）。

**设计哲学：**
- 一行代码获取跨源、跨国的经济面板数据
- 统一 DataFrame 输出格式，跨数据源无缝合并
- FRED 数据实时在线获取 + 中国数据本地内置（零延迟）
- 世界银行 API 零配置、零认证

---

## 安装

```bash
# PyPI 安装
pip install macrodatahub

# 开发者安装
git clone https://github.com/wzx11223344/macrodatahub.git
cd macrodatahub
pip install -e .
```

**依赖:** Python 3.8+ / pandas >= 1.3 / requests >= 2.25

---

## 快速开始

### 1. 获取多国 GDP 数据

```python
from macrodatahub import WorldBank

wb = WorldBank()
gdp = wb.get_indicator("NY.GDP.MKTP.CD", ["CN", "US", "JP", "DE", "GB"], 2010, 2023)
print(gdp / 1e12)  # 万亿美元
```

### 2. 中国经济概况 (内置数据集)

```python
from macrodatahub import ChinaStats

cn = ChinaStats()
print(cn.gdp_summary().tail(8))

# 通货膨胀
print(cn.cpi().tail(12))     # CPI 同比
print(cn.ppi().tail(12))     # PPI 同比

# 消费与投资
print(cn.retail_sales())     # 社会消费品零售总额
print(cn.fixed_investment()) # 固定资产投资
```

### 3. FRED 美国经济数据

```python
from macrodatahub import FRED

fred = FRED(api_key="YOUR_FRED_API_KEY")  # 免费注册: https://fred.stlouisfed.org/docs/api/api_key.html

# 常用美联储指标
gdp_us = fred.get_series("GDP")             # 美国 GDP
cpi_us = fred.get_series("CPIAUCSL")        # CPI 物价指数
unemp = fred.get_series("UNRATE")           # 失业率
ffr = fred.get_series("DFF")                # 联邦基金利率

# 获取多个系列的合并面板
data = fred.get_multiple(["GDP", "UNRATE", "DFF"], start="2010-01-01")
print(data.tail())
```

### 4. 跨数据源合并

```python
from macrodatahub import WorldBank, ChinaStats, merge_datasets

wb_gdp = WorldBank().get_indicator("NY.GDP.MKTP.KD.ZG", ["CN", "US"], 2000, 2023)
cn_infl = ChinaStats().cpi()

# 合并 + 重采样
combined = merge_datasets([wb_gdp, cn_infl], how="outer")
print(combined.head())
```

---

## API 参考

### 数据获取类

| 类名 | 描述 | 认证 | 指标数 |
|------|------|:---:|:---:|
| `WorldBank()` | 世界银行开放数据 | None | 1,400+ |
| `FRED(api_key)` | 美联储经济数据库 | API Key (免费) | 823,000+ |
| `ChinaStats()` | 中国宏观经济本地数据集 | None | 7 核心指标 |

### WorldBank API

| 方法 | 描述 | 返回 |
|------|------|------|
| `get_indicator(code, countries, start, end)` | 单指标跨国获取 | pandas DataFrame |
| `get_multiple(codes, countries, start, end)` | 多指标批量获取 | pandas DataFrame |
| `get_country_profile(code)` | 一国全部经济指标概览 | pandas DataFrame |
| `search_indicator(keyword)` | 按关键词搜索指标 | list of dicts |
| `available_countries()` | 列出所有可用国家 | list |

### FRED API

| 方法 | 描述 | 返回 |
|------|------|------|
| `get_series(series_id, start, end)` | 获取单个时间序列 | pandas Series |
| `get_multiple(series_ids, start, end)` | 批量获取多序列 | pandas DataFrame |
| `search(term)` | 搜索 FRED 序列 | list of dicts |
| `series_info(series_id)` | 序列元数据 | dict |

### ChinaStats API

| 属性/方法 | 描述 | 频率 | 覆盖期 |
|------|------|:---:|:---:|
| `gdp_summary()` | GDP 总量、增速、第一/二/三产业 | 年/季 | 2000-至今 |
| `cpi()` | 居民消费价格指数 (同比) | 月 | 2000-至今 |
| `ppi()` | 工业生产者出厂价格指数 (同比) | 月 | 2000-至今 |
| `m2()` | 广义货币供应量 M2 | 月 | 2000-至今 |
| `retail_sales()` | 社会消费品零售总额 | 月 | 2000-至今 |
| `fixed_investment()` | 固定资产投资 | 月 | 2000-至今 |
| `trade_balance()` | 进出口贸易差额 | 月 | 2000-至今 |
| `unemployment()` | 城镇调查失业率 | 月 | 2018-至今 |
| `pmi()` | 制造业 PMI | 月 | 2005-至今 |

---

## 数据源详解

### 世界银行 (World Bank API v2)

- **协议**: RESTful API, JSON 返回
- **覆盖**: 266 个经济体, 1,400+ 指标, 1960-至今
- **调用限制**: 无认证限制 (建议每次请求 < 60 个指标)
- **常用指标代码**: `NY.GDP.MKTP.CD` (名义GDP), `FP.CPI.TOTL.ZG` (通胀), `SL.UEM.TOTL.ZS` (失业率), `NE.EXP.GNFS.ZS` (出口占比)

### 美联储 FRED

- **注册**: https://fred.stlouisfed.org/docs/api/api_key.html (即时免费)
- **覆盖**: 823,000+ 美国和国际经济时间序列
- **更新频率**: 数据实时更新, 日内可查
- **常用序列**: `GDP`, `CPIAUCSL`, `UNRATE`, `DFF`, `M2SL`, `INDPRO`, `PAYEMS`, `HOUST`

### 中国统计数据

- **数据来源**: 国家统计局 (NBS) 公开发布的月度/季度/年度数据
- **更新方式**: 内置数据集，随 package 版本更新，零网络请求
- **数据处理**: 已完成缺失值插补和频率统一

---

## 数据处理工具

| 函数 | 描述 |
|------|------|
| `merge_datasets(*dfs, how)` | 合并多个 DataFrame (pandas merge/join) |
| `resample_to_quarterly(df)` | 重采样为季度频率 (取均值 / 末值) |
| `resample_to_annual(df)` | 重采样为年度频率 |
| `yoy_change(series)` | 计算同比增长率 |
| `mom_change(series)` | 计算环比增长率 |
| `real_gdp(nominal, deflator, base_year)` | 名义 GDP 转实际 GDP |

---

## 使用场景

### 场景 1: 跨国经济增长对比

```python
from macrodatahub import WorldBank

wb = WorldBank()
gdp_growth = wb.get_indicator("NY.GDP.MKTP.KD.ZG", ["CN", "US", "IN", "VN"], 2000, 2023)
gdp_growth.plot(title="Real GDP Growth Rate (%)")
```

### 场景 2: 构建计量模型的特征矩阵

```python
from macrodatahub import ChinaStats
import numpy as np

cn = ChinaStats()
gdp = cn.gdp_summary()["gdp_yoy"]       # GDP 增速
cpi = cn.cpi()                            # CPI
m2 = cn.m2()                              # M2
pmi = cn.pmi()                            # PMI

# 对齐时间索引, 构建 N x 4 特征矩阵
X = np.column_stack([gdp, cpi, m2, pmi])
# 接入 pyconometrics / statsmodels, 运行:
# from pyconometrics import OLS
# model = OLS(y, X, var_names=["gdp", "cpi", "m2", "pmi"])
```

### 场景 3: FRED 数据 + 中国数据合并分析

```python
from macrodatahub import ChinaStats, FRED, merge_datasets

cn_ppi = ChinaStats().ppi()
us_cpi = FRED("YOUR_KEY").get_series("CPIAUCSL")

global_inflation = merge_datasets([cn_ppi.rename("CN_PPI"), us_cpi.rename("US_CPI")])
```

---

## 参考文档

- [世界银行 API 文档](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-api)
- [FRED API 文档](https://fred.stlouisfed.org/docs/api/fred/)
- [中国国家统计局](http://www.stats.gov.cn/)
- [IMF Data Mapper](https://www.imf.org/en/Data)

---

## 贡献指南

欢迎贡献新数据源和功能！

- **新数据源**: Eurostat API, IMF IFS API, OECD API
- **新功能**: 季节调整 (X-13ARIMA-SEATS), 插值方法, 面板数据导出
- **Bug 报告**: [GitHub Issues](https://github.com/wzx11223344/macrodatahub/issues)

开发环境:
```bash
git clone https://github.com/wzx11223344/macrodatahub.git
cd macrodatahub
pip install -e .
```

---

## 参考文献

1. **World Bank (2024).** *World Development Indicators.* https://databank.worldbank.org/source/world-development-indicators
2. **Federal Reserve Bank of St. Louis (2024).** *FRED Economic Data.* https://fred.stlouisfed.org/
3. **National Bureau of Statistics of China (2024).** *China Statistical Yearbook.* http://www.stats.gov.cn/
4. **IMF (2024).** *International Financial Statistics.* https://data.imf.org/

---

## 许可证

本项目基于 [MIT License](LICENSE) 发布。Copyright &copy; 2024 wzx11223344.
