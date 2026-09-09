# p158-mika-demo

Small demo project for trying out Mika.

## todo.py

Minimal command-line todo list. Python 3, stdlib only.

```
python todo.py add "buy milk"
python todo.py list
python todo.py done 1
python todo.py remove 1
```

Items are stored in `todo.json` next to the script, or in the path set by the
`TODO_FILE` environment variable. Run the tests with `python -m unittest`.
