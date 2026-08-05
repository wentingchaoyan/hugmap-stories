# Style Studies

キャラクターと画風の検討資料を、役割ごとに分けて保存する。

制作順と各試作の判断は [`output-process.html`](output-process.html) で一覧できる。画像ファイル先頭の番号は、各フォルダー内での検討順を表す。

```text
style-studies/
├─ references/  外部作品の観察点と、表情設計の参照資料
├─ prompts/     画像生成・キャラクター探索の制作手順
└─ outputs/
   ├─ characters/
   │  ├─ usagi/   うさぎ単体のラフ、表情、ポーズ
   │  ├─ kotori/  ことり単体のラフ、表情、ポーズ
   │  └─ risu/    リス単体のラフ、表情、ポーズ
   ├─ groups/     メイン3匹を並べた比較・相談画面用試作
   └─ children/   子ども・人物・動物との統一画風試作
```

## 保存ルール

- 新しく生成した画像は、対象に応じて `outputs/characters/<name>/`、`outputs/groups/`、`outputs/children/` のいずれかへ置く。
- 再利用するプロンプトや制作フローは `prompts/` に置く。
- 外部作品のURL、観察メモ、描画基準は `references/` に置く。
- 外部作品の画像を許可なく複製して保存しない。参照元URLと、抽出した一般的な設計原則を記録する。
- 採用した判断は画像だけに残さず、該当する正本へ文章で反映する。
