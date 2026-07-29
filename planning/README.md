# HugMap Stories planning ガイド

このディレクトリは、HugMap Storiesの世界観、キャラクター、物語、画面設計、企画、制作運用を管理する。

同じ内容を複数のファイルへ書かず、変更する内容に応じて一つの「正本」を更新する。

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

## 2. ファイルの役割

### 正本

| ファイル | 決めること | 書かないこと |
|---|---|---|
| [`world-and-character-guide.md`](world-and-character-guide.md) | 世界の価値観、シリーズの約束、各先生の核・見つけ方・関係 | 詳細な画面構成、顔パーツ、制作日程 |
| [`world-space-story-map.md`](world-space-story-map.md) | HugMapの家、遊びの場所、担当動物、空間的な物語線 | キャラクターの口調全文、EATの詳細説明 |
| [`character-expression-guide.md`](character-expression-guide.md) | 仕草、動き、距離、発言意図、道具 | 世界観の再説明、部屋の詳細設計 |
| [`story-narrative-guide.md`](story-narrative-guide.md) | 視点、三幕、EAT＋E、本文とあとがきの分担 | キャラクター造形、CSS・UI仕様 |
| [`story-design-principles.md`](story-design-principles.md) | 画面、余白、情報階層、動き、アクセシビリティ | 世界観、キャラクター設定、作品テーマ |
| [`content-sync.md`](content-sync.md) | 外部情報・公式素材の参照元と同期手順 | 作品の物語判断、キャラクターの新設定 |

### ビジュアル補助資料

- [`line-sticker-concept.md`](line-sticker-concept.md): メイン3人のLINEスタンプ企画、文言、仕草、試作範囲。

| ファイル | 役割 | 扱い |
|---|---|---|
| [`character-facial-expression-reference.md`](character-facial-expression-reference.md) | 顔、視線、眉、口、動物固有パーツの描画基準 | `character-expression-guide.md`を絵へ翻訳する補助資料 |
| [`visual-reference-shortlist.md`](visual-reference-shortlist.md) | ポーズ、距離、余白を研究する外部参考資料 | 模倣用・設定の正本として使わない |
| [`visual-style-decision.md`](visual-style-decision.md)・[`HTML比較ボード`](visual-style-decision.html) | 人物4案と動物3案を比較し、最終候補を絞る意思決定シート | 決定後は判断理由の履歴として残す |
| [`three-day-character-pose-assignment.md`](three-day-character-pose-assignment.md) | キャラクター素材を作るための短期作業計画 | 完了後は履歴。世界設定を上書きしない |
| `style-studies/` | 画風比較用の試作画像 | 正式デザインではない |

### 作品企画・進行管理

| ファイル | 役割 |
|---|---|
| [`preverbal-development-series.md`](preverbal-development-series.md) | 「ことば以前の発達」シリーズの企画と作品候補 |
| [`story-backlog.md`](story-backlog.md) | 作品候補、優先順位、制作状態 |
| [`open-decisions.md`](open-decisions.md) | 会議メモ、未採用の提案、判断待ち。決定済み設定の正本ではない |

各作品固有の決定は、`stories/<story-slug>/script.md` に置く。企画ファイルや個別台本から、シリーズ共通設定を無断で変更しない。

## 3. 判断が衝突したとき

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

## 4. 情報を追加する場所

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
| withuとの同期、出典、専門情報 | `content-sync.md` |

## 5. 重複を防ぐルール

- 別ファイルの内容が必要な場合、要約を再掲せずリンクする。
- 一覧表は、一覧を管理する正本に一つだけ置く。
- 「今後決めること」は、決まった時点で正本へ移し、未決事項から削除する。
- 会議メモや担当者コメントを見出しへ残さない。必要なら本文へ判断理由として書く。
- 参考作品の名称は、模倣指示ではなく「何を観察するか」とセットで記録する。
- 試作画像は正式デザインと明確に区別する。

## 6. 新しい作品を始めるチェック

1. 実際の生活場面と、保護者のリアルな疑問がある。
2. 最初から専門用語やEATを当てはめていない。
3. 中心となる「見つけ方」から担当動物を一人選んでいる。
4. 必要な場所と遊びを選び、移動を増やしすぎていない。
5. 視点、Awareness、読後変化を決めている。
6. 一画面一意味で台本を作っている。
7. 根拠情報と公開可能な表現を確認している。
8. 最後を先生の説明ではなく、親子の日常へ返している。
