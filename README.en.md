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

## Planning entry points

See [`planning/README.md`](planning/README.md) for the role and reading order of the planning documents.

| Question | Source |
|---|---|
| Series values, teacher profiles, age, and gender | [`planning/world-and-character-guide.md`](planning/world-and-character-guide.md) |
| International character names, comparisons, and rejected options | [`planning/character-naming-strategy.md`](planning/character-naming-strategy.md) |
| Decisions that are still open | [`planning/open-decisions.md`](planning/open-decisions.md) |
| Story priorities and character-specific ideas | [`planning/story-backlog.md`](planning/story-backlog.md) |
| Visual-style and production-method comparisons | [`planning/visual-style-decision.md`](planning/visual-style-decision.md) |

### Current naming candidates

The current first-round candidates for the three main teachers are **Mimo** for the bird, **Luke** for the squirrel, and **Gen** for the rabbit. These are not official names. They still require testing with the artwork and children, pronunciation checks across languages, and existing-name and trademark screening.

Comparisons and reasons for rejecting earlier options are maintained in `character-naming-strategy.md`. Official names will be copied to `world-and-character-guide.md` and the stories only after a decision is made.

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
