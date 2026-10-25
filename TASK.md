QA REVIEW REQUEST — attachment storage

An attachment storage module was recently merged. This is a security-sensitive surface — every file name it receives comes from a user (a download link, an upload form, a delete button, a folder listing, the member names inside an uploaded zip), and a name that reaches outside the storage root reads, overwrites or deletes files the user must never touch — and it needs adequate test coverage before deployment.

What changed:

- Every operation (read_file, save_file, delete_file, list_dir, extract_archive) maps the user's name to a path under the storage root through safe_path, and raises PathRefused for any name that would land outside it
- Names with `..` segments and absolute names are refused when they resolve outside the root
- The check compares whole path components, so a sibling folder whose name merely starts with the root's name (`files-private` next to `files`) is outside the root
- Symlinks are resolved before the check: a link inside the root that points outside it is refused
- extract_archive checks every member name before writing anything: one member that would land outside the root refuses the whole archive, and nothing from it is written
- save_file writes atomically and creates missing folders under the root

The implementation lives at:

- ${SANDBOX_DIR}/files_app/storage.py

Existing tests:

- ${SANDBOX_DIR}/tests/test_storage.py
- ${SANDBOX_DIR}/tests/test_portability.py (a guard on the suite itself; leave it alone)

Some coverage is already in place. Some isn't. Your job is to figure out the difference, decide what matters, and write the tests yourself.

## Your task

Read the implementation. Read the existing tests. Decide which behaviors of the change aren't covered and would matter to you in a real code review. Then write those tests — don't hand them back as a list of suggestions.

Treat this as a real PR review where you have commit access: if you'd want a test to exist before approving, write it.

## Constraints

- Repo root: ${SANDBOX_DIR}.
- Your tests must run in a DIFFERENT environment than this one, where that
  path does not exist. Build every path at run time, from `Path(__file__)` or
  a temporary directory your test creates; never write an absolute path as a
  string literal. `tests/test_portability.py` enforces this and will tell you
  immediately.
- Do not modify existing tests — only add new ones.
- Do not modify source code under files_app/. Tests only.
- Match the existing test file style: standard-library `unittest` with `unittest.TestCase` classes. There are no third-party packages and no install step.
- Iterate by running the suite:
  cd ${SANDBOX_DIR} && python3 -m unittest discover -s tests -t .
- Final verification is the same command:
  cd ${SANDBOX_DIR} && python3 -m unittest discover -s tests -t .

## When you're done

You're done when the tests you've added are sufficient for you to approve this PR. Quality over quantity. Stop when adding more tests would be padding rather than risk reduction.

Most reviewers would land somewhere between 5 and 15 new test cases for a change of this surface area. If you're well outside that range in either direction, mention it in your reply.

## Reply format

Keep it tight:

- Gaps you identified: behaviors that needed coverage, one-line rationale per gap
- What you wrote: number of new tests, which files
- What you decided NOT to test, and why: the negative space matters
- Test result: the `Ran N tests` line from your final run
- Confidence: would you sign off on this PR after your additions?
