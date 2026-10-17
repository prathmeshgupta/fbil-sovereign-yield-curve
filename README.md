# Indian Sovereign Yield Curve & Term Structure Dataset

[![Weekly Update](https://github.com/prathmeshgupta/fbil-sovereign-yield-curve/actions/workflows/update.yml/badge.svg)](https://github.com/prathmeshgupta/fbil-sovereign-yield-curve/actions/workflows/update.yml)
[![Format: Parquet](https://img.shields.io/badge/Format-Apache%20Parquet-blue.svg)](output/sovereign_yield_curve.parquet)
[![Format: CSV](https://img.shields.io/badge/Format-CSV-green.svg)](output/sovereign_yield_curve.csv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An institutional quantitative dataset capturing the **Indian Sovereign Yield Curve**, Treasury Bill (91D, 182D, 364D) primary auction cutoff yields, the 10-Year Benchmark Government of India (G-Sec) bond yield, policy Repo Rates, and term structure spreads ($10Y - 91D$).

In institutional asset allocation and equity factor modeling, sovereign term spreads serve as the primary macro regime filter for business cycle expansion versus monetary tightening.

---

## Dataset Schema (`output/sovereign_yield_curve.parquet` / `.csv`)

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `trade_date` | `string` | ISO-8601 Primary Auction / Policy Date (`YYYY-MM-DD`) |
| `rbi_repo_rate` | `float64` | Reserve Bank of India Benchmark Policy Repo Rate (%) |
| `tbill_91d` | `float64` | 91-Day Treasury Bill primary auction cut-off yield (%) |
| `tbill_182d` | `float64` | 182-Day Treasury Bill primary auction cut-off yield (%) |
| `tbill_364d` | `float64` | 364-Day Treasury Bill primary auction cut-off yield (%) |
| `gsec_10y` | `float64` | 10-Year Benchmark Government of India Bond Yield (%) |
| `term_spread_10y_91d` | `float64` | Term Spread ($10\text{Y G-Sec} - 91\text{D T-Bill}$) in percentage points |
| `term_spread_10y_364d` | `float64` | Term Spread ($10\text{Y G-Sec} - 364\text{D T-Bill}$) in percentage points |
| `curve_regime` | `string` | Macro yield curve regime (`STEEP_EXPANSION`, `NORMAL_UPWARD`, `FLATTENING`, `INVERTED_RECESSION`) |
| `source` | `string` | Provenance identifier (`RBI_PRIMARY_AUCTION_BENCHMARKS`) |

---

## Quick Start (Python / Polars / DuckDB)

```python
import polars as pl

# Read directly from GitHub Raw Parquet
url = "https://github.com/prathmeshgupta/fbil-sovereign-yield-curve/raw/main/output/sovereign_yield_curve.parquet"
df = pl.read_parquet(url)

# Display latest term structure
print(df.select(["trade_date", "rbi_repo_rate", "tbill_91d", "gsec_10y", "term_spread_10y_91d", "curve_regime"]))
```
