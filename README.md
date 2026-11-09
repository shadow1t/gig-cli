# gig-cli ⚡

Fast, **offline** `.gitignore` generator CLI. Pick one or more languages, get a clean, deduplicated `.gitignore` — no website, no copy-paste.

## Install

```bash
pip install .
# or run without installing:
python -m gig --help
```

## Usage

```bash
# List all available templates
gig list

# Search templates
gig search py

# Print a template to stdout
gig show python

# Generate a combined .gitignore for multiple languages (deduplicated)
gig gen python node docker

# Write directly to ./.gitignore
gig gen python node -o

# Append to an existing .gitignore
gig gen docker -o --append

# Interactive mode: pick templates by number
gig init

# Download ALL official templates from github/gitignore (one request, ~230+ templates)
gig update

# Alternative: clone via git instead of the tarball download
gig update --via-git
```

### Aliases

`py` → python, `js`/`ts` → node, `golang` → go, `c++` → cpp, `c#` → csharp, `mac` → macos, and more.

## Custom templates

Drop your own `*.gitignore` files into:

```
~/.gig-cli/templates/
```

They override bundled templates with the same name.

## Templates

**All 248 official templates are bundled** in `gig/templates/` (from the MIT-licensed [github/gitignore](https://github.com/github/gitignore) collection) — the tool works fully offline out of the box.

Run **`gig update`** to refresh them with the latest upstream version (single tarball request, or `gig update --via-git` to use `git clone --depth 1` instead); downloaded templates go to `~/.gig-cli/templates/` and override bundled ones.

## Web UI

A static single-page app lives in [`web/`](web/) — search 248 templates, multi-select, live deduplicated preview, copy/download, shareable links, dark mode. No server needed.

It is deployed automatically to **GitHub Pages** on every push to `main` (see `.github/workflows/deploy-pages.yml`), or run locally:

```bash
python -m http.server -d web 8000
# open http://localhost:8000
```

`web/templates.js` is generated from the bundled templates:

```bash
python scripts/build_templates_js.py
```

## Development

```bash
pip install -e . pytest
pytest                 # Python tests
node tests/test_web.js # web UI logic tests
```

## License

MIT
