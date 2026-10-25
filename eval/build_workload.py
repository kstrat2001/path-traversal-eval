"""Regenerate the suite command in workloads/path-traversal.json from tools/run_junit.py.

The grader runs the suite command inside a copy of the result, where this
folder does not exist, so the runner travels inside the command itself.
Edit tools/run_junit.py, then run: python3 eval/build_workload.py
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
script = (HERE / "tools" / "run_junit.py").read_text()
assert "DARKMUX_GRADE" not in script
command = "python3 - ${REPORT} <<'DARKMUX_GRADE'\n" + script + "DARKMUX_GRADE\n"

path = HERE / "workloads" / "path-traversal.json"
doc = json.loads(path.read_text())
doc["workload"]["verify"]["grade"]["suite"]["command"] = command
path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
print(f"updated {path.name}: suite command is {len(command)} bytes")
