# 成長場面のprompt管理

共通仕様は `planning/style-studies/character-reference/` の既存JSONを正本とし、各場面には修正範囲と固有の指示だけを書きます。Genの37場面に加え、`character-reference/` にあったLukeの43場面・Mimoの40場面を統合しました。元のTXTは合計260個、場面は合計120件です。親子・子ども同士の場面も登場する動物へ分類しています。LUMI用の場面promptは見つからなかったため、空のファイルは作成していません。人物見本の `toddler-girl-patterns-prompt.txt` は動物の場面ではないため対象外です。

## ファイル

- `gen.json` / `luke.json` / `mimo.json`：動物共通の参照画像・指示と、場面IDをキーにした `scenes`。Luke・Mimoの繰り返し文章は `defaults.blocks` に一度だけ定義し、各場面の `blocks` から参照します。
- `shared.json`：外部仕様の参照先、共通の文章、修正範囲ごとの共通ブロック。色・線幅はここにも転記せず、`{{human#/colors/childOutline}}` のようにJSON Pointerで参照。
- `history/gen.json` / `history/luke.json` / `history/mimo.json`：それぞれ旧TXT62個・97個・101個のファイル名・原文・SHA-256。過去の実行日時や成功、ファイル間の実行順は推定しない。元ファイル内の複数パスも原文のまま保存。
- `render.py`：標準ライブラリだけで検証・文章展開。画像生成は実行しない。

共通の線は `animal-line-style.json` / `human-silhouette-style.json`、識別小物の色・U位置は `brand-colors.json`、場面の優先順位は `growth-scene-design-rules.json` を参照します。既存ページ側のJSONや画像はこの移行で更新しません。既存仕様ファイル相互の重複整理は対象外です。

## 編集

該当する動物JSONの `scenes.<場面ID>.instructions` を編集します。共有する文章は `defaults.blocks` を編集します。線色や線幅の数値を場面に書かず、共通仕様を変更してください。

`mode` は修正範囲を指定します。

| mode | 適用範囲 |
| --- | --- |
| `child-color` | 子どもの線色のみ。線幅・造形・動物・大人・背景を維持 |
| `child-clothing-color` | 子どもの線色と重複した服の線の整理 |
| `human-and-mark` | 人物の形・表現と動物のU位置。動物全体の線や造形は維持 |
| `local-guideline` | 場面固有の局所修正に人物・動物の現行仕様を適用 |
| `source-scoped` | Luke・Mimoの局所編集の範囲を保ち、統一方針・共通文章・場面差分・採用状態を展開 |

これは既存画像の編集用定義です。色修正だけの場面について、新規生成に必要な構図や年齢をファイル名から補完していません。背景の現行ルール全体を無条件に適用すると局所修正の範囲を越えるため、背景の描き直しも行いません。

履歴の修正promptは現行promptに自動合成しません。採用記録で確認できる状態と、共通仕様に沿う条件を現行定義へ反映しています。`undefined` だった5個は `status: invalid` として原文を保存し、展開には使用しません。

現行promptは共通仕様を優先し、採用済み監査記録に基づく場面の状態へ統一しています。`sourcePrompt` は移行元の記録です。採用した髪型・小物・背景は `decisions`、根拠となる履歴は `decisionSources` に記録します。`decisions` は生成用の文章に展開され、古い原文は展開されません。

## 統一方針

`shared.json` の `policy` が全動物・全モードに適用されます。共通の色・線幅・U表示条件を場面の指示で上書きしません。適用範囲は各場面の編集モードに従い、色修正だけの実行で造形や背景を変更しません。

- **Uマーク**：正しい服の面が見えるときだけ表示し、部分的・完全な隠れを許容。見せるために翼・姿勢を変えたり、腕・スカーフ・腰に移したりしない。
- **髪型**：場面で採用した髪型を維持。指定がなければ現状を維持し、参考画像から乳児を幼児へ変えない。
- **人物の顔**：顔内部は白く省略。発声などに必要な口は外周シルエットで表し、内部の顔パーツを追加しない。
- **小物・背景**：物語に必要な小物と採用済みの控えめな装飾を維持。未指定の装飾を追加しない。
- **編集履歴**：試行・却下・無効なpromptを一括合成しない。

| 場面 | 採用する状態 |
| --- | --- |
| Mimo・カードの順番待ち | 小さなコップとストローを保持し、飲みながら左の子どもを見る。人物線の修正では鳥を変更しない |
| Luke・粘土遊び | 白いボブ髪、右上の小さな作品棚と粘土作品2点を保持 |
| Luke・お絵描き | 左上の淡い絵2枚と小さなレールを保持 |
| Luke・自分で食べる | 左上の小さな紙の葉2枚を保持 |
| Mimo・「みて」を受け取る | 三面図の左側面、片目・片眉、星を受け取る翼。胸のUは自然な隠れを許容 |

色だけ修正する実行に異なる状態の入力画像が渡された場合、場面の状態変更は別の編集として行います。この整理自体は画像を変更しません。

場面を特定できないMimoのU復元指示は `defaults.historyRecords` に置き、特定の場面へ推測で割り当てません。履歴は展開されません。

別の動物を追加する場合も、同じ構造で動物JSONと履歴を作成します。参照画像番号の対応は元のpromptに従い、必要な実画像を添付してください。`referenceImages` は候補の一覧であり、添付順序を決めるものではありません。

## 検証と展開

リポジトリのルートから実行します。

```sh
python3 planning/participatory-growth-frame-studies/prompts/render.py \
  planning/participatory-growth-frame-studies/prompts/gen.json --validate

python3 planning/participatory-growth-frame-studies/prompts/render.py \
  planning/participatory-growth-frame-studies/prompts/gen.json --scene ball-roll

python3 planning/participatory-growth-frame-studies/prompts/render.py \
  planning/participatory-growth-frame-studies/prompts/gen.json \
  --scene ball-roll --output /tmp/gen-ball-roll-prompt.txt
```

Luke・Mimoも同じコマンドで入力ファイルを `luke.json` / `mimo.json` に変更します。例：

```sh
python3 planning/participatory-growth-frame-studies/prompts/render.py \
  planning/participatory-growth-frame-studies/prompts/luke.json --scene clay-press

python3 planning/participatory-growth-frame-studies/prompts/render.py \
  planning/participatory-growth-frame-studies/prompts/mimo.json --scene bubble-play
```

`--validate` は全場面の展開、参照JSON・画像の存在、未解決トークン、履歴の欠落・原文ハッシュを検証します。生成画像の見た目や色の適合を検証するものではありません。

`--output` は展開済みTXTと `.snapshot.json` を保存します。スナップショットには展開文章、入力仕様の内容とSHA-256、対象画像・参照画像のパスを記録します。画像自体は複製しないため、画像生成を実行する際は実際に添付した画像も別途保存してください。指定する出力先ディレクトリは事前に作成してください。

生成時は対象場面の画像を編集元として渡し、造形を直す場面では必要な参照画像を添付します。色だけ直す場面に造形変更の指示を追加しないでください。JSON内の参照やパスだけで画像が生成ツールへ添付されるわけではありません。

旧TXTを参照していた `illustration-review.json` の履歴は、`prompts/history/<動物>.json#/records/<旧ファイル名>` へ更新済みです。フラグメントはJSON Pointerとして解釈します。
