# Fully synthetic demo data

このフォルダのデータは独立した架空設定と乱数seedから生成したものです。
元データの行・分布・設問体系は使用していません。辞書の全変数は架空です。

再生成：`python scripts/generate_synthetic_data.py`

デフォルト設定は `src/chara_match/synthetic.py` と `config.py` にあります。
生成行数を小さくすると、分析に必要なクラス数を満たせない場合があります。
