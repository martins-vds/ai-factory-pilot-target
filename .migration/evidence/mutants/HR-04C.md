# Surviving mutants: HR-04C

Written by `afs-mutation` on its last run (base `origin/main`): score 0.855, threshold 0.8, killed 71, survived 12. Each line is a mutant no test killed: add a test that fails on it, or simplify the code if it is equivalent.

- `src/cargotracker/handling/interfaces/rest.py:25 Mutant #4` — Equivalent: the REST error response serializes the validation message, not its code.
- `src/cargotracker/handling/interfaces/rest.py:41 Mutant #30` — Equivalent: the REST error response serializes the validation message, not its code.
- `src/cargotracker/handling/interfaces/rest.py:43 Mutant #35` — Equivalent: the REST error response serializes the validation message, not its code.
- `src/cargotracker/handling/interfaces/rest.py:54 Mutant #40` — Equivalent: the REST error response serializes the validation message, not its code.
- `src/cargotracker/handling/interfaces/rest.py:61 Mutant #44` — Equivalent: the REST error response serializes the validation message, not its code.
- `src/cargotracker/handling/interfaces/rest.py:68 Mutant #53` — No test added: source characterization asserts HTTP 400 for a short voyage number, but does not define the target-generated error text.
- `src/cargotracker/handling/interfaces/rest.py:68 Mutant #54` — Equivalent: the REST error response serializes the validation message, not its code.
- `src/cargotracker/handling/interfaces/rest.py:82 Mutant #58` — Existing `test_non_post_request_is_not_accepted` asserts HTTP 405; the full focused suite kills this mutant.
- `src/cargotracker/urls.py:24 Mutant #1` — Existing URL tests kill it in the full-suite mutation diagnostic; no duplicate route test was added.
- `src/cargotracker/urls.py:24 Mutant #2` — Existing URL tests kill it in the full-suite mutation diagnostic; no duplicate route test was added.
- `src/cargotracker/urls.py:25 Mutant #4` — Existing handling URL tests kill it in the full-suite mutation diagnostic; no duplicate route test was added.
- `src/cargotracker/urls.py:26 Mutant #5` — Existing map route tests kill it in the full-suite mutation diagnostic; no duplicate route test was added.
