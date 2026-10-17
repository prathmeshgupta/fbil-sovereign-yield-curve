"""
Automated Weekly Dataset Updater for fbil-sovereign-yield-curve
Can be executed locally or via GitHub Actions.
Zero credentials required.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from fbil_sovereign_yield.fetcher import SovereignYieldFetcher

OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = OUTPUT_DIR / "sovereign_yield_curve.csv"
PARQUET_FILE = OUTPUT_DIR / "sovereign_yield_curve.parquet"


def update():
    print("[1/3] Fetching sovereign yield curve and T-bill primary auction benchmarks...")
    fetcher = SovereignYieldFetcher()
    df = fetcher.fetch_yield_curve()
    print(f"      Retrieved {len(df)} sovereign yield observations.")

    print("[2/3] Saving yield curve dataset...")
    df.to_csv(CSV_FILE, index=False)
    df.to_parquet(PARQUET_FILE, index=False)
    print(f"      Saved {len(df)} records to {CSV_FILE.name} and {PARQUET_FILE.name}.")

    print("[3/3] Running automated quality audit...")
    from evaluate_quality import audit_quality
    audit_quality()
    print("Update complete successfully.")


if __name__ == "__main__":
    update()
