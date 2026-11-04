# Handling registration characterization

The tier-A suite posts reports to the running legacy REST endpoint, polls the
public tracking page and `GET /rest/cargo`, and compares the observations with
the committed goldens. It reuses the pinned Java 8 / Payara runner in
`characterization/legacy-runtime/`.

Record or replay tier A with:

```bash
JAVA_HOME=/path/to/java-8 \
AFS_RECORD_HANDLING_GOLDEN=1 \
.migration/harness/tools/afs-run --ticket HR-03 --name tier-a -- \
  env JAVA_HOME=/path/to/java-8 AFS_RECORD_HANDLING_GOLDEN=1 \
  bash characterization/legacy-runtime/run-payara.sh \
  .migration/harness/tools/afs-run --ticket HR-03 --name tier-a-pytest -- \
  python -m pytest -q characterization/handling-registration/test_handling_registration.py
```

Omit `AFS_RECORD_HANDLING_GOLDEN=1` to replay the baselines. The suite gives
asynchronous reports a bounded observation window. The one-second JMS TTL is
not asserted through a timing race; the tier-B test verifies the producer's
configured TTL and the queue definition instead.

The tier-B runner copies the read-only source into a temporary directory,
adds focused inspection/factory/JMS tests there, and runs them with the
source-owned domain tests:

```bash
JAVA_HOME=/path/to/java-8 .migration/harness/tools/afs-run \
  --ticket HR-03 --name tier-b -- \
  bash characterization/handling-registration/run-tier-b.sh
```

The separate [HR-04E-TIME persistence/reload experiment](timestamp-reload/report.md)
measures DATE storage, immediate cached time-of-day, and public history after an
explicit source cache clear. Its dedicated domain/database runner and separately
named observations leave the original goldens unchanged. Quirk #171 still requires
an operator ruling; this experiment changes no target behavior.
