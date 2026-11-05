# HR-04F-CLOSURE — approved historical-attribution guard rollout

- Issue: [martins-vds/ai-factory-pilot-target#187](https://github.com/martins-vds/ai-factory-pilot-target/issues/187)
- Rollout/setup PR: [#188](https://github.com/martins-vds/ai-factory-pilot-target/pull/188) (not merged)
- Approved harness commit: `2c8e00ab87e99f3d77976e3cf78c2a89011627fb`
- Pilot baseline: `f589d826100b34722eb29628ec93deb7ad450bb8`
- Normal-bootstrap commit: `2db4f098f1764740d21b9ed76a7210282c88af5c`
- Outcome: **normal installation and independent verification passed, with a disclosed shell GitHub-API limitation.**

## Execution and independent verification

The coordinator executed normal `tools/bootstrap.py` using a clean checkout at the approved harness pin, the existing profile and capabilities, and the Java-to-Django stack pack. The coordinator's `coordinator-normal-bootstrap` journal row records exit 0 in 30.48 seconds. This session did not execute bootstrap. The installed manifest now names the approved pin.

This session independently verified:

| Check | Result |
|---|---|
| Source/tool/template parity | Pass — public pinned GitHub blobs for `tools/check_slice_returns.py` (`f40ff403…`) and `skills/afs-migration-contract/SKILL.md` (`f2e3d46a…`) match the installed files. The exact pinned `afs-map-fog.yml` template blob (`0bd651f9…`) renders byte-for-byte to the installed workflow. |
| Installed integrity | Pass — harness `0.2.0`, 77 entries / 388 files, zero problems. |
| Migration state and runtime | Pass — 90 files, zero validation errors; Python 3.13.17 matches the profile; configured `db` service is healthy. |
| Generated workflow | Pass — full history (`fetch-depth: 0`) and both `pyyaml` and `jsonschema` are present in the exact rendered workflow. |
| Protected inputs and history | Pass — only approved generated outputs and this ticket's own report/journal/handoff/return plus the coordinator's bootstrap cost differ from baseline. Application, tests, templates, profile, source lock, slices, graphs, ledger, accepted artifact archive, survivor report, and all other-role artifacts are unchanged. Capabilities differ only in the standard `checked_at` refresh. Current `.migration/returns/HR-04E.afs-verifier.yaml` (issue #176 / PR #177) is byte-identical to baseline. |
| Graph checks | Pass — source and target freshness; source flow 0 failures (27 entry points, 18 reaching data); target flow 0 failures (7 entry points, 3 reaching data, 5 owned / 0 unowned). |
| Epic113 attribution | Pass with a transport limitation — the coordinator's actual installed-guard run records `gate=slice-returns epic=113 verdict=pass tickets=9 failures=0`. Independently, this session obtained the live nine-ticket issue snapshot through GitHub MCP and ran the installed guard's history/attribution logic against it after fetching complete local ancestry; it attributed issue #131 to `.migration/returns/HR-04E.afs-verifier.yaml@1c8716c7afe972c60b750b36aca91ffa80597a79`, with zero local logic failures. The full CLI invocation in this worker could not access GitHub because `GH_TOKEN` is unavailable; direct unauthenticated public API access returned HTTP 403. These failed attempts remain in the journal. No credentials were transferred. |

Fresh independent checks were run through `afs-run`; see `.migration/evidence/runs/HR-04F-CLOSURE.md`. The local attribution-logic check is not represented as a synthesized `AFS-RESULT`; the journal preserves the coordinator's actual end-to-end guard result separately.

## Boundaries

No application change, graph rebuild, full-mutation rerun, Auditor rewrite, or acceptance verdict occurred. The accepted evidence remains tied to its original exact measured revision; it was not remeasured on this harness pin. The user's explicit approval to merge the reviewed rollout and for the coordinator's later epic action is recorded but unconsumed. This session did not merge PR #188 or mutate epic113. Research #173 remains excluded.

## Next step

Coordinator: review the exact final PR head and current CI, then perform only the separately authorized merge and subsequent epic work. The direct shell guard invocation's missing GitHub token is documented above; the coordinator's actual guard execution and this session's independent attribution verification are both recorded without conflating actors.
