# Run journal: BK-03B

Written by `afs-run`, one row per run. Raw logs are not committed; the SHA-256 prefix identifies the exact log. Command summaries are used for multiline callbacks.

| UTC | Gate | Exit | Seconds | Command | Log SHA-256 | First highlight | Result |
|---|---|---|---|---|---|---|---|
| 2026-11-07T03:50:10+00:00 | setup-probe | 0 | 0.0 | `true` | `e3b0c44298fc1c14` |  |  |
| 2026-11-07T03:51:21+00:00 | legacy-pathfinder-rest | 1 | 0.13 | `run-payara.sh (JAVA_HOME unset; stopped before startup)` | `c931788aec22d296` | JAVA_HOME must point to a Java 8 JDK |  |
| 2026-11-07T03:52:17+00:00 | legacy-pathfinder-rest | 0 | 44.02 | `run-payara.sh (Java 8; six REST response captures)` | `c1274089c50ea29f` | [INFO] Downloading from central-only: https://repo.maven.apache.org/maven2/org/apache/maven/maven-error-diagnostics/2.2. |  |
