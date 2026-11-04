"""Verify the reviewed pin, unchanged capability decisions and real view-factory inference."""

import ast
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
BASE = "d3453215147cdad68a9cfbd8cf187a3e9d4d6e34"
PIN = "9b805e17624c50d1e74cb008b3f1b0454c1be177"


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
assert Counter(row["status"] for row in current["capabilities"]) == {"met": 14, "not-applicable": 1}
manifest = json.loads((ROOT / ".migration/harness/installed.json").read_text())
assert manifest["harness_commit"] == PIN

sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / ".migration/harness/tools"))
import enrich_graph  # noqa: E402

mods = enrich_graph.py_index(ROOT / "src")
definitions = enrich_graph.defined(mods)
module, function = definitions["cargotracker.handling.composition.compose_handling_report_view"]
view = ast.Call(func=ast.Name(id=function.name), args=[], keywords=[])
assert enrich_graph.django_view_methods(view, module, definitions) == {"POST"}
print(f"Exact reviewed pin: {PIN}; profile/source lock byte-identical.")
print("Capability decisions unchanged: 14 met, 1 not applicable, no gaps/waivers.")
print("Installed enricher resolves the actual composition/factory/handler chain to POST only.")
print("This check is not graph generation, graph acceptance, or application/full-mutation evidence.")
