"""Verify rollout inputs and generated wiring without running application tests."""

import json
import subprocess
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
BASE = "e25ccc8ecb4c0fe979e85116940fe2b6e9ce36ed"
PIN = "47eb35f851b318a90cadbba218a01a2b54880869"


def original(path):
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{BASE}:{path}"],
        check=True, capture_output=True,
    ).stdout


for path in (".migration/profile.yaml", ".migration/source.lock"):
    assert (ROOT / path).read_bytes() == original(path), path

current = yaml.safe_load((ROOT / ".migration/capabilities.yaml").read_text())
previous = yaml.safe_load(original(".migration/capabilities.yaml"))
del current["checked_at"]
del previous["checked_at"]
assert current == previous, "capability decisions changed"
assert Counter(row["status"] for row in current["capabilities"]) == {
    "met": 14, "not-applicable": 1,
}

manifest = json.loads((ROOT / ".migration/harness/installed.json").read_text())
assert manifest["harness_commit"] == PIN
jobs = yaml.safe_load((ROOT / ".github/workflows/afs-harness-check.yml").read_text())["jobs"]
assert jobs["stack-base"]["steps"][0]["with"]["fetch-depth"] == 0
for name in ("harness", "return-contract", "gates"):
    assert jobs[name]["needs"] == "stack-base"
assert any(
    "pip install" in step.get("run", "")
    and {"pyyaml", "jsonschema"} <= set(step["run"].split())
    for step in jobs["return-contract"]["steps"]
)
print(f"Exact harness pin {PIN}; profile/source lock unchanged.")
print("Capability decisions unchanged: 14 met, 1 not applicable, no gaps or waivers.")
print("Generated ancestry prerequisite and return-job schema dependency verified.")
