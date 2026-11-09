import argparse
import sys

from . import __version__, core


def _cmd_list(args) -> int:
    templates = core.available_templates()
    if core.USER_TEMPLATES_DIR.is_dir():
        custom = {core._normalize_name(core._strip_name(p.name)) for p in core.USER_TEMPLATES_DIR.glob("*.gitignore")}
    else:
        custom = set()
    for name in sorted(templates):
        marker = " (custom)" if name in custom else ""
        print(name + marker)
    print(f"\n{len(templates)} templates available.", file=sys.stderr)
    return 0


def _cmd_show(args) -> int:
    templates = core.available_templates()
    name = core.resolve_name(args.language)
    if name not in templates:
        print(f"error: unknown template '{args.language}'. Try: gig search {args.language}", file=sys.stderr)
        return 1
    sys.stdout.write(templates[name])
    return 0


def _cmd_search(args) -> int:
    matches = core.search_templates(args.term)
    if not matches:
        print(f"no templates matching '{args.term}'", file=sys.stderr)
        return 1
    for match in matches:
        print(match)
    return 0


def _cmd_gen(args) -> int:
    try:
        content = core.generate(args.languages)
    except KeyError as exc:
        missing = ", ".join(exc.args[0])
        print(f"error: unknown template(s): {missing}. Run 'gig list' to see all.", file=sys.stderr)
        return 1
    if args.output:
        path = core.write_gitignore(content, append=args.append)
        print(f"written to {path}", file=sys.stderr)
    else:
        sys.stdout.write(content)
    return 0


def _cmd_init(args) -> int:
    templates = sorted(core.available_templates())
    print("Available templates:")
    for i, name in enumerate(templates, 1):
        print(f"  {i:2d}. {name}")
    raw = input("\nPick numbers separated by spaces (e.g. 1 5 12): ").strip()
    if not raw:
        print("cancelled.", file=sys.stderr)
        return 1
    try:
        picks = [templates[int(n) - 1] for n in raw.split()]
    except (ValueError, IndexError):
        print("error: invalid selection.", file=sys.stderr)
        return 1
    content = core.generate(picks)
    path = core.write_gitignore(content, append=args.append)
    print(f"created {path} with: {', '.join(picks)}", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gig",
        description="gig-cli - fast, offline .gitignore generator for any language.",
    )
    parser.add_argument("--version", action="version", version=f"gig-cli {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list all available templates")
    p_list.set_defaults(func=_cmd_list)

    p_show = sub.add_parser("show", help="print a template to stdout")
    p_show.add_argument("language", help="template name or alias (e.g. python, py, node)")
    p_show.set_defaults(func=_cmd_show)

    p_search = sub.add_parser("search", help="search templates by name")
    p_search.add_argument("term", help="search term")
    p_search.set_defaults(func=_cmd_search)

    p_gen = sub.add_parser("gen", help="generate a combined .gitignore")
    p_gen.add_argument("languages", nargs="+", help="one or more languages/aliases")
    p_gen.add_argument("-o", "--output", action="store_true", help="write to ./.gitignore instead of stdout")
    p_gen.add_argument("--append", action="store_true", help="append to existing .gitignore instead of overwriting")
    p_gen.set_defaults(func=_cmd_gen)

    p_init = sub.add_parser("init", help="interactive mode: pick templates by number")
    p_init.add_argument("--append", action="store_true", help="append to existing .gitignore")
    p_init.set_defaults(func=_cmd_init)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
