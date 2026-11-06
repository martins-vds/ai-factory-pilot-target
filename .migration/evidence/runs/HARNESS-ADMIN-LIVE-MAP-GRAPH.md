# Run journal: HARNESS-ADMIN-LIVE-MAP-GRAPH

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-06T14:48:50+00:00 | setup-validation | 0 | 0.66 | `python .migration/harness/tools/validate.py .migration` | `1f4ff7e5cda8e1f6` |  |  |
| 2026-11-06T14:48:50+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T14:48:50+00:00 | setup-services | 0 | 0.12 | `python .migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-06T14:48:50+00:00 | setup-runtime | 0 | 0.05 | `python .migration/harness/tools/check_runtime.py` | `d07c895212ff2443` |  |  |
| 2026-11-06T14:48:56+00:00 | approved-source-acquisition | 22 | 0.03 | `curl --fail --location --show-error --silent --connect-timeout 15 --max-time 60 --output /tmp/afs-harness-bdf1f43b613f5ed6c7719380cede7c02bca1c778.tar.gz https://api.github.com/repos/martins-vds/ai-factory-swarm/tarball/bdf1f43b613f5ed6c7719380cede7c02bca1c778` | `e85a8cbf6458f846` | curl: (22) The requested URL returned error: 403 |  |
| 2026-11-06T14:49:18+00:00 | installed-integrity | 0 | 0.05 | `python .migration/harness/tools/check_installed.py` | `ded3aadcd399f8e6` |  |  |
| 2026-11-06T14:49:18+00:00 | baseline-preservation | 1 | 0.06 | `bash -c 'git diff --exit-code d77b7bec98d26e7ee291488091d009e89f595117 HEAD && git diff --exit-code && python -c "import collections,json,pathlib,subprocess,yaml; b=\"d77b7bec98d26e7ee291488d009e89f595117\"; paths=subprocess.check_output([\"git\",\"ls-tree\",\"-r\",\"--name-only\",\"HEAD\"],text=True).splitlines(); returns=[p for p in paths if p.startswith(\".migration/returns/\") and p.endswith(\` | `3ed6fbf3a3ca0797` | Traceback (most recent call last): |  |
| 2026-11-06T14:49:33+00:00 | baseline-preservation-corrected | 0 | 0.04 | `bash -c 'git diff --exit-code d77b7bec98d26e7ee291488091d009e89f595117 HEAD && git diff --exit-code && python -c "import collections,json,pathlib,subprocess,yaml; paths=subprocess.check_output([\"git\",\"ls-tree\",\"-r\",\"--name-only\",\"HEAD\"],text=True).splitlines(); returns=[p for p in paths if p.startswith(\".migration/returns/\") and p.endswith(\".yaml\")]; c=collections.Counter(x[\"status\` | `da66f22555192f97` |  |  |
| 2026-11-06T14:50:07+00:00 | setup-ticket-inputs | 1 | 0.02 | `python .migration/harness/tools/check_inputs.py` | `a6ba7e9296076d23` |  |  |
| 2026-11-06T14:50:07+00:00 | application-source-input | 0 | 0.0 | `test -f /home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.source/src/main/webapp/admin/tracking/map.xhtml` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T14:50:57+00:00 | final-validation | 0 | 0.53 | `python .migration/harness/tools/validate.py .migration` | `cefb166b037d28b2` |  |  |
| 2026-11-06T14:50:58+00:00 | final-integrity | 0 | 0.04 | `python .migration/harness/tools/check_installed.py` | `ded3aadcd399f8e6` |  |  |
| 2026-11-06T14:51:36+00:00 | committed-validation | 0 | 0.55 | `python .migration/harness/tools/validate.py .migration` | `cefb166b037d28b2` |  |  |
| 2026-11-06T14:51:36+00:00 | committed-return-contract | 0 | 0.09 | `python .migration/harness/tools/check_return_contract.py --base origin/main` | `156481c2d16ac806` |  |  |
| 2026-11-06T14:51:36+00:00 | committed-baseline-preservation | 0 | 0.02 | `python -c 'import subprocess; b="d77b7bec98d26e7ee291488091d009e89f595117"; allowed={".migration/costs/2ca3da76-76ec-45d5-81d9-9cddd10ed608.json",".migration/evidence/runs/HARNESS-ADMIN-LIVE-MAP-GRAPH.md",".migration/handoffs/HARNESS-ADMIN-LIVE-MAP-GRAPH.md",".migration/returns/HARNESS-ADMIN-LIVE-MAP-GRAPH.afs-bootstrapper.yaml"}; rows=subprocess.check_output(["git","diff","--name-status",b,"HEAD"` | `a084fba46cfa382c` |  |  |
| 2026-11-06T14:51:55+00:00 | owning-proposal-attribution | 0 | 0.03 | `python -c 'import pathlib,yaml; p=pathlib.Path(".migration/returns/HARNESS-ADMIN-LIVE-MAP-GRAPH.afs-bootstrapper.yaml"); r=yaml.safe_load(p.read_text()); assert r["issue"]=="martins-vds/ai-factory-pilot-target#208"; assert r["pr"]==r["setup_pr"]=="https://github.com/martins-vds/ai-factory-pilot-target/pull/209"; assert r["role"]=="afs-bootstrapper"; assert r["installation"]["bootstrap_executed"] i` | `fe6f74cabe66c36d` |  |  |
| 2026-11-06T14:52:06+00:00 | final-output-validation | 0 | 0.56 | `python .migration/harness/tools/validate.py .migration` | `cefb166b037d28b2` |  |  |
| 2026-11-06T15:03:00+00:00 | resumed-setup-validation | 0 | 0.98 | `python .migration/harness/tools/validate.py .migration` | `cefb166b037d28b2` |  |  |
| 2026-11-06T15:03:00+00:00 | resumed-setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-06T15:03:00+00:00 | resumed-setup-services | 0 | 0.19 | `python .migration/harness/tools/afs-services check` | `274667623a156426` |  |  |
| 2026-11-06T15:03:00+00:00 | resumed-setup-runtime | 0 | 0.07 | `python .migration/harness/tools/check_runtime.py` | `d07c895212ff2443` |  |  |
| 2026-11-06T15:03:00+00:00 | resumed-installed-integrity | 0 | 0.08 | `python .migration/harness/tools/check_installed.py` | `3cc4ff5ba9f911a0` |  |  |
| 2026-11-06T15:03:51+00:00 | independent-protected-baseline | 0 | 0.13 | `python -c 'import collections,json,pathlib,subprocess,yaml
base="d77b7bec98d26e7ee291488091d009e89f595117"
parent="04bff46c768d601a9cbcb3ed00b4722138bb1b81"
previous="2a59436856ef5004a9de32bdf51c3cf408314904"
def git(*args): return subprocess.check_output(["git",*args])
def tree(ref):
 return {p:(meta.split()[0],meta.split()[2]) for line in git("ls-tree","-r",ref).decode().splitlines() for meta,p ` | `a3af0cca01090881` |  |  |
| 2026-11-06T15:04:22+00:00 | approved-fixtureless-tests | 0 | 0.36 | `env PYTHONPATH=/home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools python -c 'import pathlib,runpy,unittest; m=runpy.run_path("/tmp/afs-bdf-verification/test_enrich_graph.py"); import enrich_graph; assert pathlib.Path(enrich_graph.__file__).resolve()==pathlib.Path("/home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools/enri` | `1ad0fba38245fac7` |  |  |
| 2026-11-06T15:04:46+00:00 | approved-tool-identity | 0 | 0.04 | `python -c 'import hashlib,pathlib,subprocess; p=pathlib.Path(".migration/harness/tools/enrich_graph.py"); approved=pathlib.Path("/tmp/1793977381118-copilot-tool-output-6270ff.txt").read_bytes().split(b")",1)[1]; assert p.read_bytes()==approved; blob=subprocess.check_output(["git","hash-object",str(p)],text=True).strip(); assert blob=="44b8ff9f2eb88abefdfe4fd01573000275f7bc28"; sha=hashlib.sha256(a` | `5983bdeaf10913b9` |  |  |
| 2026-11-06T15:04:46+00:00 | real-wrapper-resolver-controls | 0 | 0.05 | `env PYTHONPATH=/home/runner/work/ai-factory-pilot-target/ai-factory-pilot-target/.migration/harness/tools python -c 'import pathlib; import enrich_graph as e
root=pathlib.Path(".source").resolve()
page=root/"src/main/webapp/admin/tracking/map.xhtml"
frame=page.with_name("mapFrame.xhtml")
assert page.is_file() and frame.is_file()
pages={frame.resolve():frame}
f=e.IframeLinks(page.read_text())
asser` | `02ad06895ea86626` |  |  |
| 2026-11-06T15:04:46+00:00 | resumed-normalized-inputs | 0 | 0.03 | `python .migration/harness/tools/check_inputs.py --text 'Continuation execution inputs: '.migration/harness/tools/enrich_graph.py' '.migration/harness/tools/check_installed.py' '.migration/harness/tools/validate.py' '.source/src/main/webapp/admin/tracking/map.xhtml' '.source/src/main/webapp/admin/tracking/mapFrame.xhtml' '.migration/profile.yaml' '.migration/capabilities.yaml' '.migration/source.lo` | `5853179d476f213e` |  |  |
| 2026-11-06T15:06:32+00:00 | installed-counts-and-own-attribution | 0 | 0.05 | `python -c 'import collections,json,pathlib,yaml; m=json.loads(pathlib.Path(".migration/harness/installed.json").read_text()); counts=collections.Counter(e["kind"] for e in m["entries"]); print("installed_entry_counts:",dict(counts)); assert counts["agent"]==10 and counts["skill"]==61; r=yaml.safe_load(pathlib.Path(".migration/returns/HARNESS-ADMIN-LIVE-MAP-GRAPH.afs-bootstrapper.yaml").read_text()` | `182333274bbfec33` |  |  |
| 2026-11-06T15:06:33+00:00 | continuation-final-validation | 0 | 0.93 | `python .migration/harness/tools/validate.py .migration` | `cefb166b037d28b2` |  |  |
| 2026-11-06T15:07:11+00:00 | final-continuation-preservation | 0 | 0.06 | `python -c 'import pathlib,subprocess; parent="04bff46c768d601a9cbcb3ed00b4722138bb1b81"; allowed={".migration/returns/HARNESS-ADMIN-LIVE-MAP-GRAPH.afs-bootstrapper.yaml",".migration/handoffs/HARNESS-ADMIN-LIVE-MAP-GRAPH.md",".migration/evidence/runs/HARNESS-ADMIN-LIVE-MAP-GRAPH.md",".migration/costs/2ca3da76-76ec-45d5-81d9-9cddd10ed608.json"}; git=lambda *a: subprocess.check_output(["git",*a]); ch` | `bda704457086a7ec` |  |  |
| 2026-11-06T15:07:12+00:00 | final-return-validation | 0 | 0.93 | `python .migration/harness/tools/validate.py .migration` | `cefb166b037d28b2` |  |  |
| 2026-11-06T15:07:13+00:00 | final-bdf-integrity | 0 | 0.08 | `python .migration/harness/tools/check_installed.py` | `3cc4ff5ba9f911a0` |  |  |
