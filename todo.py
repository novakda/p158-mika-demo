"""Tiny command-line todo app. Stdlib only."""
import json
import os
import sys

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


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        sys.exit("usage: todo.py add TEXT | list | done ID | remove ID")
    cmd, args = argv[0], argv[1:]
    items = load()

    if cmd == "add" and args:
        item = {"id": max([i["id"] for i in items], default=0) + 1, "text": " ".join(args), "done": False}
        items.append(item)
        save(items)
        print(f"added {item['id']}: {item['text']}")
    elif cmd == "list":
        for i in items:
            print(f"{i['id']:>3} [{'x' if i['done'] else ' '}] {i['text']}")
    elif cmd in ("done", "remove") and len(args) == 1 and args[0].isdigit():
        item = find(items, int(args[0]))
        if cmd == "done":
            item["done"] = True
        else:
            items.remove(item)
        save(items)
        print(f"{cmd} {item['id']}")
    else:
        sys.exit("usage: todo.py add TEXT | list | done ID | remove ID")


if __name__ == "__main__":
    main()
