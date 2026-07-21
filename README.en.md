# HugMap Stories

[日本語 README](README.md)

HugMap Stories is a standalone static website of digital picture books based on HugMap's official characters and support principles.

It is kept separate from the main `withu` repository so published stories do not change unexpectedly when the app changes. Character, design, FAQ, and activity references are reviewed and synchronized during production, but the site has no direct dependency on production app files or databases.

## Structure

```text
hugmap-stories/
├── index.html                 # Japanese series landing page
├── en/                        # English landing page and stories
├── shared/                    # Shared styles, runtime, and characters
├── stories/                   # Japanese stories and story-specific assets
├── scripts/build_english.py   # Hand-maintained English edition builder
└── planning/                  # Character, story, and synchronization guidance
```

## Read locally

Open `index.html` for Japanese or `en/index.html` for English. No build step is required to read the checked-in pages.

After changing Japanese copy, update its hand translation in `scripts/build_english.py`, then rebuild the English static pages:

```sh
python3 scripts/build_english.py
```

## Add a story

1. Create `stories/<story-slug>/`.
2. Load `../../shared/base.css` and `../../shared/story-runtime.js`.
3. Set `<body data-story-pages="page-count">`.
4. Give each panel a sequential `data-step`.
5. Follow the relevant documents under `planning/`.
6. Record each page's role, artwork, motion, and supporting information in the story's `script.md`.
7. Add and review the English translation in `scripts/build_english.py`.

For static hosting, use the repository root as the publish directory.
