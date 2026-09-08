# HugMap キャラクターUI 配置・移行監査

最終更新: 2026-09-07

関連文書: [`CHARACTER_DISPLAY_GUIDELINES.md`](CHARACTER_DISPLAY_GUIDELINES.md)

## 1. リポジトリの責務

| リポジトリ | 責務 | 置くもの | 置かないもの |
|---|---|---|---|
| `hugmap-stories` | キャラクターの検討・正本設計 | ガイドライン、造形研究、三面図、演技シート、サイズ比較、配色比較、採用前候補 | アプリの実装コンポーネント、公開サイトの本番HTML |
| `withu` | React Nativeアプリの本番実装 | Face／Avatar／Fullアセット、サイズトークン、Chat・Discover・発達・プロフィールUI | 検討途中の比較表、未採用ポーズ、Web専用ヒーロー |
| `withuai` | 公開Web・FAQの本番実装 | Web用Face／Avatar／Full、FAQテンプレート、CTA、公開プロフィール・ヒーロー | アプリ専用ナビゲーション、React Nativeコンポーネント、造形検討全履歴 |

## 2. 今回の `withu` 監査結果

### 最適化済み

| UI | 変更前 | 変更後 |
|---|---|---|
| Discover先生タブ | 56–58px枠へ全身を縮小 | 主要4人はFaceを88%で表示、未制作キャラはFullへフォールバック |
| 発達ステージカード見出し | 28pxへ全身を縮小 | Faceを使用 |
| Discover本文のbuddy表示 | 38pxへ全身を縮小 | Faceを使用 |
| 発達詳細FAQ・担当表示 | 46px／小型回答バッジへ全身を縮小 | Faceを使用 |
| Chat先生選択カード | Fullを52px表示 | Fullを80px表示 |
| サイズ指定 | 各画面に数値を直書き | `PERSONA_DISPLAY_SIZES`を追加 |

### 既に適切だった箇所

- Chat回答カードは`faceAvatar ?? avatar`を使用していた。
- Chatのキープ一覧・紹介チップもFaceを優先していた。
- キャラクター情報画面はScene用ヒーローを使用し、UI用Fullと分離していた。
- キャラクターが未制作の場合にFullへフォールバックする仕組みがある。

### 次回のアセット制作後に最適化する箇所

1. `pediatrician`、`sped`、`feeding_oral`、`peer_parent`にもFaceを追加する。
2. 主要4人にAvatar専用の上半身アセットを追加し、DiscoverタブをFaceからAvatarへ更新する。
3. 先生カード用Fullの透明余白と頭部光学サイズを統一する。
4. Sceneヒーローの頭部比率・服・固有記号をUI正本へ合わせる。
5. `persona_pocket.png`にもFace／Avatar／Fullの段階を設ける。

## 3. `withu` へ移動・実装すべきUI

次はアプリ固有のため、設計承認後に`withu`へ移す。

| 優先度 | UI／アセット | 移動先候補 | 理由 |
|---:|---|---|---|
| P0 | 主要4人のFace正本 | `src/images/persona/faces/` | Chat、FAQ、Discoverの小型表示で共用する |
| P0 | 全先生のFace正本 | `src/images/persona/faces/` | Fullへのフォールバックを解消する |
| P0 | キャラクターサイズトークン | `src/constants/ChatPersona.ts`または専用表示コンポーネント | 画面ごとの数値差を防ぐ |
| P1 | 主要4人のAvatar正本 | `src/images/persona/avatars/` | Discover先生タブ用 |
| P1 | 光学サイズを揃えたFull正本 | `src/images/persona/full/` | 先生選択カード、空状態用 |
| P1 | 共通`PersonaImage`コンポーネント | `src/components/persona/PersonaImage.tsx` | variant、サイズ、背景、フォールバックを一元管理する |
| P1 | LumiのPurple Grey版 | 上記Face／Avatar／Full | Genとの分離と穏やかな役割表現 |
| P2 | Discover用Scene画像 | `src/images/discover/`または配信アセット | 子どもとの共同注意など、本文の場面表現に使う |
| P2 | CharacterProfileヒーロー | `src/images/persona/heroes/` | 大型の世界観表現として使用する |

`hugmap-stories`の比較表そのものをアプリへコピーしない。採用されたキャラクターを1体ずつ切り出し、用途別正本として書き出してから移す。

## 4. `withuai` へ移動・実装すべきUI

次は公開Web固有のため、設計承認後に`withuai`へ移す。

| 優先度 | UI／アセット | 移動先候補 | 理由 |
|---:|---|---|---|
| P0 | Web用Face 8人分 | `assets/images/persona/faces/` | FAQ一覧の27px回答者表示をFull縮小から置換する |
| P0 | Face／Avatar／Fullを選ぶテンプレート関数 | `scripts/faq_ja_template.html`ほか | `AV()`一種類で全用途を賄う状態を解消する |
| P0 | FAQ回答者Face | `.qa .av` | 34px枠内で顔を明確にする |
| P1 | 先生タイル用Avatar | FAQテンプレートの`.tile` | 56pxで上半身と固有記号を見せる |
| P1 | CTA用FaceまたはAvatar | FAQテンプレートの`.cta` | 30pxへFullを縮小しない |
| P1 | 光学サイズを揃えた集合Full | FAQヒーローの`.lineup` | キャラごとの個別height直書きを廃止する |
| P2 | 公開キャラクタープロフィールScene | `assets/images/persona/heroes/` | 世界観紹介・プロフィールページ用 |
| P2 | SNS／OG用Sceneテンプレート | `assets/images/og/` | UIアセットと投稿イラストを分離する |

公開FAQでは現在、`AV()`が一覧、回答、CTAなどへ同じFull画像を返している。次のように用途別関数へ分ける。

```js
const FACE_AV = persona => `assets/images/persona/faces/${fileFor(persona)}.png`;
const AVATAR_AV = persona => `assets/images/persona/avatars/${fileFor(persona)}.png`;
const FULL_AV = persona => `assets/images/persona/full/${fileFor(persona)}.png`;
```

Faceが未制作のキャラクターだけFullへフォールバックし、制作完了後にフォールバックを削除する。

## 5. `hugmap-stories` に残すUI・資料

次は本番UIではなく意思決定資料なので、`planning`配下に残す。

- 頭部形状比較
- 体型・年齢・性表現比較
- 三面図とpx計測ガイド
- 8ポーズ演技シート
- 線の揺れ・紙質・無彩色比較
- 28／40／56／80／128px実寸比較
- カラーパレット比較
- Before／Afterと不採用案
- キャラクター表示ガイドライン
- リポジトリ間の移行監査

## 6. 移行ゲート

アセットを`withu`または`withuai`へ移す前に、次を満たす。

- [ ] Face／Avatar／Fullの固定造形が一致している
- [ ] 28、56、80pxの実寸で確認済み
- [ ] WhiteとOff White背景で境界が見える
- [ ] 頭部の光学サイズが全員で揃っている
- [ ] キャラクター固有色とアクセント面積が承認済み
- [ ] 日本語・英語の名前を画像へ焼き込んでいない
- [ ] 透過PNGまたは編集可能な正本がある
- [ ] アプリとWebで同じpersona ID・ファイル名を使える
- [ ] 検討用比較画像ではなく、1体ずつ切り出した本番アセットである
