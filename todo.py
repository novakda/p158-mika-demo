"""Tiny command-line todo app. Stdlib only."""
import json
import os
import sys
from datetime import datetime

USAGE = "usage: todo.py add TEXT [--due YYYY-MM-DD] | list | done ID | remove ID"
TODO_FILE = os.environ.get("TODO_FILE") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo.json")


def load():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, encoding="utf-8") as f:
        return json.load(f)


def save(items):
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)


def find(items, item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    sys.exit(f"error: no item with id {item_id}")


def parse_due(args):
    """Split off an optional `--due YYYY-MM-DD`; return (text_args, due_or_None)."""
    if "--due" not in args:
        return args, None
    pos = args.index("--due")
    if pos + 1 >= len(args):
        sys.exit("error: --due requires a date in YYYY-MM-DD format")
    due = args[pos + 1]
    try:
        datetime.strptime(due, "%Y-%m-%d")
    except ValueError:
        sys.exit(f"error: invalid date {due!r}, expected YYYY-MM-DD")
    return args[:pos] + args[pos + 2:], due


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        sys.exit(USAGE)
    cmd, args = argv[0], argv[1:]
    items = load()

    if cmd == "add" and args:
        args, due = parse_due(args)
        if not args:
            sys.exit(USAGE)
        item = {"id": max([i["id"] for i in items], default=0) + 1, "text": " ".join(args), "done": False}
        if due:
            item["due"] = due
        items.append(item)
        save(items)
        print(f"added {item['id']}: {item['text']}" + (f" (due {due})" if due else ""))
    elif cmd == "list":
        # ISO dates sort correctly as strings; undated items go last.
        for i in sorted(items, key=lambda i: (i.get("due") is None, i.get("due") or "", i["id"])):
            due = f" (due {i['due']})" if i.get("due") else ""
            print(f"{i['id']:>3} [{'x' if i['done'] else ' '}] {i['text']}{due}")
    elif cmd in ("done", "remove") and len(args) == 1 and args[0].isdigit():
        item = find(items, int(args[0]))
        if cmd == "done":
            item["done"] = True
        else:
            items.remove(item)
        save(items)
        print(f"{cmd} {item['id']}")
    else:
        sys.exit(USAGE)


if __name__ == "__main__":
    main()
