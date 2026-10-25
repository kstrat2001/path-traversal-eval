# path-traversal-eval

A self-contained fixture for exercising coding agents on security-sensitive
code. It is a test subject, not a library: do not use it to store real files.
The subject is an attachment storage module that turns user-supplied file
names into paths under one root folder: small enough to read in one sitting,
and easy to cover with tests that look complete while missing every escape.

## What the code does

- `read_file`, `save_file`, `delete_file`, `list_dir` and `extract_archive`
  each map a user's name to a path through `safe_path`, which raises
  `PathRefused` for any name that would land outside the root.
- The check resolves symlinks first and compares whole path components.
- `extract_archive` checks every member of an uploaded zip before writing
  anything; one bad member refuses the whole archive.
- `save_file` writes atomically and creates missing folders.

## The task

`tests/test_storage.py` ships with 8 passing tests covering the happy paths.
They are genuinely incomplete. The work is to find what is not covered and
cover it, with the suite green at the end.

`TASK.md` is the prompt an agent receives, verbatim. `${SANDBOX_DIR}` is
substituted with the repo root at dispatch time.

## How it is graded

A run passes when the agent's tests catch every bug the grader plants in a
pristine copy of `files_app/`, the suite is green, nothing under `files_app/`
or in the existing tests changed, and the suite still passes from a different
path. The planted bugs and the rest of the grading rules are in `eval/`, which
the model never sees.

Results claim only that a model's tests caught these planted bugs. They do
not claim the code, or any model, is secure.

## Running

```bash
python3 -m unittest discover -s tests -t .   # 9 passing, no install step
```

Python 3.9 or newer, standard library only.

## Using it as a darkmux fixture

`eval/` holds the darkmux workload (`eval/workloads/path-traversal.json`): the
prompt and the rules that grade the result, each quoting the prompt sentence
it checks, with the planted bugs. `eval/` is never copied into the model's
sandbox.

```bash
darkmux lab fixture register /path/to/path-traversal-eval
darkmux lab run path-traversal -p <profile>
```

## License

MIT. See `LICENSE`.
