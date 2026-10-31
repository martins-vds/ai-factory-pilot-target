# Track Cargo characterization

The tier-A suite drives the running legacy JSF tracking page with a session and preserves each input
and normalized output in `golden/`. It covers the four cargos seeded by `SampleDataGenerator`,
whitespace and lowercase IDs, empty and unknown IDs, and the empty-history cargo.

Install the pinned Python test dependencies:

```bash
python -m pip install -r characterization/track-cargo/requirements.txt
```

Run Payara and pytest together so the app stays up for the suite:

```bash
JAVA_HOME=/path/to/java-8 \
LEGACY_BASE_URL=http://localhost:8080/cargo-tracker \
.migration/harness/tools/afs-run --ticket 15 --name tier-a-runtime -- \
  env JAVA_HOME=/path/to/java-8 LEGACY_BASE_URL=http://localhost:8080/cargo-tracker \
  bash characterization/legacy-runtime/run-payara.sh \
  .migration/harness/tools/afs-run --ticket 15 --name tier-a-pytest -- \
  python -m pytest -q characterization/track-cargo/test_tracking.py
```

The runtime runner accepts an optional command after deployment and executes it before shutting down
Payara. The characterization suite uses the app's sample data and does not mutate it.

The tier-B runner adds its characterization class to a writable scratch copy of the pinned source,
then executes it alongside the legacy domain tests. The read-only `.source/` checkout is unchanged:

```bash
JAVA_HOME=/path/to/java-8 .migration/harness/tools/afs-run \
  --ticket 15 --name tier-b-domain -- \
  bash characterization/track-cargo/run-tier-b.sh
```

Golden dates use `<TODAY>` and signed day offsets. The recorded prediction mismatch for MNO456 is
preserved with its observed past ETA and linked to `.migration/quirks/claimed-cargo-past-eta.md`.
