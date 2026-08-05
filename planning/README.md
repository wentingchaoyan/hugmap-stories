# HugMap Stories planning インデックス

このディレクトリは、HugMap Storiesの世界観、キャラクター、物語、画面設計、企画、制作運用を管理する。

同じ内容を複数のファイルへ書かず、変更する内容に応じて一つの「正本」を更新する。

## 0. planning全体の構造

```text
世界の土台
├─ world-and-character-guide.md　⭐️⭐️⭐️　達成したい世界および人物の特徴
└─ world-space-story-map.md

キャラクターを絵と行動へ翻訳
├─ character-expression-guide.md
├─ character-facial-expression-reference.md
├─ visual-style-decision.md / .html　⭐️⭐️⭐️　動物と人間の絵のスタイルの組み合わせ方
└─ visual-reference-shortlist.md

一冊の物語を設計
├─ story-narrative-guide.md
└─ story-design-principles.md

作品候補と制作を管理
├─ story-backlog.md　　✍️ 心が動くもので、scriptを自分で書いてみる
├─ series-values-story-shortlist.md
├─ preverbal-development-series.md
├─ line-sticker-concept.md
├─ three-day-character-pose-assignment.md
└─ open-decisions.md　　⭐️⭐️⭐️　未決の制作軸、名前、国際展開、ストーリーの入り方

外部情報と同期
└─ content-sync.md

画風・キャラクター制作資料
├─ style-studies/
│  ├─ README.md
│  ├─ output-process.html　⭐️⭐️⭐️　探索から現在地までを画像でたどる
│  ├─ references/
│  ├─ prompts/
│  └─ outputs/
│     ├─ characters/{usagi,kotori,risu}/
│     ├─ groups/
│     └─ children/
└─ line-sticker-prototypes/
```

ファイルの種類:

| 種類 | 意味 |
|---|---|
| **正本** | シリーズ共通の決定事項を書く。内容を変えると複数作品へ影響する |
| **企画・管理** | 作品候補、進行、未決事項を管理する。決定後は正本へ反映する |
| **補助資料** | 正本を描画や制作へ翻訳する。正本そのものは上書きしない |
| **試作** | 比較・検討用。正式デザインとして直接流用しない |

## 1. 最初に読む順番

新しい絵本を企画するときは、次の順で確認する。

1. [`world-and-character-guide.md`](world-and-character-guide.md)
   シリーズが何を信じ、各先生が何を見つけるか。
2. [`world-space-story-map.md`](world-space-story-map.md)
   先生たちが暮らす場所と、場所を移動する物語線。
3. [`character-expression-guide.md`](character-expression-guide.md)
   先生が仕草、言葉、距離、道具でどう関わるか。
4. [`story-narrative-guide.md`](story-narrative-guide.md)
   誰の視点で語り、読者の理解をどう進めるか。
5. [`story-design-principles.md`](story-design-principles.md)
   一画面一見開き、余白、動き、UIをどう設計するか。
6. [`content-sync.md`](content-sync.md)
   `withu` の専門情報・素材をどう参照し、公開用へ同期するか。

## 2. 全ファイルの役割

### 2.1 シリーズ共通の正本

| ファイル | 役割 | 開く場面 | 書かないこと |
|---|---|---|---|
| [`world-and-character-guide.md`](world-and-character-guide.md) | 世界の価値観、シリーズの約束、メイン・サブの区別、各先生の信念・関心・強みの裏返し・チーム関係を決める | キャラクターの核を追加・変更するとき | 詳細な画面構成、顔パーツ、制作日程 |
| [`world-space-story-map.md`](world-space-story-map.md) | HugMapの家、遊びの場所、担当動物、場所を移動する物語線を決める | 新しい部屋、遊び、移動ルートを考えるとき | キャラクターの口調全文、物語の台詞 |
| [`character-expression-guide.md`](character-expression-guide.md) | 仕草、動き、距離、発言意図、象徴道具、代表ポーズを決める | 一場面で先生が何をするか描くとき | 世界観の再説明、部屋の詳細設計 |
| [`story-narrative-guide.md`](story-narrative-guide.md) | 子どもの視点、三幕、EAT＋E、問いと余白、本文とあとがきの役割を決める | 台本の流れと言葉を組み立てるとき | キャラクター造形、CSS・UI仕様 |
| [`story-design-principles.md`](story-design-principles.md) | 一画面一意味、余白、情報階層、色、動き、アクセシビリティを決める | HTML絵本の画面を設計・レビューするとき | 世界観、キャラクターの新設定、作品テーマ |
| [`content-sync.md`](content-sync.md) | `withu`の専門情報・公式素材・出典の参照元と同期手順を決める | 専門知識を台本やあとがきへ反映するとき | 作品の物語判断、キャラクターの新設定 |

### 2.2 キャラクターと画風の補助資料

| ファイル | 役割 | 開く場面 | 扱い |
|---|---|---|
| [`character-facial-expression-reference.md`](style-studies/references/character-facial-expression-reference.md) | 顔、視線、眉、口、耳、羽、尻尾などの描画基準 | 表情差分やイラスト発注資料を作るとき | `character-expression-guide.md`を絵へ翻訳する。性格の正本ではない |
| [`visual-reference-shortlist.md`](style-studies/references/visual-reference-shortlist.md) | ポーズ、距離、余白を研究する外部絵本・作家の観察点 | 参考作品を探すとき | 模倣用・画風の正本として使わない |
| [`character-design-prompt-workflow.md`](style-studies/prompts/character-design-prompt-workflow.md) | 6工程でキャラクター制作を安定させるPrompt A | 形が決まった後に色・三面図・応用へ進むとき | 正本の設定を変更しない |
| [`character-design-exploration-prompt-workflow.md`](style-studies/prompts/character-design-exploration-prompt-workflow.md) | 性格を誇張してから削るPrompt B | 性格がまだ形に出ていないとき | Prompt Aを置き換えない |
| [`visual-style-decision.md`](visual-style-decision.md) | 人物4案×動物3案から候補を絞り、判断理由と評価軸を残す | 画風を比較・決定するとき | 決定後も判断履歴として残す |
| [`visual-style-decision.html`](visual-style-decision.html) | 上記の画像を一画面で比較し、候補A/Bとメモをブラウザ上で確認する | 複数画像を見ながら話し合うとき | メモはブラウザ内保存。決定事項はMarkdownまたは正本へ移す |
| [`style-studies/README.md`](style-studies/README.md) | 画風・キャラクター試作の保存先、番号、更新ルールを示す | 画像を追加・整理するとき | 制作判断そのものは`output-process.html`で確認する |
| [`style-studies/output-process.html`](style-studies/output-process.html) | 3匹合同・各キャラクター・人物の探索順、採否、推奨案、現在地を画像で一覧化する | 試作の前後関係や採用理由を確認するとき | 現在地はSTEP 09。正式仕様は正本へ文章で反映する |

### 2.3 作品企画・進行管理

| ファイル | 役割 | 開く場面 | 完了後 |
|---|---|---|---|
| [`story-backlog.md`](story-backlog.md) | 完成作、試作、キャラクター別の物語の種、横断テーマ、優先順位を管理する | 次に作る一冊や担当動物を選ぶとき | 作品化したら状態と作品パスを更新する |
| [`series-values-story-shortlist.md`](series-values-story-shortlist.md) | バックログからシリーズ共通の価値観を表現しやすい代表作候補を選ぶ | シリーズの入口や代表サンプルを決めるとき | 採用後は作品別台本へ移し、候補の状態は`story-backlog.md`で更新する |
| [`preverbal-development-series.md`](preverbal-development-series.md) | 「ことば以前の発達」に限定したシリーズ企画、発達テーマ、作品候補を管理する | 発語以外の理解・伝達を扱う作品を企画するとき | 採用した物語は`story-backlog.md`と作品別台本へつなぐ |
| [`line-sticker-concept.md`](line-sticker-concept.md) | メイン3人のLINEスタンプ企画、文言、仕草、試作範囲を管理する | スタンプ制作・外注・商品展開を考えるとき | 正式素材の保存先と状態を追記する |
| [`three-day-character-pose-assignment.md`](three-day-character-pose-assignment.md) | 基本立ち、専門性ポーズ、チーム場面を作る3日間の作業計画 | キャラクター素材制作を短期アサインするとき | 完了後は制作履歴として残す |
| [`open-decisions.md`](open-decisions.md) | 会議メモ、比較中の案、メンタリングで聞くこと、判断待ちを一元管理する | まだ決めていない事項を追加・確認するとき | 決定したら該当する正本へ移し、ここには決定日と反映先だけ残す |

各作品固有の決定は、`stories/<story-slug>/script.md` に置く。企画ファイルや個別台本から、シリーズ共通設定を無断で変更しない。

### 2.4 試作画像とフォルダ

| パス | 内容 | 正式利用 |
|---|---|---|
| [`style-studies/`](style-studies/) | 参照資料、制作Prompt、生成物を役割別に管理する | **不可**。正式決定前の試作 |
| [`style-studies/outputs/`](style-studies/outputs/) | キャラクター別、3匹合同、人物別に分類した生成画像群 | **不可**。正式決定前の試作 |
| [`01-main-three-symbolic-pose-sheet-v1.png`](style-studies/outputs/groups/01-main-three-symbolic-pose-sheet-v1.png) | ことり・りす・うさぎの記号型3ポーズ | 画風候補Aの比較用 |
| [`02-main-three-animated-pose-sheet-v1.png`](style-studies/outputs/groups/02-main-three-animated-pose-sheet-v1.png) | メイン3人のキャラクター・アニメーション型3ポーズ | 画風候補Bの比較用 |
| [`03-main-three-collage-pose-sheet-v1.png`](style-studies/outputs/groups/03-main-three-collage-pose-sheet-v1.png) | メイン3人のコラージュ・素材型3ポーズ | 紙素材と絵本の温度の比較用 |
| [`04-main-three-playful-graphic-symbol-pose-sheet-v1.png`](style-studies/outputs/groups/04-main-three-playful-graphic-symbol-pose-sheet-v1.png) | 記号性を保ちながら動きと手描き感を加えた比較 | 別系統の画風探索 |
| [`05-main-three-character-design-step-1-unified-v2.png`](style-studies/outputs/groups/05-main-three-character-design-step-1-unified-v2.png) | 3匹の共通骨格候補と推奨案 | 頭身・胴体幅・手足の比率の基準 |
| [`06-main-three-emotional-roughs-dialogue-overview-v1.png`](style-studies/outputs/groups/06-main-three-emotional-roughs-dialogue-overview-v1.png) | 3匹それぞれの役割を表す感情・ポーズ候補 | 代表ポーズの推奨選定 |
| [`07-main-three-consultation-group-pose-options-v2.png`](style-studies/outputs/groups/07-main-three-consultation-group-pose-options-v2.png) | 相談画面で並べる際のポーズと、りすの再調整案 | 3匹の見分けやすさの確認 |
| [`08-main-three-prompt-b-step-2-personality-exaggeration-v1.png`](style-studies/outputs/groups/08-main-three-prompt-b-step-2-personality-exaggeration-v1.png) | 顔・身体・重心による性格の誇張比較 | 正式案ではなく検討資料 |
| [`09-main-three-selected-emotional-poses-color-study-v2.png`](style-studies/outputs/groups/09-main-three-selected-emotional-poses-color-study-v2.png) | 推奨骨格へ代表ポーズと配色を統合し、りすの白い口元を比較 | 現在地。完成デザインではない |
| [`01-child-symbolic-study-v1.png`](style-studies/outputs/children/01-child-symbolic-study-v1.png) | 人物の記号・アイコン型 | 人物4案の比較用 |
| [`02-child-animated-study-v1.png`](style-studies/outputs/children/02-child-animated-study-v1.png) | 人物のキャラクター・アニメーション型 | 人物4案の比較用 |
| [`03-child-watercolor-life-study-v1.png`](style-studies/outputs/children/03-child-watercolor-life-study-v1.png) | 人物の水彩・生活描写型 | 人物4案の比較用 |
| [`04-child-line-sketch-study-v1.png`](style-studies/outputs/children/04-child-line-sketch-study-v1.png) | 人物の線画・スケッチ型 | 現在の人物第一候補 |
| [`05-boy-kotori-unified-style-v1.png`](style-studies/outputs/children/05-boy-kotori-unified-style-v1.png) | 子どもとことり先生を同一画風へ寄せた初期試作 | 過去比較 |
| [`06-boy-matched-to-animal-style-v2.png`](style-studies/outputs/children/06-boy-matched-to-animal-style-v2.png) | 子どもを既存動物の画風へ寄せた初期試作 | 過去比較 |
| [`line-sticker-prototypes/`](line-sticker-prototypes/) | LINEスタンプのシート試作 | 正式スタンプではない |
| [`main-three-nine-sticker-sheet-v1.png`](line-sticker-prototypes/main-three-nine-sticker-sheet-v1.png) | メイン3人×3種の9スタンプ試作 | 文言・ポーズ・縮小時の確認用 |

試作画像から採用する要素は、必ず文章化して該当する正本へ移す。画像だけを暗黙の仕様にしない。

## 3. 目的から探す

| 今したいこと | 最初に開く | 次に開く |
|---|---|---|
| 世界観を説明したい | `world-and-character-guide.md` | `world-space-story-map.md` |
| 一人の先生を深めたい | `world-and-character-guide.md` | `character-expression-guide.md` |
| 表情やポーズを描きたい | `character-expression-guide.md` | `character-facial-expression-reference.md` |
| 画風を決めたい | `visual-style-decision.html` | `visual-style-decision.md`、`open-decisions.md` |
| キャラクター造形の現在地を見たい | `style-studies/output-process.html` | `style-studies/README.md`、`character-expression-guide.md` |
| 新しい絵本を企画したい | `story-backlog.md` | `story-narrative-guide.md` |
| シリーズの代表作を選びたい | `series-values-story-shortlist.md` | `world-and-character-guide.md` |
| 一冊の台本を書きたい | `story-narrative-guide.md` | `stories/<story-slug>/script.md` |
| HTML絵本を作りたい | `story-design-principles.md` | 既存作品の`index.html` |
| 専門情報を確認したい | `content-sync.md` | `withu`側の正本 |
| 未決事項を相談したい | `open-decisions.md` | 関係する正本 |
| LINEスタンプを作りたい | `line-sticker-concept.md` | `character-expression-guide.md` |

## 4. 判断が衝突したとき

次の優先順位で判断する。

```text
実際の親子・支援者の声と安全性
↓
world-and-character-guide.md の価値観
↓
world-space-story-map.md と character-expression-guide.md
↓
story-narrative-guide.md
↓
story-design-principles.md
↓
作品別の企画・台本
↓
参考画像・一時的な制作メモ
```

参考画像や過去作品が正本と異なる場合、参考画像や過去作品をそのまま正解にしない。

## 5. 情報を追加する場所

| 追加したい情報 | 更新先 |
|---|---|
| シリーズの信念、先生の役割、チーム関係 | `world-and-character-guide.md` |
| 部屋、遊び、行き先、移動ルート | `world-space-story-map.md` |
| 仕草、発言、距離、持ち物 | `character-expression-guide.md` |
| 目、眉、口などの描画方法 | `character-facial-expression-reference.md` |
| 視点、EAT、三幕、読後変化 | `story-narrative-guide.md` |
| レイアウト、色の役割、アニメーション | `story-design-principles.md` |
| 実話や一冊だけの展開 | 作品別 `script.md` |
| 次に作る作品と優先順位 | `story-backlog.md` |
| 会議で出た未決定の提案 | `open-decisions.md` |
| キャラクターの国際名、命名規則、即時認識の未決事項 | `open-decisions.md` |
| withuとの同期、出典、専門情報 | `content-sync.md` |
| 画風の比較結果・採点 | `visual-style-decision.md` |
| 画風の未決事項 | `open-decisions.md` |
| LINEスタンプの文言・商品企画 | `line-sticker-concept.md` |

## 6. 重複を防ぐルール

- 別ファイルの内容が必要な場合、要約を再掲せずリンクする。
- 一覧表は、一覧を管理する正本に一つだけ置く。
- 「今後決めること」は、決まった時点で正本へ移し、未決事項から削除する。
- 会議メモや担当者コメントを見出しへ残さない。必要なら本文へ判断理由として書く。
- 参考作品の名称は、模倣指示ではなく「何を観察するか」とセットで記録する。
- 試作画像は正式デザインと明確に区別する。

## 7. 新しい作品を始めるチェック

1. 実際の生活場面と、保護者のリアルな疑問がある。
2. 最初から専門用語やEATを当てはめていない。
3. 中心となる「見つけ方」から担当動物を一人選んでいる。
4. 必要な場所と遊びを選び、移動を増やしすぎていない。
5. 視点、Awareness、読後変化を決めている。
6. 一画面一意味で台本を作っている。
7. 根拠情報と公開可能な表現を確認している。
8. 最後を先生の説明ではなく、親子の日常へ返している。
