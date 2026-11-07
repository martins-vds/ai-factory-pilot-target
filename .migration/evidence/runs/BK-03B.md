# Run journal: BK-03B

Written by `afs-run`, one row per gate run. Raw logs are not committed; the SHA-256 identifies the exact log. Result is the gate tool's own `AFS-RESULT` line.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T03:50:10+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T03:51:21+00:00 | legacy-pathfinder-rest | 1 | 0.13 | `characterization/legacy-runtime/run-payara.sh bash -c 'set -euo pipefail
base=".migration/characterization/booking/pathfinder"
endpoint="http://localhost:8080/cargo-tracker/rest/graph-traversal/shortest-path"
capture() {
  name="$1"
  url="$2"
  curl -sS --max-time 60 -D "$base/$name.headers" -o "$base/$name.body" -w "%{http_code}\n" "$url" > "$base/$name.status"
  awk '"'"'BEGIN { IGNORECASE=1 } ` | `c931788aec22d296` |  |  |
| 2026-11-07T03:52:17+00:00 | legacy-pathfinder-rest | 0 | 44.02 | `characterization/legacy-runtime/run-payara.sh bash -c 'set -euo pipefail
base=".migration/characterization/booking/pathfinder"
endpoint="http://localhost:8080/cargo-tracker/rest/graph-traversal/shortest-path"
capture() {
  name="$1"
  url="$2"
  curl -sS --max-time 60 -D "$base/$name.headers" -o "$base/$name.body" -w "%{http_code}\n" "$url" > "$base/$name.status"
  awk '"'"'BEGIN { IGNORECASE=1 } ` | `c1274089c50ea29f` | [INFO] Downloading from central-only: https://repo.maven.apache.org/maven2/org/apache/maven/maven-error-diagnostics/2.2. |  |
