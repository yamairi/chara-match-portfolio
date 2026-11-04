from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from chara_match.pipeline import run_pipeline
from chara_match.config import PRODUCT_COLS, CHARACTER_SUPPORT_COLS

def main():
    parser = argparse.ArgumentParser(description="Run the synthetic CHARA MATCH demonstration")
    parser.add_argument("--n-products", type=int, default=len(PRODUCT_COLS))
    parser.add_argument("--n-characters", type=int, default=len(CHARACTER_SUPPORT_COLS))
    parser.add_argument("--output-dir", type=Path, default=REPO / "outputs_demo")
    args = parser.parse_args()
    if not 1 <= args.n_products <= len(PRODUCT_COLS):
        parser.error("Product count is outside the demo configuration")
    if not 1 <= args.n_characters <= len(CHARACTER_SUPPORT_COLS):
        parser.error("Character count is outside the demo configuration")
    df = pd.read_csv(REPO / "sample_data/synthetic_demo.csv")
    result = run_pipeline(df, PRODUCT_COLS[:args.n_products], CHARACTER_SUPPORT_COLS[:args.n_characters])
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    for key, filename in {
        "model_summary": "model_summary", "gap_long": "product_cluster_gap",
        "product_vectors": "product_vectors", "character_vectors": "character_vectors",
        "pair_scores": "pair_scores", "customer_shift_long": "customer_shift_long",
    }.items():
        result[key].to_csv(out / f"{filename}.csv", index=False)
    for key in ["thresholds", "cluster_diagnostics", "market_vector"]:
        (out / f"{key}.json").write_text(json.dumps(result[key], ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    top = result["pair_scores"].nlargest(10, "expansion_m30").sort_values("expansion_m30")
    labels = top.product_variable + " / " + top.character_variable
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.barh(labels, top.expansion_m30, color="#277e96")
    ax.set_xlabel("Expansion score (synthetic data only)")
    ax.set_title("CHARA MATCH | Top synthetic pairs by expansion")
    fig.tight_layout()
    fig.savefig(out / "top_pairs_expansion.png", dpi=150)
    plt.close(fig)
    print(f"Completed: {len(df)} artificial rows; {len(result['pair_scores'])} pairs")
    print(f"All product models converged: {result['model_summary'].converged.all()}")

if __name__ == "__main__":
    main()
