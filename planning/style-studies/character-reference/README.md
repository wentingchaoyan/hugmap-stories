# HugMap キャラクター設定集

[設定集を開く](index.html)

採用中の画像のみをassetsに保存。画像ファイル名に版番号は付けず、更新時は同じ名前で差し替える。過去の試作・比較ファイルは作業フォルダに残さず、履歴はGitで管理する。

- 三面図・寸法原図、Mimo／Luke／Genのポーズと表情、小物、4背景、子ども・大人の標準モデルを収録。
- LUMIの追加ポーズ・表情は保留。
- JSONは現在の設定。線仕様はanimal-line-styleとhuman-silhouette-styleを参照。
- 小物一覧の首飾り4点はブランド色に補正済み。その他の掲載PNGの線幅・色・造形の厳密な数値適合は未検証。

利用シーンの使い分け：[制作ガイド](usage-guidelines.html)。背景の道具一覧：background-props.json。

参照の優先順位：造形・衣装の形は三面図、寸法は寸法図、線はanimal-line-style.json／human-silhouette-style.json、識別小物と胸マークの色はbrand-colors.json、身体の白／カラーと背景量はusage-guidelines.htmlを基準にする。原図の黒い線・胸記号や旧資料の色指定より現在の線・配色仕様を優先する。

動物の輪郭・表情線は #A77C65、目・鼻・眼鏡は #6B5143（Mimo・Luke・Gen）。既存PNGの再着色は未実施。過去の生成プロンプトは制作履歴であり、新規制作の色指定は現行JSONを優先する。

成長記録の役割別要件：[growth-scene-design-rules.json](growth-scene-design-rules.json)。今回の整合性確認：[guideline-consistency-review.md](guideline-consistency-review.md)。
