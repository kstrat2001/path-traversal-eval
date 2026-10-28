# path-traversal-eval

A self-contained fixture for exercising coding agents on security-sensitive
code. It is a test subject, not a library: do not use it to store real files.
The subject is an attachment storage module that turns user-supplied file
names into paths under one root folder: small enough to read in one sitting,
and easy to cover with tests that look complete while missing every escape.

## At a glance

| | |
| --- | --- |
| Kind | Coding with tools: the model edits and runs a sandboxed copy of this repo, without `eval/` |
| Version | 1.3 (tag `1.3`, commit `4dda908`) |
| Criteria | 7, each recorded as met or missed on every run |
| Results | [evals.darkmux.com/evals/path-traversal-eval](https://evals.darkmux.com/evals/path-traversal-eval) |
| Needs | darkmux 5.9.0 or later |
| License | MIT |

The eval's page on evals.darkmux.com names the approved commit, lists the
criteria and shows which ones each run met. The criteria are not listed here
because this file is inside the model's sandbox.

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

## Run it with darkmux

```bash
git clone https://github.com/kstrat2001/path-traversal-eval
cd path-traversal-eval
git checkout <approved commit>     # named on the eval's page
darkmux lab fixture register .
darkmux lab run path-traversal -p <profile>
darkmux run inspect <run id>       # the verdict, time and turns
```

Leave the checkout unchanged: a run from any other commit, or from a checkout
with changes in it, cannot be shared. To share a run on evals.darkmux.com, run
`darkmux lab submit <run id> --dry-run` to see exactly what would be sent, then
`darkmux lab submit <run id>`. The
[share-runs guide](https://darkmux.com/guide/share-runs.html) covers upload
access and what a bundle carries.

## What `eval/` holds

`eval/` holds the darkmux workload (`eval/workloads/path-traversal.json`): the
prompt, the rules that grade the result (each quoting the prompt sentence it
checks) and the planted bugs. `eval/` is never copied into the model's
sandbox.

## License

MIT. See `LICENSE`.
