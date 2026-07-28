# HugMap Stories

[English README](README.en.md)

HugMapの公式キャラクターと支援方針をもとにした、独立公開可能な静的デジタル絵本サイトです。

アプリ本体の `withu` リポジトリとは分離し、公開中の絵本がアプリ側の変更で突然変わらない構成にしています。キャラクター、デザイン、FAQ、Activityは制作時に参照・同期しますが、本番アプリのファイルやデータベースには直接依存しません。

## 構成

```text
hugmap-stories/
├── index.html                 # シリーズ入口
├── shared/
│   ├── base.css               # ブランドトークンと共通アクセシビリティ
│   ├── story-runtime.js       # ページ進捗・文字・動きの共通操作
│   ├── characters/            # 公開承認済みキャラクターの固定コピー
│   └── asset-manifest.json    # アプリ側の取得元とハッシュ
├── stories/
│   ├── mouikkai/
│   └── hero-team/
├── content/references/        # FAQ・Activityから選定した静的な制作資料
└── planning/                  # 世界観・物語・ビジュアル・制作運用の正本と企画
```

## ローカルで読む

`index.html` をブラウザーで開いてください。ビルド工程はありません。

英語版は `en/index.html` から読めます。日本語原稿を更新した場合は、手訳を管理する `scripts/build_english.py` を更新してから `python3 scripts/build_english.py` を実行してください。

## 新しい作品を追加する

1. `stories/<story-slug>/` を作る。
2. `../../shared/base.css` と `../../shared/story-runtime.js` を読み込む。
3. `<body data-story-pages="ページ数">` を設定する。
4. 各パネルに連番の `data-step` を付ける。
5. `planning/README.md` の順番で、世界観、キャラクター、物語、画面設計を確認する。
6. `planning/content-sync.md` に従い、専門情報と素材の出典を確認する。
7. `planning/story-design-principles.md` を参照し、作品タイプと動きの強さを決める。
8. 各作品の `script.md` にページの役割・絵・動き・補足情報を記録する。
9. `planning/story-backlog.md` の状態を更新する。

## ブランチと公開

- 共通基盤: `codex/storybook-foundation-*`
- 新作: `codex/story-<slug>`
- 改訂: `codex/story-<slug>-revision-*`
- 完成後は `main` へ統合し、制作ブランチは閉じる。
- 公開版には `storybook-<slug>-v1.0.0` 形式のタグを付ける。

静的ホスティングではリポジトリルートを公開ディレクトリに指定できます。
