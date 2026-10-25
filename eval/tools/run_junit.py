"""Run the result's tests and write JUnit XML.

darkmux's grader reads JUnit, and Python's unittest does not write it, so this
standard-library runner does. `eval/build_workload.py` embeds this file into
the workload's suite command, because the grader runs that command in a copy
of the result where eval/ does not exist.
"""

import sys
import unittest
from pathlib import Path
from xml.sax.saxutils import quoteattr


class Recorder(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.cases = []

    def addSuccess(self, test):
        self.cases.append((test, None))

    def addFailure(self, test, err):
        self.cases.append((test, ("failure", self._exc_info_to_string(err, test))))

    def addError(self, test, err):
        self.cases.append((test, ("error", self._exc_info_to_string(err, test))))

    def addSkip(self, test, reason):
        self.cases.append((test, ("skipped", reason)))


def main(report):
    root = Path.cwd()
    sys.path.insert(0, str(root))
    suite = unittest.TestLoader().discover(str(root / "tests"), top_level_dir=str(root))
    result = Recorder()
    suite.run(result)

    lines = ['<?xml version="1.0" encoding="utf-8"?>', "<testsuites><testsuite>"]
    for test, outcome in result.cases:
        name = quoteattr(test.id())
        if outcome is None:
            lines.append(f"<testcase name={name}/>")
        else:
            kind, text = outcome
            lines.append(f"<testcase name={name}><{kind} message={quoteattr(text[-2000:])}/></testcase>")
    lines.append("</testsuite></testsuites>")
    Path(report).write_text("\n".join(lines) + "\n")

    failed = [t.id() for t, o in result.cases if o and o[0] != "skipped"]
    for test, outcome in result.cases:
        print(("ok   " if outcome is None else outcome[0].ljust(5)), test.id())
    print(f"{len(result.cases) - len(failed)} of {len(result.cases)} passed")
    return 1 if failed or not result.cases else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
