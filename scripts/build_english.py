"""Build the hand-translated English static pages from their Japanese originals."""

from html.parser import HTMLParser
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]

TOP = {
    "English": "日本語",
    "子どものことば、からだ、おてて、行動の手がかりを、HugMapの先生たちと見つけるデジタル絵本。": "Digital picture books for discovering clues in children's communication, bodies, hands, and behavior with the HugMap teachers.",
    "きもちを、": "Picture books",
    "ひらく": "that open",
    "絵本。": "up feelings.",
    "ことばになる前のサインも、": "Signs that come before words.",
    "見えにくい身体のがんばりも。": "The body's efforts that are easy to miss.",
    "動物の先生たちと、いっしょに見つけます。": "Discover them together with our animal teachers.",
    "きょうは、どんなことが気になる？": "What are you wondering about today?",
    "ぼくたちが、": "We'll help you",
    "本を あんないするよ。": "find your story.",
    "いまの気持ちに合う入口から。": "Start wherever feels right today.",
    "絵本で、気づく": "Notice through stories",
    "子どもの視点から、気持ちや行動を見てみる。": "See feelings and behavior from a child's point of view.",
    "FAQで、知る": "Learn through FAQs",
    "299件のQ&Aから、理由と関わり方を探す。": "Explore 299 answers about possible reasons and ways to help.",
    "先生に、相談する": "Talk with a teacher",
    "この子の場合を、HugMapの先生と一緒に考える。": "Think about your child's situation with a HugMap teacher.",
    "ことりせんせい": "Kotori Sensei",
    "ことばになる前から、": "The story begins",
    "おはなしは はじまっているよ。": "even before words.",
    "TEACHER SHELF・ことばとコミュニケーション": "TEACHER SHELF · LANGUAGE & COMMUNICATION",
    "ことり先生から、": "Start with",
    "見てみる。": "Kotori Sensei.",
    "絵本で子どもの気持ちに近づいたあと、FAQで理由や具体的な関わり方を確かめられます。": "After stepping into a child's point of view through a story, use the FAQs to explore possible reasons and practical ways to respond.",
    "絵本『ぼくの「もういっかい」きこえた？』": "Story: Did You Hear My “Again”?",
    "読む →": "Read →",
    "関連するFAQ": "RELATED FAQS",
    "ことばが出る前の子。要求があると大声で叫びます": "My child does not use words yet and screams when they want something",
    "発語を促す、楽しい遊びはありますか？": "Are there fun activities that encourage speech?",
    "喃語が少ない場合、どう見たらいい？": "What should I look for when my child rarely babbles?",
    "声に反応しない場合、まず何を確かめる？": "What should I check first if my child does not respond to voices?",
    "ことり先生の42問を見る": "See Kotori Sensei's 42 questions",
    "この子の場合を相談する": "Ask about my child",
    "先生と、本をえらぶ。": "Choose a story with a teacher.",
    "気になることから選んでも、好きな先生から選んでも大丈夫です。": "Choose by what is on your mind, or simply by the teacher you like.",
    "ことばになる前のサイン": "SIGNS BEFORE WORDS",
    "ことりせんせい、": "Kotori Sensei,",
    "ぼくの「もういっかい」": "did you hear my",
    "きこえた？": "“again”?",
    "目、手、身体の動き。まだことばにならない「伝えたい」に出会うおはなし。": "Eyes, hands, and body movements—a story about messages that have not become words yet.",
    "ことりせんせいと読む": "Read with Kotori Sensei",
    "みんなの力をつなぐ": "BRINGING EVERYONE'S STRENGTHS TOGETHER",
    "きょうは、": "Whose turn",
    "だれの出番かな？": "is it today?",
    "困りごとに合わせて、8人の先生が「できる方法」をつないでいく一日。": "Eight teachers connect their ideas to find ways that work throughout one child's day.",
    "ヒーローチームと読む": "Read with the hero team",
    "8人の先生たち": "Eight HugMap teachers",
    "8人、それぞれの見つけ方。": "Eight teachers. Eight ways to notice.",
    "からだの感覚": "BODY & SENSORY EXPERIENCES",
    "りすせんせい、": "Risu Sensei,",
    "ぼくのからだは": "what is my body",
    "なにをさがしているの？": "looking for?",
    "行動を決めつけず、身体が探している感覚と安全な代わり方を考えるおはなし。": "A story about looking beyond behavior to understand sensory needs and find safer alternatives.",
    "りすせんせいと読む": "Read with Risu Sensei",
    "りすせんせい": "Risu Sensei",
    "見えない身体のがんばり": "THE BODY'S HIDDEN WORK",
    "うさぎせんせい、": "Usagi Sensei,",
    "「かんたん」って": "who decided",
    "だれがきめたの？": "this was “easy”?",
    "動きに必要な力を知り、道具と環境で「できる形」をつくるおはなし。": "A story about understanding what movement takes and creating a way to succeed through tools and surroundings.",
    "うさぎせんせいと読む": "Read with Usagi Sensei",
    "うさぎせんせい": "Usagi Sensei",
    "遊びとおてての成長": "PLAY & GROWING HAND SKILLS",
    "りすせんせいと、": "Risu Sensei and",
    "ふしぎなおてての": "the marvelous hands'",
    "たからばこ": "treasure chest",
    "触る、入れる、積む、つまむ。遊びながら「できる」がつながるおはなし。": "Touch, place, stack, and pinch—a story about how play connects new abilities.",
    "宝箱をひらく": "Open the treasure chest",
    "宝箱を案内するりすせんせい": "Risu Sensei guiding us through the treasure chest",
    "記録から見つける": "DISCOVERING THROUGH RECORDS",
    "ぽけっとさん、": "Pocket,",
    "ぼくの「いや！」は": "where did my “No!”",
    "どこからきたの？": "come from?",
    "一週間の小さな出来事を並べ、行動の前に重なっていた負担を見つけるおはなし。": "A story that lines up one week's small events to reveal the demands that built up before a behavior.",
    "ぽけっとさんと探す": "Investigate with Pocket",
    "ぽけっとさん": "Pocket",
}

COMMON = {
    "文字を大きく": "Larger text", "動きを減らす": "Reduce motion", "はじまり": "Start",
    "おはなしを読む ↓": "Read the story ↓", "おはなしを読む": "Read the story",
    "おはなしの あとに": "After the story", "もういちど読む": "Read again",
    "物語の進み具合": "Story progress",
}

HAND_TREASURE = COMMON | {
    "りすせんせいと、ふしぎなおてての宝箱": "Risu Sensei and the Marvelous Hands' Treasure Chest",
    "おてての成長・Activity編": "Growing Hand Skills · Activity Story",
    "りすせんせいと、": "Risu Sensei and", "ふしぎな おてての": "the marvelous hands'", "たからばこ": "treasure chest",
    "あそぶたび、": "Every time I play,", "おてての「できる」が つながっていく。": "my hands connect one new skill to the next.",
    "ぱかっ。": "Pop!", "あそびが いっぱい！": "It's full of ways to play!",
    "「きょうは どんな おててに": "“What will your hands", "であえるかな？": "discover today?", "」": "”",
    "おてての道 ①・感覚あそび": "Hands Path 1 · Sensory play", "さわる。おす。にぎる。": "Touch. Press. Squeeze.",
    "ふわふわの布、でこぼこボール、やわらかい粘土。": "Soft cloth, a bumpy ball, and squishy dough.",
    "手のひらと指が、いろんな感じに出会う。": "My palms and fingers meet all kinds of sensations.",
    "布": "Cloth", "感触ボール": "Sensory ball", "粘土": "Dough", "スポンジ": "Sponge",
    "おてての道 ②・入れる／出す": "Hands Path 2 · Put in / take out", "にぎって、はこんで、": "Hold it, carry it,", "はこの なかへ。ぱっ。": "and let go inside the box.",
    "出して、また入れて。持つ場所と離す場所がつながる。": "Take it out and put it back. The place I grasp and the place I let go begin to connect.",
    "ボール落とし": "Ball drop", "型はめ箱": "Shape sorter", "ポットン落とし": "Posting toy",
    "おてての道 ③・積む": "Hands Path 3 · Stack", "上を 見て、": "Look up,", "そーっと のせる。": "and place it gently.",
    "位置を合わせ、指をゆるめる。ひとつ、ふたつ、みっつ！": "Line it up and relax my fingers. One, two, three!",
    "大きな積み木": "Large blocks", "重ねカップ": "Stacking cups", "リング積み": "Stacking rings",
    "おてての道 ④・両手チーム": "Hands Path 4 · Two-hand team", "片手が もつ。": "One hand holds.", "もう片方が うごかす。": "The other hand moves.",
    "ふたを開ける、引っぱる、はがす。二つの手に別々の役目。": "Open, pull, peel. Each hand has its own job.",
    "ふた付き容器": "Lidded container", "面ファスナー": "Hook-and-loop fastener", "引っぱり玩具": "Pull toy",
    "おてての道 ⑤・つまむ／ねらう": "Hands Path 5 · Pinch / aim", "おやゆびと ゆびで、": "With my thumb and finger,", "ちいさく ぎゅっ。": "a tiny squeeze.",
    "つまんで、穴や印を見つけて、そこへ運ぶ。": "Pinch, find the hole or mark, and carry it there.",
    "大きなシール": "Large stickers", "ジャンボペグ": "Jumbo pegs", "洗濯ばさみ": "Clothespins",
    "おてての道 ⑥・紐通し": "Hands Path 6 · Threading", "穴を 見つけて、": "Find the hole,", "ひもを すーっ。": "and slide the string through.",
    "片手でビーズ、片手で紐。見る・合わせる・通す・引く。": "Bead in one hand, string in the other. Look, line up, thread, and pull.",
    "大きな紐通し": "Large threading beads", "穴あきカード": "Lacing cards", "太いひも": "Thick cord",
    "おてての道 ⑦・ハサミ": "Hands Path 7 · Scissors", "紙を もって、": "Hold the paper.", "ちょきん。ちょきん。": "Snip, snip.",
    "片手で紙を動かし、もう片方で開いて閉じる。": "One hand moves the paper while the other opens and closes.",
    "バネ付きハサミ": "Spring scissors", "細長い厚紙": "Narrow cardstock", "太い線": "Thick lines",
    "おてての道 ⑧・描く": "Hands Path 8 · Draw", "てん。せん。ぐるぐる。": "Dots. Lines. Swirls.",
    "腕を動かす線から、少しずつ指で動かす線へ。ぼくの絵が広がる。": "From lines moved by my whole arm to lines guided by my fingers. My pictures keep growing.",
    "太いクレヨン": "Chunky crayons", "三角クレヨン": "Triangular crayons", "スタンプ": "Stamps", "水ペン": "Water brush",
    "たからばこから、": "From the treasure chest,", "きょうの あそびを えらぶ。": "I choose today's play.",
    "大きさ、かたさ、持ち手、すべりにくさ。": "The right size, firmness, grip, and slip resistance.",
    "今のおててが、たくさん動ける道具。": "Tools that let my hands move in lots of ways right now.",
    "道具は、": "Tools are friends", "できるを ふやす なかま。": "that help me do more.",
    "さわるから、にぎるへ。": "From touching to holding.", "にぎるから、はなすへ。": "From holding to letting go.",
    "入れる。積む。両手。つまむ。通す。切る。描く。": "Put in. Stack. Use both hands. Pinch. Thread. Cut. Draw.",
    "昨日の遊びが、今日の力につながっている。": "Yesterday's play connects to today's abilities.",
    "おてての道は、どんどん ひろがる。": "The path for my hands keeps growing.",
    "さわる": "Touch", "入れる": "Put in", "積む": "Stack", "通す": "Thread", "切る": "Cut", "描く": "Draw",
    "たからばこに 入っていたのは、": "The treasure chest held", "おもちゃだけじゃなかった。": "more than toys.",
    "あそんで みつけた、たくさんの おてての力。": "It held all the abilities my hands discovered through play.",
    "きょうの「できた」が、": "What I did today", "あしたの あそびを ひらいていく。": "opens up tomorrow's play.",
    "りすせんせい": "Risu Sensei",
    "遊びの中で、手の力は重なりながら育ちます。": "Hand skills grow together through play.",
    "感覚遊び、入れる・出す、積む、両手操作、つまむ、紐通し、ハサミ、描画は、代表的なつながりです。実際の発達は重なり、順番が前後し、得意な活動も一人ひとり異なります。玩具は年齢だけでなく、本人の興味、現在の操作、安全性に合わせて選び、必要に応じてOT等へ相談してください。": "Sensory play, putting in and taking out, stacking, using both hands, pinching, threading, scissors, and drawing are common connections in hand development. In real life these skills overlap, emerge in different orders, and every child has different strengths. Choose toys for the child's interests, current abilities, and safety—not age alone—and consult an occupational therapist when needed.",
    "りすせんせいに相談する": "Talk with Risu Sensei",
}

WEEKLY_CLUES = COMMON | {
    "おひるね ○　ごはん ○": "Nap: good. Meal: good.", "ぽけっとさんが、": "Pocket",
    "一週間の小さな記録を並べ、子どもの行動の前に重なっていた負担と必要な支援を見つけるHugMapのデジタル絵本。": "A HugMap digital picture book that looks across one week to find the demands building up before a child's behavior and the support they may need.",
    "ぽけっとさん、ぼくの「いや！」はどこからきたの？": "Pocket, Where Did My “No!” Come From?",
    "記録で見つける編 ①": "Discovering Through Records · 1", "ぽけっとさん、": "Pocket,", "ぼくの「いや！」は": "where did my “No!”", "どこから きたの？": "come from?",
    "きょうだけを 見ても わからない。": "Looking at today alone wasn't enough.", "一週間を ならべたら、見えてきた。": "When we lined up the whole week, clues appeared.",
    "笑顔で立つ男の子": "A smiling boy", "記録が得意なぽけっとさん": "Pocket, who is good at keeping records",
    "きんようび・夕方": "FRIDAY · EVENING", "いやーっ！": "NOOO!", "げんかんで、音も くつも": "At the door, the sounds and my shoes", "ぜんぶ いやになった。": "suddenly felt like too much.",
    "ママが きいても、ぼくは うまく いえない。": "Mom asked, but I couldn't explain it.", "ぼくにも、わからない。": "I didn't know either.",
    "帰宅して耳をふさぎ、困っている男の子": "A distressed boy covering his ears after coming home",
    "「おなかが すいた？」": "“Are you hungry?”", "「くつが いや？」": "“Are your shoes bothering you?”", "「わがまま なの？」": "“Are you being difficult?”",
    "その しゅんかんだけでは、": "From that one moment alone,", "こたえは ひとつに きまらない。": "there isn't one certain answer.",
    "ぽけっとさんは、": "Pocket", "こたえを いわなかった。": "didn't give us an answer.", "「きょうを なおす前に、": "“Before we try to fix today,", "小さな できごとを あつめよう": "let's collect the small events.”",
    "いつ・どこで・その前に何があった？": "When and where? What happened just before?", "からだ・食事・睡眠・音・予定の変化は？": "What about his body, meals, sleep, sounds, or changes in plans?",
    "クリップボードを持つぽけっとさん": "Pocket holding a clipboard",
    "げつようび": "MONDAY", "いつもの 園。": "The usual preschool.", "いつもの おむかえ。": "The usual pickup.", "おひるね ○ ごはん ○": "Nap: good. Meal: good.", "帰ってからも、ゆっくり。": "A relaxed evening at home.", "この日は「いや！」が": "That day's “No!”", "小さかった。": "was small.", "月": "Mon", "いつも通り": "As usual",
    "かようび": "TUESDAY", "ホールに たくさんの 人。": "Lots of people in the hall.", "マイクの 大きな 音。": "A loud microphone.", "先生が「音のとき、耳をふさいだ」と": "His teacher wrote, “He covered his ears during the noise,”", "記録してくれた。": "in the day's notes.", "ぼくの中に、": "Inside me,", "音の つかれが のこった。": "the tiredness from the noise remained.", "火": "Tue", "大きな音": "Loud noise",
    "すいようび": "WEDNESDAY", "たのしい うんどう。": "Fun exercise.", "そのあと、おひるねは みじかめ。": "Then a short nap.", "たのしい日にも、からだは がんばっている。": "My body works hard even on fun days.", "楽しいと 疲れない、ではなかった。": "Having fun didn't mean I wasn't tired.", "からだの でんちは、": "My body's battery", "すこしずつ へっていた。": "was slowly running down.", "水": "Wed", "運動＋短い昼寝": "Exercise + short nap",
    "もくようび": "THURSDAY", "おむかえが、いつもより おそい。": "Pickup was later than usual.", "帰る みちも、ちがった。": "We took a different way home.", "小さな へんこうでも、次が見えないと": "Even a small change takes work", "ぼくは ずっと がんばっている。": "when I can't see what comes next.", "「ちがう」が、": "One more “different”", "もう ひとつ かさなった。": "was added to the pile.", "木": "Thu", "予定変更": "Plan changed",
    "きんようび": "FRIDAY", "大きな音。みじかい昼寝。": "Loud noise. A short nap.", "いつもと ちがう 予定。": "A change in plans.", "ひとつなら だいじょうぶでも、": "I might manage one,", "いくつも かさなると——": "but when several build up—", "げんかんで、ぼくの「もう いっぱい」が": "at the door, my “I've had enough”", "あふれたのかもしれない。": "may have overflowed.", "音": "Noise", "疲れ": "Tired", "変更": "Change", "もう": "TOO", "いっぱい": "MUCH",
    "一週間を ならべた。": "lined up the whole week.", "「いや！」の数を 数えるだけではなく、": "We didn't just count the “No!” moments.", "何も起きなかった日との ちがいも 見る。": "We also compared the days when nothing happened.", "犯人を きめるんじゃない。": "We weren't looking for something to blame.", "ぼくが 楽になる 手がかりを 見つける。": "We were looking for clues that could make things easier for me.", "疲": "Tired", "変": "Change", "金": "Fri",
    "つぎの 金ようびは、": "The next Friday,", "先に「やすむ」を つくった。": "we made room for rest ahead of time.", "帰る予定を 絵で知らせる。": "Show the homecoming plan in pictures.", "げんかんでは 話しかけすぎない。": "Use fewer words at the door.", "静かな場所、水分、ひと休み。": "A quiet place, a drink, and a break.", "「いや！」の あとではなく、": "Support me before I overflow,", "あふれる前に たすける。": "not only after my “No!”", "よてい": "PLAN", "しずか": "QUIET", "おみず": "DRINK", "やすむ": "REST",
    "つぎの きんようび": "THE NEXT FRIDAY", "ぼくは、げんかんで": "At the door, I", "やすむカードに 手を のばした。": "reached for the rest card.", "「いや！」が出ても だいじょうぶ。": "It is okay if “No!” still comes out.", "記録は ぼくを おとなしくするためじゃない。": "The records aren't meant to make me quiet.", "ぼくの「もう いっぱい」を、": "They help us notice my “I've had enough”", "早く いっしょに 気づくため。": "earlier, together.",
    "自分の希望を伝える男の子": "A boy communicating what he wants", "笑顔の男の子": "A smiling boy", "ぽけっとさん": "Pocket",
    "きょうだけでは 見えないことも、": "Some things are invisible in a single day,", "つなげると 見えてくる。": "but appear when we connect the days.", "ぼくの 毎日は、": "My everyday life", "ぼくを たすける 手がかりだった。": "was full of clues that could help me.",
    "記録は、原因を決めつけるためではありません。": "Records are not meant to declare a single cause.",
    "行動があった日だけでなく、なかった日も含めて、時刻・場所・直前の出来事・睡眠・食事・体調・感覚刺激・予定変更・周囲の対応を短く残します。数日から数週間を並べると、単独では見えにくい「重なり」が仮説になります。仮説は家庭・園・学校・支援職で共有し、安全を確かめながら小さく環境を変えて検証します。痛みや急な行動変化がある場合は、記録だけで判断せず医療職にも相談してください。": "Keep brief notes about the time, place, what happened just before, sleep, food, health, sensory input, changes in plans, and how others responded—on days when the behavior occurred and days when it did not. Looking across several days or weeks can reveal combinations that suggest a hypothesis. Share that hypothesis among family, preschool or school, and support professionals, then test small environmental changes safely. If there is pain or a sudden change in behavior, do not rely on records alone; consult a healthcare professional.",
    "HugMapで気づきをつなぐ": "Connect your observations with HugMap",
}

EVERY_STEP = COMMON | {
    "うさぎせんせいは、": "Usagi Sensei", "」": "”",
    "簡単に見える動きに必要な力とPTによる環境調整を描くHugMapのデジタル絵本。": "A HugMap digital picture book about the hidden work behind simple-looking movements and how physical therapy can shape supportive environments.",
    "うさぎせんせい、「かんたん」ってだれがきめたの？": "Usagi Sensei, Who Decided This Was “Easy”?",
    "からだのふしぎ編 ②・PT": "Body Wonders 2 · Physical Therapy", "うさぎせんせい、": "Usagi Sensei,", "「かんたん」って": "who decided", "だれが きめたの？": "this was “easy”?",
    "ひとつの うごきの なかには、": "Inside a single movement,", "みえない しごとが いっぱい。": "there is so much invisible work.",
    "すわる。": "Sit.", "ボールを とる。": "Catch a ball.", "かいだんを のぼる。": "Climb the stairs.", "みんなには、ひとつの うごき。": "For everyone else, each looks like one movement.", "でも ぼくには——": "But for me—", "いくつもの うごきを": "it means doing many movements", "いっしょに すること。": "all at once.", "すわる": "Sit", "とる": "Catch", "のぼる": "Climb",
    "あしが ぶらぶら。": "My feet dangle.", "からだが ぐらり。": "My body wobbles.", "おえかきしたいのに、ぼくの てまで ぐらぐらする。": "I want to draw, but even my hand wobbles.", "すわるには、": "To sit, I need to", "あしで ささえる・おなかを おこす・あたまを まっすぐ・めと てを うごかす": "support with my feet · hold up my trunk · keep my head steady · move my eyes and hands", "が いる。": "all together.",
    "うさぎせんせいが、": "Usagi Sensei", "あしだいを ことん。": "sets down a footrest.", "あしが ぺたん。おしりが あんてい。": "Feet flat. Hips steady.", "てが すーっと うごいた。": "My hand moves smoothly.", "「がんばる」を ふやすより、": "Instead of asking me to try harder,", "ぐらぐらを へらそう。": "let's reduce the wobble.",
    "ボールを とる": "Catch a ball", "見えているのに、": "I can see it,", "てが まにあわない。": "but my hands don't arrive in time.", "とるには、": "To catch, I need to", "めで みつける・うごきを おいかける・りょうてを のばす・からだを たおさない": "spot it · track it · reach both hands · keep my body upright", "めと てと からだを、": "My eyes, hands, and body", "おなじ ときに うごかす しごと。": "all have to work at the same time.",
    "ベンチで からだを": "We steady my body", "あんていさせて、": "on a bench,", "おおきな ボールを、ゆっくり。": "and use a big, slow ball.", "みる。まつ。てを のばす。": "Look. Wait. Reach.", "つかまえた！": "I caught it!", "ぼくに あう はやさなら、": "At a speed that suits me,", "めと ても であえる。": "my eyes and hands can meet.",
    "かいだんを のぼる": "Climb the stairs", "みんなは どんどん。": "Everyone else keeps going.", "ぼくは ぴたり。": "I stop still.", "のぼるには、": "To climb, I need to", "つぎの だんを みる・かたあしで ささえる・もう かたほうを あげる・たいじゅうを うつす": "see the next step · balance on one leg · lift the other · shift my weight", "一だんの なかに、": "Inside a single step,", "たくさんの しごと。": "there is so much work.",
    "ぼくの からだは、": "My body", "その しごとを まとめるのに": "needs a little more time", "すこし 時間が かかる。": "to bring that work together.", "力を たもちにくい。かんせつが やわらかい。": "My muscle tone is low. My joints are flexible.", "たつと かかとが かたむきやすい。": "When I stand, my heels tend to tilt.", "バランスを さがす 時間も いる。": "I need time to find my balance.", "どれも「だめ」じゃない。": "None of that is “bad.”", "ぼくの からだの とくちょう。": "It is how my body works.",
    "からだ": "Body", "ささえる": "Support", "かんせつ": "Joints", "やわらかい": "Flexible", "あし": "Feet", "ならべる": "Align", "め＋て": "Eyes + hands", "あわせる": "Coordinate",
    "「もっと がんばって」より": "looks before saying, “Try harder.”", "さきに みた。": "", "おなか。せなか。ひざ。あし。": "Trunk. Back. Knees. Feet.", "めせん。はやさ。つかれかた。": "Gaze. Speed. Fatigue.", "「むずかしい わけは、": "“There isn't just one reason", "ひとつじゃないね": "this is hard.”", "め": "Eyes", "せなか": "Back", "ひざ": "Knees",
    "うさぎせんせいの": "Usagi Sensei's", "どうぐばこ。": "toolbox.", "あしだい。ベンチ。かがみ。": "A footrest. Bench. Mirror.", "あしあと。てすり。ゆっくりの ボール。": "Footprints. A handrail. A slow ball.", "つかれたときの おやすみカード。": "A rest card for when I am tired.", "ぼくを なおす どうぐじゃない。": "These tools aren't here to fix me.", "ぼくの 力を つかう どうぐ。": "They help me use my abilities.",
    "てすりを ぎゅっ。": "Grip the handrail.", "あしあとを みる。": "Look at the footprints.", "ひくい だん。": "A low step.", "ぼくが うごくまで まつ 時間。": "Time to wait until I move.", "できる じゅんび": "prepares a way I can do it", "を してくれる。": ".",
    "つぎの だんを みる。": "Look at the next step.", "かたあしで ささえる。": "Balance on one leg.", "もう かたほうを あげる。": "Lift the other.", "いち、に。": "One, two.", "さいごの 一歩は、ぼくが だす。": "The final step is mine to take.",
    "ぼくは「できない」んじゃない。": "It isn't that I “can't.”", "ひとつずつ わかること。ぼくに あう どうぐ。ぼくに あう はやさ。": "One clear step at a time. Tools that fit me. A pace that fits me.", "できる かたちなら、": "When the way works for me,", "ぼくの 一歩は すすんでいく。": "my steps keep moving forward.",
    "うさぎせんせい": "Usagi Sensei", "一つの動きの中には、いくつもの身体の仕事があります。": "A single movement contains many jobs for the body.",
    "この物語の主人公は、ダウン症のある子どもです。低緊張に加え、筋力、関節の柔らかさ、足の位置、姿勢、バランス、目と手の協調、疲れやすさなどは一人ひとり異なります。行動を急がせる前に、動きに必要な力を分けて観察すると、支援の手がかりが見つかります。足台、椅子、手すり、段差、靴や装具などは、PT等による個別の評価と安全確認のうえで選んでください。": "The child in this story has Down syndrome. Along with low muscle tone, strength, joint flexibility, foot position, posture, balance, eye–hand coordination, and fatigue differ from child to child. Before rushing a movement, break down and observe the abilities it requires; this can reveal useful supports. Choose footrests, chairs, rails, step heights, shoes, and orthoses only after an individual assessment and safety check by a physical therapist or other qualified professional.",
    "うさぎせんせいに相談する": "Talk with Usagi Sensei",
}

BODY_WONDERS = COMMON | {
    "ダウン症のある子どもの感覚処理と、OT・摂食支援チームによる観察と環境調整を描くHugMapのデジタル絵本。": "A HugMap digital picture book about sensory processing in a child with Down syndrome and support from occupational therapy, feeding specialists, and the care team.",
    "りすせんせい、ぼくのからだは何をさがしているの？": "Risu Sensei, What Is My Body Looking For?", "からだのふしぎ編 ①・感覚処理": "Body Wonders 1 · Sensory Processing",
    "りすせんせい、": "Risu Sensei,", "ぼくの からだは": "what is my body", "なにを さがしているの？": "looking for?", "「もっと」「もう いや」": "“More.” “That's enough.”", "ぼくの からだには、ぼくだけの かんじかた。": "My body has its own way of sensing the world.",
    "ぼくの からだは、": "Sometimes my body", "ときどき ふしぎなことを する。": "does puzzling things.", "ぼくにも、どうしてなのか": "I can't yet explain", "まだ うまく いえない。": "why, either.", "「ちょうどいい かんじ」を": "Maybe it is looking for", "さがしているのかな。": "a feeling that is “just right.”",
    "あー。うー。": "Ahh. Ooh.", "のどの あたりを おして、": "I press around my throat", "かわる こえを たのしむ。": "and enjoy how my voice changes.", "のどの ふるえと、いつもと ちがう音。": "The vibration and the unusual sound", "ぼくには おもしろい あそび。": "feel like an interesting game to me.", "でも、のどを つよく おすのは きけん。": "But pressing hard on my throat is dangerous.", "まず やさしく とめてもらう。": "First, gently help me stop.",
    "ぎゅっ。": "Grip.", "ひとの かみを、": "I want to pull", "つよく ひっぱりたくなる。": "someone's hair hard.", "にぎる かんじ。ひっぱる かんじ。": "The feeling of gripping. The feeling of pulling.", "相手は いたい。でも ぼくは まだ わからない。": "It hurts them, but I don't understand that yet.", "手を やさしく とめて、": "Gently stop my hand", "かわりに にぎれるものへ。": "and offer something safe to grip instead.",
    "ごはんを、": "I fill", "くち いっぱいに。": "my whole mouth with food.", "すこしだと、くちの なかで": "With only a little, it can be hard", "「ごはんが ここに ある」が": "to feel exactly where", "わかりにくい ときがある。": "the food is in my mouth.", "いっぱいなら、": "With a full mouth,", "つよく かんじられる。": "I can feel it strongly.",
    "「のどは おさないよ」": "“Don't press your throat.”", "「かみを はなそう」": "“Let go of the hair.”", "「つめこまないで」": "“Don't stuff your mouth.”", "ママも こまっている。": "Mom is worried too.", "ぼくも、やめかたが わからない。": "I don't know how to stop.", "こまらせたいんじゃない。": "I'm not trying to cause trouble.", "からだが なにかを つたえている。": "My body is communicating something.",
    "りすせんせいは、": "Risu Sensei", "すぐに「感覚のせい」と": "doesn't immediately decide", "きめなかった。": "that sensory needs explain it.", "「いつ？ どこで？": "“When? Where?", "そのまえと あとは？": "What happened before and after?", "いっしょに みてみよう": "Let's look together.”", "まえ": "Before", "いま": "Now", "あと": "After",
    "からだの サインには、": "A body's signals can have", "いくつもの かのうせい。": "many possible meanings.", "もっと かんじたい？": "Wanting more sensation?", "つよすぎて つらい？": "Overwhelmed by too much?", "つかれた？ ひまだった？": "Tired? Bored?", "どこか いたい？ うまく できない？": "In pain? Finding something difficult?", "ひとつの 行動に、": "Don't give one behavior", "ひとつの こたえを つけない。": "only one answer.", "もっと": "More", "つよい": "Too much", "いたい": "Pain", "むずかしい": "Hard",
    "くち いっぱいには、": "A full mouth raises", "もうひとつ たいせつなこと。": "another important question.", "かばせんせいは、ひとくちの りょう。": "Kaba Sensei looks at bite size,", "かむこと。したの うごき。たべる はやさ。": "chewing, tongue movement, and eating speed,", "むせずに のみこめているかを みる。": "and whether I swallow without choking.", "感覚だけじゃなく、": "Not only sensation—", "たべる力と あんぜんも。": "eating skills and safety too.",
    "あしが ゆかに つく いす。": "A chair where my feet touch the floor.", "おさらには、ひとくちずつ。": "One bite at a time on the plate.", "つぎの ひとくちまで、ちょっと まつ。": "A short wait before the next bite.", "おとと においが つよい日は、しずかな ばしょ。": "A quiet place on days when sounds and smells are strong.", "ぼくを とめるより、": "Instead of only stopping me,", "あんぜんに わかる かたちへ。": "make it safe and easier to sense.",
    "ぼくは、音と ふるえを": "Sometimes I repeatedly seek", "くりかえし さがすこともある。": "sounds and vibration.", "はを ずっと ぎりぎり。": "Grinding my teeth.", "音の でる おもちゃを、なんども とんとん。": "Tapping a sound-making toy again and again.", "同じ音が かえってくると、わかりやすい。": "A sound that comes back the same way is predictable.", "安全に とめることと、": "Stop what is unsafe", "かわりの 感覚を さがすこと。": "and look for safer sensory alternatives.",
    "ひとりで きめない。": "doesn't decide alone.", "食べることは、かばせんせい。": "Kaba Sensei helps with eating.", "痛みや体調は、くませんせい。": "Kuma Sensei helps with pain and health.", "ママが みつけた「いつもと ちがう」も たいせつ。": "Mom's observations about what is unusual matter too.", "みんなの きづきを つなぐと、": "When everyone's observations connect,", "ぼくの サインが みえてくる。": "my signals come into view.",
    "ぼくの 行動は、": "My behavior", "こまらせるためじゃなかった。": "wasn't meant to cause trouble.", "「もっと かんじたい」": "“I need more sensation.”", "「これは つよすぎる」": "“This is too much.”", "「ちょっと いたい」「うまく できない」": "“Something hurts.” “This is hard.”", "ぼくの からだからの": "They were different stories", "いろんな おはなしだった。": "told by my body.",
    "りすせんせい": "Risu Sensei", "理解することと、安全に止めることは両立できます。": "Understanding a behavior and stopping it safely can happen together.",
    "喉元への圧迫、他人の髪を強く引く行動、長く続く歯ぎしりなどは、感覚を求める行動の可能性があっても、まず安全に止めてください。喉の痛み、声のかすれ、呼吸や飲み込みの変化がある場合は医療機関へ。歯ぎしりが続く場合は歯科等へ相談してください。口に食べ物を多く入れることも感覚だけで決めつけず、噛む力、舌の動き、一口量、姿勢、食べる速さ、嚥下を確認します。行動の前後を観察し、OT、摂食・嚥下を扱うST、医療職と安全な代替手段を検討してください。": "Even if pressing the throat, pulling another person's hair, or persistent tooth grinding may be sensory-seeking, stop the action safely first. Seek medical care for throat pain, hoarseness, or changes in breathing or swallowing, and dental advice for persistent grinding. Do not assume that overfilling the mouth is sensory alone; check chewing, tongue movement, bite size, posture, eating speed, and swallowing. Observe what happens before and after, and work with an occupational therapist, feeding or swallowing specialist, and healthcare professionals on safe alternatives.",
    "りすせんせいに相談する": "Talk with Risu Sensei",
}

HERO_TEAM = COMMON | {
    "子どもの一日をHugMapの先生たちがそれぞれの力で支えるデジタル絵本。": "A digital picture book about the HugMap teachers bringing their different strengths to support one child's day.",
    "HugMapヒーローズ — きょうは、だれの出番かな？": "HugMap Heroes — Whose Turn Is It Today?", "きょうは、": "Whose turn", "だれの出番かな？": "is it today?",
    "ぼくを かえるんじゃない。": "They aren't here to change me.", "ぼくに あう「できる」を": "They're heroes who help me find", "いっしょに みつける ヒーローたち。": "a way that works for me.",
    "あさ・きがえ": "MORNING · GETTING DRESSED", "ボタンが つまめない。": "I can't pinch the button.", "やりたいのに、ゆびが うまく うごかない。": "I want to do it, but my fingers won't move the way I need.", "「できない」って いわれると、かなしいな。": "It makes me sad when people say I “can't.”", "「できないんじゃないよ。": "“It isn't that you can't.", "やりやすい かたち": "Let's find a way", "を さがそう」": "that makes it easier.”", "りすせんせいの力": "RISU SENSEI'S POWER", "動きを小さく分け、道具や環境を整える": "Break movements into smaller parts and adjust tools and surroundings",
    "とうえん・かいだん": "ARRIVAL · STAIRS", "おちそうで こわい。": "I'm scared I might fall.", "みんなは どんどん のぼるけど、": "Everyone else climbs quickly,", "ぼくの あしは まだ じゅんびちゅう。": "but my legs are still getting ready.", "「はやさより、": "“Instead of speed, start with", "あんしんできる 一歩": "one step that feels safe", "から」": ". ”", "うさぎせんせいの力": "USAGI SENSEI'S POWER", "身体を支え、小さな成功を積み重ねる": "Support the body and build up small successes",
    "かつどう・みんなのせつめい": "ACTIVITY · GROUP INSTRUCTIONS", "ことばだけでは、わからない。": "Words alone aren't enough for me.", "なにを、どの じゅんばんで するのかな。": "What are we doing, and in what order?", "みんなが はじめても、ぼくは うごけない。": "Everyone starts, but I can't get moving.", "「おなじ ゴールでも、": "“We can have the same goal", "みえる道": "and a path you can see", "が あっていい」": ". ”", "ぞうせんせいの力": "ZOU SENSEI'S POWER", "絵や具体物で、学びへの別の道をつくる": "Create another path to learning with pictures and concrete objects",
    "おひる・ごはん": "LUNCH · EATING", "くちに いれると、びっくりする。": "Putting it in my mouth surprises me.", "かたさ、におい、おおきさ。": "Texture, smell, size.", "「たべない」には、わけが あるんだ。": "There is a reason behind “not eating.”", "「れんしゅうの まえに、": "“Before practice,", "あんしんして たべる": "make eating feel safe", "こと」": ". ”", "かばせんせいの力": "KABA SENSEI'S POWER", "食べやすい姿勢・形・量と安全を探す": "Find a safe posture, form, and amount that make eating easier",
    "あそび・ともだち": "PLAY · FRIENDS", "いっしょに あそびたい。": "I want to play together.", "おもちゃと ともだちを こうごに みる。": "I look back and forth between the toy and my friend.", "でも、ぼくの おさそいは まだ みつからない。": "But no one has noticed my invitation yet.", "「めも、てもしぐさも、": "“Your eyes, hands, and gestures—", "ぜんぶ おはなし": "they are all communication", "だよ」": ". ”", "ことりせんせいの力": "KOTORI SENSEI'S POWER", "ことばになる前のコミュニケーションを見つける": "Notice communication before it becomes words",
    "かえり・よていへんこう": "GOING HOME · CHANGE OF PLANS", "きゅうに かわると、こわい。": "A sudden change is scary.", "いつもの みちが とおれない。": "We can't take our usual route.", "ぼくは とまって、ないて、うごけなくなった。": "I stop, cry, and can't move.", "「こまった行動には、": "“Behind behavior that looks difficult,", "こまっている 理由": "there is a person having difficulty", "が ある」": ". ”", "ふくろうせんせいの力": "FUKUROU SENSEI'S POWER", "出来事・行動・必要な助けをつないで考える": "Connect events, behavior, and the help that may be needed",
    "おうち・いつもとちがう": "HOME · SOMETHING IS DIFFERENT", "きょうは、なんだか しんどい。": "Something feels hard today.", "ことばで「いたい」と いえなくても、": "Even when I can't say “it hurts,”", "ねむりや うごきが いつもと ちがう。": "my sleep and movements may be different.", "「あんしんすることも、": "“Reassurance matters,", "そうだんすること": "and so does asking for advice", "も だいじ」": ". ”", "くませんせいの力": "KUMA SENSEI'S POWER", "いつもとの違いを整理し、健康相談へつなぐ": "Organize what is different and connect the family with health advice",
    "よる・きょうのきろく": "EVENING · TODAY'S NOTES", "きょうの「できた」を、なくさない。": "Don't lose what worked today.", "ママが みつけたこと。": "What Mom noticed.", "せんせいと うまくいったこと。": "What worked with the teacher.", "ぼくが つたえたこと。": "What I communicated.", "「たいせつなこと、": "“I'll keep the important things", "ポケットに しまっておくね": "safe in my pocket", "ぽけっとさんの力": "POCKET'S POWER", "気づきや記録を預かり、次の支援者へつなぐ": "Keep observations and records safe, then pass them to the next supporter",
    "ぼくを かえるために": "They don't come", "くるんじゃない。": "to change me.", "ぼくが ぼくの ままで、": "They help me find", "できる ほうほうを": "ways I can succeed", "いっしょに みつけてくれる。": "while still being me.", "きょうは、だれの 出番かな？": "Whose turn is it today?",
    "ぽけっとさん": "Pocket", "困りごとに合う先生と、": "Find the right teacher for the challenge", "できる方法を探そう。": "and look for a way that works.",
    "ことば、手や感覚、身体、こころ、学び、食事、健康。HugMapでは、今気になることから相談する先生を選べます。まだ何に困っているか分からなくても大丈夫です。": "Language, hands and senses, movement, emotions, learning, eating, and health: HugMap lets you choose a teacher based on what concerns you now. It is also okay if you do not yet know exactly what the difficulty is.",
    "HugMapで先生を見つける": "Find a teacher with HugMap",
}

MOU_IKKAI = COMMON | {
    "ことばにならなくても、気持ちはここにある。HugMapのデジタル絵本。": "Feelings are here even when they are not spoken. A HugMap digital picture book.",
    "ことりせんせい、ぼくの「もういっかい」きこえた？": "Kotori Sensei, Did You Hear My “Again”?", "絵本の操作": "Story controls", "物語の最初へ": "Back to the beginning",
    "ことりせんせい、": "Kotori Sensei,", "ぼくの「もういっかい」": "did you hear my", "きこえた？": "“again”?", "ぼくは まいにち、": "Every day,", "からだじゅうで おはなししている。": "I talk with my whole body.", "スクロールして おはなしを読む": "Scroll to read the story",
    "ぼくは、まだ": "I don't use", "ことばを たくさん いわない。": "many words yet.", "でもね。": "But you know what?", "りょうてを のばして、": "I reach out both hands", "ママを みあげる。": "and look up at Mom.", "「だっこして」って": "I'm saying,", "いっているんだ。": "“Pick me up.”", "「だっこ？」": "“Up?”", "ママが きいて、": "Mom asks", "すこし まってくれた。": "and waits a little.", "ぼくは にっこり。": "I smile.", "つたわった！": "She understood!",
    "ふり": "Wiggle", "たのしい おとが きこえたら、": "When I hear a fun sound,", "あたまも からだも": "my head and body", "わくわく。": "wiggle with excitement.", "これも ぼくの おはなし。": "This is my communication too.",
    "でも、いやな ときは——": "But when I don't want something—", "かおを そむける。": "I turn my face away.", "てを とめる。": "I stop my hands.", "からだを かたくする。": "My body goes stiff.", "「いや」「まって」": "Maybe I'm saying,", "なのかもしれない。": "“No,” or “Wait.”",
    "あるひ、だいすきな": "One day, my favorite", "おんがくが とまりました。": "music stopped.", "ぼくは ママの そでを": "I gently pulled", "そっと ひきました。": "Mom's sleeve.", "「こっち。こっちだよ」": "“This way. Over here.”",
    "ついたのは、": "We arrived", "おんがくえほんの ところ。": "at my musical book.", "ちいさな ボタンに": "I placed my finger", "ゆびを おきました。": "on the tiny button.", "でも、ぼくの ちからでは": "But I wasn't strong enough", "おせません。": "to press it.", "ママの かおを みる。": "I looked at Mom.", "「いっしょに おして。もういっかい」": "“Help me press it. Again.”",
    "「おなかが すいたの？」": "“Are you hungry?”", "「ちがう おもちゃ？」": "“Do you want another toy?”", "ママも いっしょうけんめい。": "Mom was trying hard too.", "でも、まだ わかりません。": "But she still didn't understand.", "ぼくは もっと つよく": "I pulled her sleeve", "そでを ひきました。": "even harder.", "ぼくの おはなし、どこに いっちゃったの？": "Where did my message go?",
    "そのとき、ことりせんせいが": "Just then, Kotori Sensei", "やってきました。": "arrived.", "「だいじょうぶ。": "“It's okay.", "きみの めと てと": "I can hear the words", "からだの ことばも、": "spoken by your eyes, hands, and body too.”", "ぼくには きこえるよ。": "",
    "そでを ひく。": "Pull the sleeve.", "えほんへ いく。": "Go to the book.", "ボタンに ゆびを おく。": "Put a finger on the button.", "ママを みる。": "Look at Mom.", "ことりせんせいは、": "Kotori Sensei", "まえと あと": "what came before and after", "を みて、": "watched", "そっと まちました。": "and waited quietly.", "そで": "SLEEVE", "えほん": "BOOK", "ボタン": "BUTTON", "みる": "LOOK",
    "「いっしょに ボタンを おして、": "“Do you want help pressing the button", "この おんがくを": "so you can hear this song", "もういっかい": "again", "、かな？」": "?”", "ことりせんせいは": "Kotori Sensei didn't assume.", "きめつけないで、": "", "ぼくに きいてくれました。": "He asked me.",
    "ママも ぼくを みて、": "Mom looked at me too", "すこし まってから ききました。": "and asked after waiting a little.", "「いっしょに おして、もういっかい？」": "“Press it together, again?”", "ぼくは にっこり。あたまを ふりふり。": "I smiled and wiggled my head.", "ママと ぼくの ゆびで、ぽちっ。": "Mom's finger and mine went click.", "きこえた！ ぼくの「てつだって」と「もういっかい」。": "She heard me! She heard my “help me” and “again.”",
    "ぽけっとさん": "Pocket", "いつもの仕草にある「ことば」を、": "Let's discover the “words” in everyday gestures", "一緒に見つけよう。": "together.",
    "手を伸ばす、顔をそむける、袖を引く、物と人を交互に見る。同じ仕草でも、場面によって意味は変わります。まずは「見る・待つ・たしかめる」。HugMapでは、お子さんの表情や動き、その前後の出来事から、伝えたいことと関わり方を一緒に考えます。": "Reaching, turning away, pulling a sleeve, or looking back and forth between an object and a person: the same gesture can mean different things in different situations. Start by watching, waiting, and checking. HugMap helps you consider what your child may be communicating and how to respond by looking at expressions, movements, and what happens before and after.",
    "ことりせんせいの三つのヒント": "Kotori Sensei's three tips", "見る": "Watch", "視線・手・身体と、その前後を見る": "Watch the eyes, hands, body, and what happens around the gesture", "待つ": "Wait", "次のサインが出るまで、少し待つ": "Wait a little for the next signal", "たしかめる": "Check", "「もう一回かな？」と本人に聞く": "Ask the child, “Again?”",
    "ことりせんせいとサインを見つける": "Find signals with Kotori Sensei", "この絵本は一般的な情報をもとにした作品です。聞こえや発達について心配がある場合は、小児科・言語聴覚士などの専門職にご相談ください。": "This story is based on general information. If you have concerns about hearing or development, consult a pediatrician, speech-language therapist, or another qualified professional.",
    "閉じる": "Close", "HugMap・ことりせんせい": "HugMap · Kotori Sensei", "お子さんは、どんな方法で": "How does your child", "伝えていますか？": "communicate?", "今見られる伝え方を選んでください": "Select the ways your child communicates now",
    "手を伸ばす": "Reaching", "てを のばす": "reach", "頭を振る": "Shaking the head", "あたまを ふる": "shake head", "顔をそむける": "Turning away", "かおを そむける": "turn away", "袖を引く": "Pulling a sleeve", "そでを ひく": "pull sleeve", "視線を送る": "Looking at someone", "かおを みる": "look at face", "声を出す": "Vocalizing", "こえを だす": "make a sound", "物と人を交互に見る": "Looking between an object and person", "ものと ひとを みる": "look back and forth", "動きを止める": "Stopping movement", "うごきを とめる": "stop moving",
    "この内容で作ってみる": "Create with these choices", "もっとことりせんせいに相談する": "Ask Kotori Sensei more", "HugMapアプリを見る →": "See the HugMap app →",
}


class Translator(HTMLParser):
    def __init__(self, translations, page_kind, story=None):
        super().__init__(convert_charrefs=False)
        self.translations = translations
        self.page_kind = page_kind
        self.story = story
        self.out = []

    def handle_decl(self, decl): self.out.append(f"<!{decl}>")
    def handle_comment(self, data): self.out.append(f"<!--{data}-->")
    def handle_entityref(self, name): self.out.append(f"&{name};")
    def handle_charref(self, name): self.out.append(f"&#{name};")
    def handle_endtag(self, tag): self.out.append(f"</{tag}>")
    def handle_data(self, data):
        stripped = data.strip()
        if stripped in self.translations:
            data = data.replace(stripped, self.translations[stripped])
        self.out.append(data)

    def handle_startendtag(self, tag, attrs): self._tag(tag, attrs, True)
    def handle_starttag(self, tag, attrs): self._tag(tag, attrs, False)

    def _tag(self, tag, attrs, closed):
        rendered = []
        for key, value in attrs:
            if value is None:
                rendered.append(key); continue
            if key in {"content", "title", "alt", "aria-label", "value"} and value in self.translations:
                value = self.translations[value]
            if key == "lang" and value == "ja": value = "en"
            elif self.page_kind == "top" and key == "lang" and value == "en": value = "ja"
            if self.page_kind == "top" and key in {"src", "href"} and value.startswith("shared/"):
                value = "../" + value
            if self.page_kind == "top" and key == "href" and value == "en/": value = "../"
            if self.page_kind == "story" and key in {"src", "href"}:
                if value == "../../shared/story-runtime.js": value = "../../story-runtime.js"
                elif self.story == "mouikkai" and value == "story.js": value = "../../mouikkai-story.js"
                elif value.startswith("../../shared/"): value = "../../../shared/" + value.removeprefix("../../shared/")
                elif value.startswith("assets/"): value = f"../../../stories/{self.story}/" + value
                elif value.startswith("styles.css"): value = f"../../../stories/{self.story}/" + value
                elif value == "story.js": value = f"../../../stories/{self.story}/story.js"
            rendered.append(f'{key}="{escape(value, quote=True)}"')
        self.out.append("<" + tag + (" " + " ".join(rendered) if rendered else "") + (" />" if closed else ">"))


def render(source, target, translations, page_kind, story=None):
    parser = Translator(translations, page_kind, story)
    parser.feed(source.read_text())
    target.parent.mkdir(parents=True, exist_ok=True)
    output = "".join(parser.out)
    output = output.replace("299件のQ&amp;Aから、理由と関わり方を探す。", "Explore 299 questions and answers about possible reasons and ways to help.")
    target.write_text(output)


render(ROOT / "index.html", ROOT / "en/index.html", TOP, "top")
render(ROOT / "stories/hand-treasure/index.html", ROOT / "en/stories/hand-treasure/index.html", HAND_TREASURE, "story", "hand-treasure")
render(ROOT / "stories/weekly-clues/index.html", ROOT / "en/stories/weekly-clues/index.html", WEEKLY_CLUES, "story", "weekly-clues")
render(ROOT / "stories/every-step/index.html", ROOT / "en/stories/every-step/index.html", EVERY_STEP, "story", "every-step")
render(ROOT / "stories/body-wonders/index.html", ROOT / "en/stories/body-wonders/index.html", BODY_WONDERS, "story", "body-wonders")
render(ROOT / "stories/hero-team/index.html", ROOT / "en/stories/hero-team/index.html", HERO_TEAM, "story", "hero-team")
render(ROOT / "stories/mouikkai/index.html", ROOT / "en/stories/mouikkai/index.html", MOU_IKKAI, "story", "mouikkai")
