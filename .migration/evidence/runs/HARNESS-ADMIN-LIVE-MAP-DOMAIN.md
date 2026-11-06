# Run journal: HARNESS-ADMIN-LIVE-MAP-DOMAIN

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-06T16:17:42+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T16:20:16+00:00 | source-tree-and-current-state | 0 | 0.06 | `python -c 'import json,pathlib,subprocess,yaml; root=pathlib.Path("/tmp/afs-admin-map-source/tree"); tree=subprocess.check_output(["git","-C",str(root),"write-tree"],text=True).strip(); cap=yaml.safe_load(pathlib.Path(".migration/capabilities.yaml").read_text()); counts={k:sum(c["status"]==k for c in cap["capabilities"]) for k in ("met","gap","waived","not-applicable")}; installed=json.loads(pathl` | `c0ff0ee408693623` |  |  |
| 2026-11-06T16:20:20+00:00 | source-head-metadata | 128 | 0.0 | `git -C /tmp/afs-admin-map-source/tree rev-parse HEAD` | `e000a2af1ee89f0a` | fatal: ambiguous argument 'HEAD': unknown revision or path not in the working tree. |  |
| 2026-11-06T16:20:54+00:00 | migration-state-validation | 0 | 0.96 | `python .migration/harness/tools/validate.py .migration` | `446108b8fc1c3e05` |  |  |
| 2026-11-06T16:21:16+00:00 | final-migration-state-validation | 0 | 0.95 | `python .migration/harness/tools/validate.py .migration` | `446108b8fc1c3e05` |  |  |
| 2026-11-06T16:32:55+00:00 | resume-setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T16:34:14+00:00 | own-return-schema-validation | 0 | 0.25 | `python -c 'import json,pathlib,yaml,jsonschema; p=pathlib.Path(".migration/returns/HARNESS-ADMIN-LIVE-MAP-DOMAIN.afs-bootstrapper.yaml"); schema=json.loads(pathlib.Path(".migration/harness/schemas/return.schema.json").read_text()); jsonschema.validate(yaml.safe_load(p.read_text()),schema); print("ticket return schema valid")'` | `12b947452c7fd7e4` |  |  |
| 2026-11-06T16:34:36+00:00 | final-own-return-schema-validation | 0 | 0.25 | `python -c 'import json,pathlib,yaml,jsonschema; p=pathlib.Path(".migration/returns/HARNESS-ADMIN-LIVE-MAP-DOMAIN.afs-bootstrapper.yaml"); jsonschema.validate(yaml.safe_load(p.read_text()),json.loads(pathlib.Path(".migration/harness/schemas/return.schema.json").read_text())); print("ticket return schema valid")'` | `12b947452c7fd7e4` |  |  |
| 2026-11-06T17:10:45+00:00 | resumed-migration-state-validation | 0 | 0.85 | `python .migration/harness/tools/validate.py .migration` | `446108b8fc1c3e05` |  |  |
| 2026-11-06T17:10:45+00:00 | resumed-setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T17:11:34+00:00 | installed-integrity | 0 | 0.07 | `python .migration/harness/tools/check_installed.py` | `b3204e753b040c28` |  |  |
| 2026-11-06T17:11:48+00:00 | installation-identity-preservation | 1 | 0.07 | `bash -c 'python - <<'"'"'PY'"'"'
import hashlib,json,pathlib,subprocess,yaml
base="16369df8798b7352cdb9034c9a8562fbb75a778d"
install="9b21510ded472fa77121ca6d8760779ec29ca4c4"
def tree(ref):
 raw=subprocess.check_output(["git","ls-tree","-r","-z","--full-tree",ref]); out={}
 for rec in raw.split(b"\0"):
  if rec:
   meta,path=rec.split(b"\t",1); mode,kind,oid=meta.decode().split(); out[path.decode` | `bb770ecae3a6f77a` | Traceback (most recent call last): |  |
| 2026-11-06T17:12:17+00:00 | baseline-and-artifact-preservation | 1 | 0.07 | `bash -c 'python - <<'"'"'PY'"'"'
import hashlib,json,pathlib,subprocess,yaml
base="35f014a9f63619844810000024dc4c51362fb040"; initial="16369df8798b7352cdb9034c9a8562fbb75a778d"; install="9b21510ded472fa77121ca6d8760779ec29ca4c4"; head="HEAD"
def tree(ref):
 raw=subprocess.check_output(["git","ls-tree","-r","-z","--full-tree",ref]); out={}
 for rec in raw.split(b"\0"):
  if rec:
   meta,path=rec.sp` | `2fd68528a4756a18` | Traceback (most recent call last): |  |
| 2026-11-06T17:12:29+00:00 | baseline-and-artifact-preservation | 1 | 0.08 | `bash -c 'python - <<'"'"'PY'"'"'
import hashlib,json,pathlib,subprocess,yaml
base="35f014a9f63619844810000024dc4c51362fb040"; initial="16369df8798b7352cdb9034c9a8562fbb75a778d"; install="9b21510ded472fa77121ca6d8760779ec29ca4c4"; head="HEAD"
def tree(ref):
 raw=subprocess.check_output(["git","ls-tree","-r","-z","--full-tree",ref]); out={}
 for rec in raw.split(b"\0"):
  if rec:
   meta,path=rec.sp` | `bcf3c563a03150f4` | Traceback (most recent call last): |  |
| 2026-11-06T17:13:19+00:00 | baseline-and-artifact-preservation | 0 | 0.08 | `bash -c 'python - <<'"'"'PY'"'"'
import json,pathlib,subprocess,yaml
base="35f014a9f63619844810000024dc4c51362fb040"; initial="16369df8798b7352cdb9034c9a8562fbb75a778d"; install="9b21510ded472fa77121ca6d8760779ec29ca4c4"; head="HEAD"
def tree(ref):
 raw=subprocess.check_output(["git","ls-tree","-r","-z","--full-tree",ref]); out={}
 for rec in raw.split(b"\0"):
  if rec:
   meta,path=rec.split(b"\t` | `25eec14ee956cea1` |  |  |
| 2026-11-06T17:13:41+00:00 | bounded-runner-checker-workflow-controls | 1 | 0.81 | `bash -c 'python - <<'"'"'PY'"'"'
import asyncio, importlib, os, pathlib, sys, tempfile
sys.path.insert(0,str(pathlib.Path(".migration/harness/tools").resolve()))
checker=importlib.import_module("check_domain_coverage")
root=pathlib.Path(".source").resolve(); entry="src/main/webapp/admin/tracking/map.xhtml"
assert (root/entry).is_file(); assert checker.validate_entry_points(root,[entry,entry])==[en` | `70505205e307a57e` | Traceback (most recent call last): |  |
| 2026-11-06T17:13:54+00:00 | bounded-runner-checker-workflow-controls | 0 | 0.09 | `bash -c 'python - <<'"'"'PY'"'"'
import asyncio, importlib, os, pathlib, sys
sys.path.insert(0,str(pathlib.Path(".migration/harness/tools").resolve()))
checker=importlib.import_module("check_domain_coverage")
root=pathlib.Path(".source").resolve(); entry="src/main/webapp/admin/tracking/map.xhtml"
assert (root/entry).is_file(); assert checker.validate_entry_points(root,[entry,entry])==[entry]
for i` | `4e6aeb8f1a7dbe92` | workflow controls: optional blank model/entry inputs; fatal coverage checker follows enrichment |  |
| 2026-11-06T17:14:01+00:00 | installed-tool-tracing | 0 | 0.16 | `bash -c 'set -e; python .migration/harness/tools/check_domain_coverage.py --help >/dev/null; python .migration/harness/tools/understand.py --help >/dev/null; python .migration/harness/tools/check_domain_coverage.py --root .source --knowledge /tmp/afs-no-knowledge.json --domain /tmp/afs-no-domain.json'` | `0f40d659d4fd5bd0` |  |  |
| 2026-11-06T17:14:35+00:00 | workflow-wiring-safety | 1 | 0.05 | `python -c 'import pathlib,subprocess
names=("afs-acceptance.yml","afs-costs.yml","afs-harness-check.yml","afs-map-fog.yml","afs-ticket-guard.yml","copilot-setup-steps.yml")
for name in names:
 p=f".github/workflows/{name}"; old=subprocess.check_output(["git","show",f"35f014a9f63619844810000024dc4c51362fb040:{p}"],text=True).splitlines(); new=pathlib.Path(p).read_text().splitlines(); assert new[0].` | `e72739de9383a730` | Traceback (most recent call last): |  |
| 2026-11-06T17:14:49+00:00 | workflow-wiring-safety | 0 | 0.04 | `python -c 'import pathlib,subprocess
names=("afs-acceptance.yml","afs-costs.yml","afs-harness-check.yml","afs-map-fog.yml","afs-ticket-guard.yml","copilot-setup-steps.yml")
for name in names:
 p=f".github/workflows/{name}"; old=subprocess.check_output(["git","show",f"35f014a9f63619844810000024dc4c51362fb040:{p}"],text=True).splitlines(); new=pathlib.Path(p).read_text().splitlines(); assert "9fcf4d` | `b85bd595b91179c9` | understand workflow: optional blank inputs, default model, post-enrichment conditional checker, fatal failure propagatio |  |
