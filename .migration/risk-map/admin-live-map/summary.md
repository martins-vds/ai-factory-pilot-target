# Admin live map — best-effort source risk map

Source SHA: `f3beacf78de4f6d34edc4971ac87e38a5c6fe59d`.

## Results

| Input | Detected methods | Above CRAP 30 | Highest hotspot |
|---|---:|---:|---|
| Java source (six scoped/shared model files) | 37 | 2 | `Delivery.calculateNextExpectedActivity`: CRAP 156, CCN 12 |
| Embedded JavaScript in `mapFrame.xhtml` | 3 | 1 | `init()`: CRAP 110, CCN 10 |
| Combined reported methods | 40 | 3 | See reports below |

The other Java hotspot is `Delivery.calculateTransportStatus` (CRAP 56, CCN 7). The JavaScript report also includes two simple functions (CRAP 2 each).

## Limitations

- These are best-effort risk rankings, not a blocking CRAP gate. No coverage input was supplied, so the CRAP tool reports zero coverage and ranks complexity; source coverage was not measured.
- The Lizard Java parser emitted no rows for `CargoMonitoringService.java` and `RealtimeCargoTrackingService.java`, even when run on those files alone. Their method complexity is omitted from the 37-method count.
- Source tests were not run. Existing `Delivery` behavior is a shared accepted dependency, not new admin-map work.

## Reproducible artifacts

- `.migration/risk-map/admin-live-map/lizard-java.csv`
- `.migration/risk-map/admin-live-map/lizard-mapframe.csv`
- `.migration/risk-map/admin-live-map/lizard-services.csv` (empty output from the isolated REST/WebSocket parse)
- `.migration/risk-map/admin-live-map/crap-java.csv`
- `.migration/risk-map/admin-live-map/crap-mapframe.csv`
- `.migration/risk-map/admin-live-map/report-java.md`
- `.migration/risk-map/admin-live-map/report-mapframe.md`
- All runs are recorded in `.migration/evidence/runs/AM-02.md`; raw logs remain in the ignored `.migration/runs/AM-02/`.
