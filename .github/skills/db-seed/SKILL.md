---
name: db-seed
description: "Generate database seed scripts that populate Microsoft SQL Server (T-SQL) and Oracle (PL/SQL and SQL*Plus) databases with realistic, domain-appropriate sample data — output as a runnable .sql script or an optional Python faker-based seeder. Reads CREATE TABLE DDL or migration files already in the repository (including Flyway and Liquibase), respects foreign-key insert ordering, and produces idempotent, re-runnable seed scripts. USE FOR: seeding or populating a dev, demo, or test SQL Server or Oracle database; generating sample, demo, or test data, or INSERT scripts, for SQL Server or Oracle tables; building a faker-based Python seeder for those engines. Trigger this skill whenever the request fits, even if the user does not say 'db-seed' — e.g. 'seed the database', 'sample/demo/test data', 'populate the tables', 'mssql/sql server/oracle seed script'. DO NOT USE FOR: PostgreSQL or MySQL seeding; Django or ORM test data, factory_boy, or pytest fixtures; JUnit test-data builders; authoring schema or CREATE TABLE DDL; Oracle-to-PostgreSQL migration or migration review; SQL query performance tuning; one-off application INSERT statements; or generating standalone CSV/data files."
---

# Database Seed Generator

Generate seed scripts that populate **Microsoft SQL Server** and **Oracle** databases with
realistic, domain-appropriate sample data. Read the schema from DDL or migration files in the
repository and produce ready-to-run seed files — as T-SQL, Oracle SQL, Python (faker), or a
combination.

This skill generates scripts only. It does not connect to or execute against a live database;
the user runs the produced script themselves. Keep that boundary in mind — the output has to be
self-contained and runnable as-is.

## Workflow

```
Progress:
- [ ] Step 1: Find and read the schema
- [ ] Step 2: Determine seed parameters
- [ ] Step 3: Plan insert order from foreign keys
- [ ] Step 4: Generate realistic data
- [ ] Step 5: Produce the seed script (engine-specific)
- [ ] Step 6: Make it idempotent
```

### 1. Find and read the schema

The schema lives in DDL or migration files in the repo, not in a live connection. Scan for it:

| Source | Location pattern |
|--------|------------------|
| SQL Server DDL | `*.sql` containing `CREATE TABLE [schema].[Table]`, often under `db/`, `sql/`, `database/`, `scripts/` |
| Oracle DDL | `*.sql` containing `CREATE TABLE`, `CREATE SEQUENCE`, often under `ddl/`, `schema/` |
| Flyway | `**/db/migration/V*__*.sql` |
| Liquibase | `**/db/changelog/**/*.{xml,yaml,json,sql}` |
| Generic migrations | `migrations/*.sql`, `migration/*.sql` |

Read every relevant file and build a model of:

- Tables, columns, and data types
- Constraints: `NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK`, primary keys
- Foreign-key relationships (which table references which)
- Auto-generated keys: SQL Server `IDENTITY`, Oracle sequences or `GENERATED ... AS IDENTITY`
- Columns needing special handling: `BIT`/`NUMBER(1)` booleans, `DATETIME2`/`DATE`/`TIMESTAMP`,
  `uniqueidentifier`/`RAW(16)` GUIDs, `NVARCHAR`/`CLOB` text, JSON columns

If the schema is ambiguous — for example a foreign key is implied by a naming convention rather
than a declared `FOREIGN KEY` constraint — state your interpretation and confirm it with the user
before generating, so the insert order is correct.

### 2. Determine seed parameters

Ask the user, inferring sensible defaults from the schema and repo when they don't say:

| Parameter | Options | Default |
|-----------|---------|---------|
| Engine | SQL Server, Oracle, or both | Infer from the DDL dialect |
| Purpose | dev, demo, testing | dev |
| Volume | small (5–10 rows/table), medium (20–50), large (100+) | small |
| Domain context | "e-commerce store", "SaaS app", "blog", etc. | Infer from table/column names |
| Output format | T-SQL, Oracle SQL, Python (faker), or a combination | Match the engine |

**Purpose affects data quality:**
- **dev**: Varied data with some edge cases (empty-ish fields, long strings, unicode)
- **demo**: Polished data that looks good in screenshots and presentations
- **testing**: Systematic data covering boundary conditions, duplicates, special characters

### 3. Plan insert order from foreign keys

Build a dependency graph from the foreign keys and insert parent tables before children.

Example order for a blog schema:

```
1. users        (no dependencies)
2. categories   (no dependencies)
3. posts        (depends on users, categories)
4. comments     (depends on users, posts)
5. tags         (no dependencies)
6. post_tags    (depends on posts, tags)
```

**Self-referencing tables** (e.g. `employees.manager_id -> employees.id`): insert root rows with a
NULL parent first, then the dependent rows.

**Circular dependencies** (A references B and B references A): insert with the nullable FK set to
NULL, then `UPDATE` to wire up the references in a second pass.

Delete in the reverse order (children first) so re-runs don't violate constraints.

### 4. Generate realistic data

Match the domain. An e-commerce seed has products with real-sounding names and prices, not
"Product 1". Do **not** use generic placeholders like `test123`, `foo@bar.com`, or "Lorem ipsum" —
that data is useless for spotting layout bugs and looks bad in demos.

For **SQL scripts** (no external libraries), keep small hardcoded pools and combine them:

- **Names**: mix genders and cultural backgrounds — `Sarah Chen`, `James Wilson`, `Priya Patel`,
  `Mohammed Garcia`, `Wei Kim`, `Aisha O'Brien`.
- **Emails**: derive from names — `sarah.chen@example.com`. Use the reserved `example.com` domain
  (RFC 2606) so nothing accidentally emails a real address.
- **Dates**: spread across a realistic range; see the engine reference for the correct literal syntax.
- **Prices/amounts**: realistic ranges, not every value `9.99`.
- **Text/content**: write 3–5 realistic variations per column and cycle through them. Don't generate
  AI-sounding prose — write like real user data.

For **Python output**, use the `faker` library with a fixed seed for reproducibility. See
[references/python-faker.md](references/python-faker.md).

Whatever the format, vary the data — don't make every user "John Smith" or every price the same.

### 5. Produce the seed script

Read the reference for the chosen target and follow its template and gotchas closely — the
escaping rules, identity/sequence handling, and multi-row syntax differ meaningfully between engines:

| Target | Reference |
|--------|-----------|
| SQL Server (T-SQL) | [references/mssql.md](references/mssql.md) |
| Oracle (PL/SQL & SQL*Plus) | [references/oracle.md](references/oracle.md) |
| Python (faker, either engine) | [references/python-faker.md](references/python-faker.md) |

Always put the run command in a comment at the top of the file, and print or log a summary of what
was seeded so the user can confirm it worked.

### 6. Make it idempotent

Seed scripts must be safe to re-run; a script that only works on a pristine database is a trap.
Two strategies:

- **Delete-then-insert** (simple, resets seed data): delete child→parent, then insert. Default for
  **dev/testing**.
- **Upsert via `MERGE`** (preserves rows users added themselves): match on the natural/primary key,
  then update or insert. Default for **demo**.

Both SQL Server and Oracle support `MERGE`; the engine references show the exact syntax.

## Quality rules

1. **Match the domain** — real-sounding names, prices, and content, never "Product 1".
2. **Vary the data** — different names, dates, and values across rows.
3. **Include edge cases for testing seeds** — empty strings, long text, special characters, boundary values.
4. **Reference real keys** — foreign keys must point to rows actually inserted earlier in the script.
5. **Escape correctly** — double single quotes in SQL literals (`O''Brien`); mind Oracle's
   empty-string-is-NULL behavior and SQL*Plus `&` substitution.
6. **Print what was seeded** — log row counts per table.
7. **Document the run command** — put it in a comment at the top of the file.
