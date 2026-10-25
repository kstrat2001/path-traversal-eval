# How path-traversal-eval is graded

This folder is never copied into the model's sandbox. `workloads/path-traversal.json`
holds the prompt and the grading rules; each rule quotes the prompt sentence it grades.
`DESCRIPTION.md` is the eval's public write-up: the attack and the incidents it comes from.

The grader plants one bug at a time in a pristine copy of `files_app/storage.py`
and runs the agent's tests against it:

| Behavior | Planted bug |
| --- | --- |
| Download | `read_file` joins the name onto the root without the check |
| Upload | `save_file` joins the name onto the root without the check |
| Delete | `delete_file` joins the name onto the root without the check |
| Folder listing | `list_dir` joins the name onto the root without the check |
| Archive extraction | Member names are joined without the check (Zip Slip); members are written before the whole archive is checked |
| Sibling folder | The check compares strings (`startswith`), so `../files-private` passes |
| Symlinks | The path is normalized without resolving symlinks |

A run passes when the agent's tests catch every planted bug, the suite is
green, nothing under `files_app/` or in the existing tests changed, and the
suite still passes from a different path. The baseline suite catches none of
them. Atomic writes are in the prompt but not graded.

Python's unittest writes no JUnit report, so the suite command carries a small
standard-library runner (`tools/run_junit.py`). After editing it, run
`python3 eval/build_workload.py`.

The sandbox and the grader run in `python:3.13-slim`, pinned by digest in the
workload's `image`, not in darkmux's default image. Bump the digest as a new
fixture version.

Results claim only that a model's tests caught these planted bugs. They do
not claim the code, or any model, is secure.
