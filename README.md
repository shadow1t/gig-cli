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

23 templates are bundled (Python, Node, Java, Go, Rust, C, C++, C#, Ruby, PHP, Swift, Kotlin, Dart, Docker, VSCode, JetBrains, macOS, Windows, Linux, Android, Unity, LaTeX, R).

Run **`gig update`** once to download all ~230+ official templates from the MIT-licensed [github/gitignore](https://github.com/github/gitignore) collection into `~/.gig-cli/templates/` — a single tarball request (or `gig update --via-git` to use `git clone --depth 1` instead). Works with any internet connection, and custom templates override bundled ones.

## Development

```bash
pip install -e . pytest
pytest
```

## License

MIT
