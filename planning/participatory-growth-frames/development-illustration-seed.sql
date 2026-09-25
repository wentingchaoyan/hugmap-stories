-- Development only: dltohjfxawjonomvxfsd. Upload PNG assets before applying.

BEGIN;

INSERT INTO public.illustration (id, category_stage_id, code, asset_key, title_ja, alt_text_ja, display_order, storage_bucket, aspect_ratio, scene_label_ja, card_note_ja, is_active, is_deleted_flag) VALUES
('6b75ac6f-ebd5-54a5-b79b-8c12a940d9fc', '550e8400-e29b-41d4-a716-446655440036', 'mimo-frame-two-word-found-mom', 'mimo-frame-two-word-found-mom.png', 'ママ、いた。見つけたことを伝える', 'ママ、いた。見つけたことを伝える', 1, 'public-assets', '1:1', 'ことばをつないで伝える', NULL, true, false),
('b21aa262-24b1-5f77-a6f5-dc2caaa18914', '550e8400-e29b-41d4-a716-446655440036', 'mimo-frame-possessive-dads-shoes', 'mimo-frame-possessive-dads-shoes.png', 'パパの、くつ。持ち主へ届ける', 'パパの、くつ。持ち主へ届ける', 2, 'public-assets', '1:1', 'ことばをつないで伝える', NULL, true, false),
('ab572058-9eef-584b-8d56-57849e3224bb', '550e8400-e29b-41d4-a716-446655440036', 'mimo-frame-object-action-kick-ball', 'mimo-frame-object-action-kick-ball.png', 'ボール、ける。やりたいことを伝える', 'ボール、ける。やりたいことを伝える', 3, 'public-assets', '1:1', 'ことばをつないで伝える', NULL, true, false),
('d93c6758-14f2-5ad4-a47d-adfb5b4be728', '550e8400-e29b-41d4-a716-446655440036', 'mimo-frame-location-up-there', 'mimo-frame-location-up-there.png', '上に、ある。場所をいっしょに確かめる', '上に、ある。場所をいっしょに確かめる', 4, 'public-assets', '1:1', 'ことばをつないで伝える', NULL, true, false),
('76b73fdb-9841-5c4c-acf9-e18fd4c38216', '550e8400-e29b-41d4-a716-446655440036', 'mimo-frame-word-sound-picture-play', 'mimo-frame-word-sound-picture-play.png', '絵と身ぶりで、ことばをつなぐ', '絵と身ぶりで、ことばをつなぐ', 5, 'public-assets', '1:1', 'ことばをつないで伝える', '「かさ・はこ・ぞう」などの命名や音遊びの場面。発音の達成判定を示すものではありません。', true, false),
('0c9e224c-39a2-52da-8c46-bf2a1bb1a6e5', '550e8400-e29b-41d4-a716-446655440001', 'luke-frame-visual-tracking-cloth', 'luke-frame-visual-tracking-cloth.png', 'ふわり、目で追いかけた', '動くものを目で追う：ふわり、目で追いかけた', 1, 'public-assets', '1:1', '動くものを目で追う', NULL, true, false),
('a459ffd3-f717-5c11-8f0b-2f9bb7b29bcf', '550e8400-e29b-41d4-a716-446655440012', 'luke-frame-look-and-reach-both-hands', 'luke-frame-look-and-reach-both-hands.png', '見つけて、両手がのびた', '見ながら手を伸ばす：見つけて、両手がのびた', 1, 'public-assets', '1:1', '見ながら手を伸ばす', NULL, true, false),
('1dc6ab7c-adc6-5ede-bd06-add61f01ac19', '550e8400-e29b-41d4-a716-446655440003', 'luke-frame-watch-spinning-toy', 'luke-frame-watch-spinning-toy.png', 'くるくる、気になるね', '気になるものを見つめる：くるくる、気になるね', 1, 'public-assets', '1:1', '気になるものを見つめる', '興味を向けて遊びに参加する場面の提案。集中の持続時間を絵で判定するものではありません。', true, false),
('a9824ea6-1f8a-5c4f-9960-23bcfa021cdb', '550e8400-e29b-41d4-a716-446655440043', 'luke-frame-remember-hidden-toy', 'luke-frame-remember-hidden-toy.png', 'さっきの場所に、あった', '覚えて、思い出す：さっきの場所に、あった', 1, 'public-assets', '1:1', '覚えて、思い出す', NULL, true, false),
('7a4b9ec1-910d-5606-ab4e-464574f1268e', '550e8400-e29b-41d4-a716-446655440002', 'mimo-frame-notice-gentle-sound', 'mimo-frame-notice-gentle-sound.png', 'あれ、音のするほうへ', '声や音に気づく：あれ、音のするほうへ', 1, 'public-assets', '1:1', '声や音に気づく', NULL, true, false)
ON CONFLICT (id) DO UPDATE SET category_stage_id = EXCLUDED.category_stage_id, code = EXCLUDED.code, asset_key = EXCLUDED.asset_key, title_ja = EXCLUDED.title_ja, alt_text_ja = EXCLUDED.alt_text_ja, display_order = EXCLUDED.display_order, storage_bucket = EXCLUDED.storage_bucket, aspect_ratio = EXCLUDED.aspect_ratio, scene_label_ja = EXCLUDED.scene_label_ja, card_note_ja = EXCLUDED.card_note_ja, is_active = EXCLUDED.is_active, is_deleted_flag = EXCLUDED.is_deleted_flag;

INSERT INTO public.illustration_development_item (illustration_id, development_item_id, display_order, is_primary) VALUES
('6b75ac6f-ebd5-54a5-b79b-8c12a940d9fc', 'd1bf266b-46d4-4f81-a6cf-e37b272c1f3a', 1, false),
('b21aa262-24b1-5f77-a6f5-dc2caaa18914', 'd8a6e7d6-923a-4617-b1d6-539d7377bc70', 1, false),
('ab572058-9eef-584b-8d56-57849e3224bb', '76541fb2-99de-4be4-813b-3443acbd60c9', 1, false),
('ab572058-9eef-584b-8d56-57849e3224bb', '48ccd3a7-3e63-dbe3-3a3d-a7ee92a19b30', 2, false),
('d93c6758-14f2-5ad4-a47d-adfb5b4be728', 'e4b00712-7d3b-4d32-9f72-fd49a03a31d6', 1, false),
('76b73fdb-9841-5c4c-acf9-e18fd4c38216', '48ccd3a7-3e63-dbe3-3a3d-a7ee92a19b30', 1, false),
('76b73fdb-9841-5c4c-acf9-e18fd4c38216', '347de6e9-8d11-4487-92b1-a58666d43d6a', 2, false),
('76b73fdb-9841-5c4c-acf9-e18fd4c38216', 'a631850a-2faf-4b89-9a83-78a5faa02e7b', 3, false),
('0c9e224c-39a2-52da-8c46-bf2a1bb1a6e5', 'c5d54cb8-10a2-47ef-bcd2-d2625e70fbd2', 1, false),
('0c9e224c-39a2-52da-8c46-bf2a1bb1a6e5', '8e7d2aac-d59f-489f-bf2c-cbc188123cac', 2, false),
('a459ffd3-f717-5c11-8f0b-2f9bb7b29bcf', 'eb3e9c8c-7c1b-49c0-8d26-b38c2885df55', 1, false),
('a459ffd3-f717-5c11-8f0b-2f9bb7b29bcf', 'c28833e8-6d3b-4990-8d59-cd3c467fe60a', 2, false),
('1dc6ab7c-adc6-5ede-bd06-add61f01ac19', '8a702cfc-d5cd-46b2-bd6a-0642cc69d415', 1, false),
('a9824ea6-1f8a-5c4f-9960-23bcfa021cdb', '4891c484-4364-441b-9753-9325abf6d295', 1, false),
('7a4b9ec1-910d-5606-ab4e-464574f1268e', '06150ab9-c40e-46dc-a829-0b80a65dcbb5', 1, false)
ON CONFLICT (illustration_id, development_item_id) DO UPDATE SET display_order = EXCLUDED.display_order, is_primary = EXCLUDED.is_primary;

COMMIT;
