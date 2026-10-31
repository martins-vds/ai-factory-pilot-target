# Track Cargo characterization run summary

- Source SHA: `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`
- Final tier-A command: `JAVA_HOME=/usr/lib/jvm/temurin-8-jdk-amd64 LEGACY_BASE_URL=http://localhost:8080/cargo-tracker bash characterization/legacy-runtime/run-payara.sh .migration/harness/tools/afs-run --ticket 15 --name tier-a-pytest-final -- python -m pytest -q characterization/track-cargo/test_tracking.py`
- Tier-A harness log: `.migration/runs/15/20261031T181017511302Z-tier-a-characterization-final.log`
- Tier-A suite log: `.migration/runs/15/20261031T181040428604Z-tier-a-pytest-final.log`
- Tier-A result: Payara Server 4.1.2.181 deployed the scratch-built WAR; `GET /cargo-tracker/` returned HTTP 200; pytest reported `12 passed in 0.93s`.
- Tier-B command: `JAVA_HOME=/usr/lib/jvm/temurin-8-jdk-amd64 bash characterization/track-cargo/run-tier-b.sh`
- Tier-B log: `.migration/runs/15/20261031T180806878653Z-tier-b-domain.log`
- Tier-B result: Maven reported `Tests run: 29, Failures: 0, Errors: 0, Skipped: 0` and `BUILD SUCCESS`. This consists of all 24 source domain tests and five new characterization tests.
- Initial failed attempts: `.migration/runs/15/20261031T180642867052Z-tier-b-domain.log` (read-only scratch-copy cleanup), `.migration/runs/15/20261031T180656588156Z-tier-b-domain.log` (legacy POM skipped tests), and `.migration/runs/15/20261031T180733164599Z-tier-b-domain.log` (test harness used the wrong event constructor). The runner now makes only its temporary copy writable, explicitly sets `-DskipTests=false`, and uses the source constructor overload that corresponds to event type; the final run passes.

## Outcome

- Tier-A golden cases: 8 recorded; 7 predicted/observed matches; 1 recorded finding for MNO456's past ETA.
- Tier-A tests: 12 passed.
- Tier-B tests: 29 passed.
- Source checkout: unchanged and read-only.
- New local quirk tickets: `.migration/quirks/claimed-cargo-past-eta.md` and `.migration/quirks/itinerary-test-next-expected.md`.
