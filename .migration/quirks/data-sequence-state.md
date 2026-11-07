# Legacy SEQUENCE metadata has no target table

## Question
The snapshot contains one SEQUENCE row with provider-style metadata columns, while the target uses PostgreSQL-native BigAutoField sequences; should the migration preserve the source counter semantics or realign target-native counters after importing explicit IDs?

## Evidence
- Source: `.source/src/main/resources/META-INF/persistence.xml:6-17`; generated identifiers include `Cargo.java:65-67` and `Leg.java:26-28`.
- Characterization: snapshot manifest count is one and the header is `SEQ_NAME, SEQ_COUNT`; no row values or source DDL were inspected.
- Why it looks wrong: the source snapshot includes this table, but it has no JPA entity/graph node and target models/migrations define no corresponding table. Sequence state may affect future generated IDs.

## Impact
- Ledger capabilities: `data.sequence`
- Blocks: follow-on data-migration mapping decision (not yet ticketed)

## Options
1. Preserve exactly if compatible with target-native sequence mechanics.
2. Reinitialize target-native counters after imported primary keys, documenting that the provider table itself is not copied.
3. Other
