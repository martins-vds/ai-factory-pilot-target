# SQL Server (T-SQL) Seed Scripts

Target: Microsoft SQL Server / Azure SQL. Output a single `.sql` file runnable via `sqlcmd`, SSMS,
or Azure Data Studio.

## Template

```sql
/*
 * seed.sql - sample data for <database> (dev)
 * Run: sqlcmd -S localhost -d MyDb -i seed.sql
 *   or open in SSMS / Azure Data Studio and execute.
 */
SET NOCOUNT ON;
SET XACT_ABORT ON;   -- abort and roll back the whole batch on any error

BEGIN TRANSACTION;

-- Clear existing data (child -> parent order)
DELETE FROM dbo.comments;
DELETE FROM dbo.posts;
DELETE FROM dbo.users;

-- users -- table has IDENTITY(1,1) on id; let SQL Server assign ids.
INSERT INTO dbo.users (name, email, is_active, created_at) VALUES
  (N'Sarah Chen',   N'sarah.chen@example.com',   1, '2025-01-15T10:30:00'),
  (N'James Wilson', N'james.wilson@example.com', 1, '2025-02-01T14:22:00'),
  (N'Priya Patel',  N'priya.patel@example.com',  0, '2025-02-18T09:05:00');

-- posts (FK -> users): reference parents by natural key (email), not hardcoded ids.
INSERT INTO dbo.posts (user_id, title, body, published_at)
SELECT u.id, v.title, v.body, v.published_at
FROM (VALUES
  (N'sarah.chen@example.com',   N'Getting started with widgets', N'A practical intro...', '2025-03-01T09:00:00'),
  (N'james.wilson@example.com', N'Why we switched stacks',       N'Six months ago...',    '2025-03-04T16:40:00')
) AS v(email, title, body, published_at)
JOIN dbo.users u ON u.email = v.email;

COMMIT TRANSACTION;

-- Summary
SELECT 'users' AS table_name, COUNT(*) AS row_count FROM dbo.users
UNION ALL SELECT 'posts', COUNT(*) FROM dbo.posts;
```

## Inserting explicit IDENTITY values

If you must control identity values (e.g. to hardcode FK references), toggle `IDENTITY_INSERT` for
one table at a time:

```sql
SET IDENTITY_INSERT dbo.users ON;
INSERT INTO dbo.users (id, name, email) VALUES (1, N'Sarah Chen', N'sarah.chen@example.com');
SET IDENTITY_INSERT dbo.users OFF;   -- only one table may have it ON at a time
```

## Idempotent upsert (MERGE)

Use for demo seeds that must not clobber rows the user added:

```sql
MERGE dbo.users AS target
USING (VALUES
  (N'sarah.chen@example.com',   N'Sarah Chen',   1),
  (N'james.wilson@example.com', N'James Wilson', 1)
) AS src (email, name, is_active)
ON target.email = src.email
WHEN MATCHED THEN UPDATE SET name = src.name, is_active = src.is_active
WHEN NOT MATCHED THEN INSERT (email, name, is_active) VALUES (src.email, src.name, src.is_active);
```

The trailing semicolon on a `MERGE` statement is required, not optional.

## Gotchas

| Gotcha                      | Solution                                                                                                |
| --------------------------- | ------------------------------------------------------------------------------------------------------- |
| `INSERT ... VALUES` row cap | Max **1000** row tuples per statement; batch larger sets                                                |
| IDENTITY columns            | Omit the column, or wrap explicit values in `SET IDENTITY_INSERT ... ON/OFF` (one table at a time)      |
| Booleans                    | Use `BIT` with `0` / `1`                                                                                |
| Dates/times                 | `'YYYY-MM-DDTHH:MM:SS'` literals for `DATETIME2`; or `SYSDATETIME()`, `DATEADD(DAY, -n, SYSDATETIME())` |
| Unicode text                | Use `NVARCHAR` and prefix literals with `N'...'`                                                        |
| GUIDs                       | `NEWID()` for `uniqueidentifier`                                                                        |
| Single quotes in data       | Double them: `N'O''Brien'`                                                                              |
| FK enforcement              | Insert parents first; delete children first                                                             |
| Whole-script safety         | `SET XACT_ABORT ON` plus a single `BEGIN TRAN` / `COMMIT` so any failure rolls everything back          |
| Batch separators            | Use `GO` only in sqlcmd/SSMS scripts, and never inside a transaction you need to stay atomic            |

For many child rows, prefer the `INSERT ... SELECT ... JOIN` pattern in the template (join children
to parents on a natural key) over capturing each generated id by hand.
