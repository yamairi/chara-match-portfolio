from pathlib import Path
import argparse
import sys
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from chara_match.synthetic import generate_synthetic_data, data_dictionary, DEFAULT_ROWS, DEFAULT_SEED

def main():
    parser = argparse.ArgumentParser(description="Generate fully artificial demo inputs")
    parser.add_argument("--rows", type=int, default=DEFAULT_ROWS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output-dir", type=Path, default=REPO / "sample_data")
    args = parser.parse_args()
    df = generate_synthetic_data(args.rows, args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output_dir / "synthetic_demo.csv", index=False, float_format="%.6f")
    data_dictionary().to_csv(args.output_dir / "data_dictionary.csv", index=False)
    print(f"Generated {len(df)} artificial rows")

if __name__ == "__main__":
    main()
