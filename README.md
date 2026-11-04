# CHARA MATCH — Portfolio Edition

**商品とキャラクターの組み合わせを、顧客構成の相性と新規層への拡張余地から比較する分析システム。**

> 元データ非公開・ポートフォリオ用の一般化再実装です。データと掲載結果はすべて完全人工生成（synthetic）で、元の個票・集計結果・調査固有の設問やコード体系は含みません。

## できること

- **顧客層の可視化**：価値観の特徴を要約し、顧客をクラスタに分類
- **コラボ候補の比較**：商品購入者とキャラクター支持者の構成から、相性と拡張余地を評価
- **選定理由の確認**：候補分類・推奨理由・顧客構成の違いを表示
- **ブラウザでの操作**：商品・キャラクターの選択、ランキングの並び替え、CSV保存

## ブラウザデモ

`demo/index.html` をブラウザで開くと、インストールなしで操作できます。

デモは人工データの計算済み結果を表示するものです。ブラウザ上でモデルの再学習は行いません。

## 分析の流れ

```text
人工データ
  ↓
重み付き標準化 → PCA・Varimax回転 → 顧客クラスタリング
  ↓
商品モデルの比較・クラスタ別の拡張余地を算出
  ↓
購入者・支持者の構成比を比較
  ↓
ペア評価・候補分類・推奨理由
```

主な手法は、重み付きK-means++、L2ロジスティック回帰、交差検証によるモデル比較です。支持者が少ない場合は構成比を市場平均へ縮約し、少数サンプルの影響を抑えます。

## 評価指標

| 指標 | 意味 |
| --- | --- |
| Compatibility | 商品購入者とキャラクター支持者の顧客構成の相性 |
| Expansion | 新しい顧客層への広がりを比較する指標 |
| Unexpected Affinity | 背景カテゴリから期待される支持率に対する上振れ・下振れ |
| Customer Shift | 購入者と支持者のクラスタ構成比の差 |

これらは候補探索のための指標であり、売上増加や施策の因果効果を予測するものではありません。候補分類は比較対象内の相対評価です。

## サンプル結果

![人工データによる拡張スコアの比較](outputs_sample/top_pairs_expansion.png)

- [ペアの評価・推奨理由](outputs_sample/pair_scores.csv)
- [商品モデルの比較](outputs_sample/model_summary.csv)
- [顧客構成の違い](outputs_sample/customer_shift_long.csv)

## 分析コードの実行

Python 3.11以上を使用します。リポジトリのルートで実行してください。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python -m pytest -q
python scripts/run_demo.py
```

Windowsでは、有効化のコマンドを `.venv\Scripts\activate` に置き換えてください。

デフォルトでは架空の6商品×8キャラクターを評価し、`outputs_demo/` に結果を保存します。

```bash
# 人工データを再生成
python scripts/generate_synthetic_data.py

# 対象を絞って実行
python scripts/run_demo.py --n-products 2 --n-characters 3
```

## リポジトリ構成

```text
demo/                ブラウザで操作できるデモ
src/chara_match/      分析ロジック・人工データ生成
scripts/             実行用スクリプト
sample_data/         人工データ・データ辞書
outputs_sample/      人工データによるサンプル結果
tests/               自動テスト
docs/                方法論・検証記録
.github/workflows/   自動テスト・デモ公開
```

## 詳細資料

[方法論](docs/methodology.md) · [データ辞書](sample_data/data_dictionary.csv) · [データ方針](docs/data_policy.md) · [再実装について](RECONSTRUCTION_NOTES.md) · [検証結果](docs/verification.md)

## ライセンス

再配布ライセンスは設定していません。の再配布ライセンスは設定していません。
