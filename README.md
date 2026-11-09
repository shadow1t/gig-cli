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
```

### Aliases

`py` → python, `js`/`ts` → node, `golang` → go, `c++` → cpp, `c#` → csharp, `mac` → macos, and more.

## Custom templates

Drop your own `*.gitignore` files into:

```
~/.gig-cli/templates/
```

They override bundled templates with the same name.

## Bundled templates

Python, Node, Java, Go, Rust, C, C++, C#, Ruby, PHP, Swift, Kotlin, Dart/Flutter, Docker, VSCode, JetBrains, macOS, Windows, Linux, Android, Unity, LaTeX, R.

Templates are adapted from the MIT-licensed [github/gitignore](https://github.com/github/gitignore) collection.

## Development

```bash
pip install -e . pytest
pytest
```

## License

MIT
