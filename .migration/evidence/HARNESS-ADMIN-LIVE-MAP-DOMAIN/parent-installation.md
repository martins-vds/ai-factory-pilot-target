# Parent normal-bootstrap assistance

Actor: parent coordinator, not the original Bootstrapper. This assistance follows
the original worker's explicit committed ownership handoff at
`16369df8798b7352cdb9034c9a8562fbb75a778d`, after its authoritative
2026-11-06T16:22:37Z finish. The same worker must independently verify and finalize.

The worker's single ordinary archive acquisition succeeded and independently
verified approved source tree `db4d5e74d056c69f401564d31d1fb812d4fd440c`;
the archive lacked the Git commit metadata required by the unchanged installer.
The worker correctly did not install from a zero/dirty fallback identity. Its
original return, handoff, journal and cost record remain byte-for-byte unchanged.

The parent used a fresh complete clean checkout of
`martins-vds/ai-factory-swarm@9fcf4deb0565229bc4c3078e9da0c9bfece045c7`,
independently verified tree `db4d5e74d056c69f401564d31d1fb812d4fd440c`,
and ran that release's unchanged normal `tools/bootstrap.py` against this
original proposal branch. The existing target profile/capabilities and approved
`stacks/java-to-django.json` were used. The command exited 0 at
2026-11-06T16:28:30Z after 108.13 seconds, reporting 10 agents and 61 skills.

Existing authorized parent access was used. No credentials were transferred,
private dependencies skipped, offline mode used, installed file hotpatched,
manifest fabricated, graph generated or merged, application edited, model
overridden, or acceptance rerun. This parent execution is not worker installation.

## Parent checks

Commands ran through `afs-run` with the distinct parent ticket
`HARNESS-ADMIN-LIVE-MAP-DOMAIN-PARENT`. The committed journal is
`.migration/evidence/runs/HARNESS-ADMIN-LIVE-MAP-DOMAIN-PARENT.md`.

| Parent check | Actual result | Full raw-log SHA256 |
|---|---|---|
| Normal bootstrap | Exit0; exact9FC, 10 agents / 61 skills | `fa2fbd6a1221ee12727caca40bcd038dd0086df3b77a37d268993bb23f4f31c0` |
| Installed integrity | Exit0; 77 entries / 389 files / 0 problems | `b3204e753b040c284f6c39c2f34b90adaa1a9a332fcf58832b82cb4d7e4d070e` |
| Migration validation | Exit0; 103 files / 0 errors | `446108b8fc1c3e05411d20bae90cc78a66542dc0f0b7b5a9d7493c070f7356d0` |
| Preservation and parity | Exit0; 813 other baseline blobs/modes, all45 historical returns and all4 original worker outputs unchanged; 65 direct approved-source file comparisons and all7 workflow comparisons | `5161bb25ff7bc4abc14d450d49df29d79d34a271ac00d8d4b062ca66588c9ab6` |
| New checker entry point | Exit0; real installed `--help` emits repository-standard `AFS-TOOL check_domain_coverage.py exit=0` | `e1e5d211b67fc6e7f6ba25a34049bfca1d1db355727e035ddf3ef8cbe247369f` |

Of823 baseline paths, exactly10 changed normally: seven generated workflows,
capability `checked_at`, the installed manifest and the approved `understand.py`.
The new approved `check_domain_coverage.py` is one additional generated tool.
Six workflow bodies remain unchanged except their release header; the understand
workflow exactly matches the approved normal generator, including optional entry
points, explicit deferral and fatal coverage checking after enrichment. All seven
workflows were compared with the approved normal generator. The manifest changes
only release/time and the approved runner/checker file hashes. Capability
decisions, providers and statuses are unchanged. No staging directory or lock
remains.

Raw logs remain untracked under `.migration/runs/`. The parent preservation script
and complete35F baseline inventory remain in the orchestration session artifacts;
their execution is not attributed to the worker. Parent Python checks are not a
new configured-runtime/service verification, all-source test run, or role finish.

This installs9FC on proposal211 only, not pilot main. The blocked return is
deliberately preserved for the same original worker to supersede truthfully.
Independent worker verification, exact final-head CI, parent review, actual
authorized merge/main installation and postmerge gates remain required before
one normal focused source-graph generation. This installation alone proves no
new domain semantics, source characterization, slice acceptance or plan approval.
