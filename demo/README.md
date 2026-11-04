# 操作デモ

`index.html` をブラウザで開いて使用できます。商品・キャラクターの変更、ランキング並び替え、候補クリック、CSV保存に対応します。
外部通信やデータ送信はありません。モデルの再学習ではなく、完全人工データの計算済み結果の表示です。

結果を更新したら `python scripts/build_browser_data.py` で表示用データも更新してください。

## GitHub Pagesで公開

1. この `demo` フォルダをリポジトリのルートに追加します。
2. `.github/workflows/pages.yml` を同じ階層構造で追加します。
3. GitHubのSettings → PagesでSourceをGitHub Actionsに設定します。
4. Actions → Publish browser demo → Run workflowを実行します。
5. 完了後、Settings → Pagesに表示されるURLを開きます。

既存の分析テスト用 `ci.yml` は残してください。公開操作はまだ実施していません。
