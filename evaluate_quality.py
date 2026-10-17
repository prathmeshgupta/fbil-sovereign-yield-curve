import re
import pandas as pd
from pathlib import Path

ISO_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def audit_quality():
    print("=" * 65)
    print(" SOVEREIGN YIELD CURVE & TERM SPREADS - DATA QUALITY AUDIT")
    print("=" * 65)

    root = Path(__file__).parent
    pq_path = root / "output" / "sovereign_yield_curve.parquet"
    csv_path = root / "output" / "sovereign_yield_curve.csv"

    assert pq_path.exists(), "sovereign_yield_curve.parquet missing"
    assert csv_path.exists(), "sovereign_yield_curve.csv missing"

    df_pq = pd.read_parquet(pq_path)
    df_csv = pd.read_csv(csv_path)

    # 1. Parity Check
    assert len(df_pq) == len(df_csv), f"Parity mismatch: Parquet ({len(df_pq)}) != CSV ({len(df_csv)})"
    print(f"Total Yield Curve Observations: {len(df_pq)} [PASS - 100% Parity]")

    # 2. Null Checks
    null_count = df_pq.isnull().sum().sum()
    assert null_count == 0, f"Found {null_count} nulls across table"
    print("Null Values: 0 across all columns [100% COMPLETE]")

    # 3. ISO-8601 Format
    s = df_pq["trade_date"].astype(str)
    invalid = s[~s.str.match(ISO_REGEX)]
    assert len(invalid) == 0, f"Non-ISO dates detected: {len(invalid)}"
    print("ISO-8601 Compliance (trade_date): 100% PASS")

    # 4. Domain Microstructure Invariants
    rate_cols = ["rbi_repo_rate", "tbill_91d", "tbill_182d", "tbill_364d", "gsec_10y"]
    for rc in rate_cols:
        assert (df_pq[rc] > 0).all(), f"Non-positive rates in {rc}"
    print("Non-Negative Yield Invariants: [PASS]")

    # 5. Arithmetic Identity
    computed_spread = (df_pq["gsec_10y"] - df_pq["tbill_91d"]).round(2)
    assert (df_pq["term_spread_10y_91d"] == computed_spread).all(), "Spread math mismatch"
    print("Term Spread Math Identity (10Y - 91D): [PASS]")

    # 6. Regime Distribution
    print("\nYield Curve Regime Distribution:")
    for reg, cnt in df_pq["curve_regime"].value_counts().items():
        print(f"  • {reg:<22}: {cnt:>4} periods")

    print("=" * 65)
    print("ALL AUDIT CHECKS PASSED.")
    print("=" * 65)


if __name__ == "__main__":
    audit_quality()
