# Oracle (PL/SQL & SQL*Plus) Seed Scripts

Target: Oracle Database. Output a single `.sql` file runnable via SQL*Plus or SQLcl.

## Template

```sql
/*
 * seed.sql - sample data for <schema> (dev)
 * Run: sqlplus user/password@//host:1521/service @seed.sql
 *   or SQLcl: sql user/password@//host:1521/service @seed.sql
 */
SET DEFINE OFF;   -- critical: stop SQL*Plus treating '&' in data as a substitution variable
WHENEVER SQLERROR EXIT FAILURE ROLLBACK;

-- Clear existing data (child -> parent order)
DELETE FROM comments;
DELETE FROM posts;
DELETE FROM users;

-- users -- id is GENERATED ALWAYS AS IDENTITY; let Oracle assign it.
INSERT ALL
  INTO users (name, email, is_active, created_at)
       VALUES ('Sarah Chen',   'sarah.chen@example.com',   1, TIMESTAMP '2025-01-15 10:30:00')
  INTO users (name, email, is_active, created_at)
       VALUES ('James Wilson', 'james.wilson@example.com', 1, TIMESTAMP '2025-02-01 14:22:00')
  INTO users (name, email, is_active, created_at)
       VALUES ('Priya Patel',  'priya.patel@example.com',  0, TIMESTAMP '2025-02-18 09:05:00')
SELECT 1 FROM dual;

-- posts (FK -> users): reference parents by natural key (email), not hardcoded ids.
INSERT INTO posts (user_id, title, body, published_at)
SELECT u.id, 'Getting started with widgets', 'A practical intro...', TIMESTAMP '2025-03-01 09:00:00'
  FROM users u WHERE u.email = 'sarah.chen@example.com'
UNION ALL
SELECT u.id, 'Why we switched stacks', 'Six months ago...', TIMESTAMP '2025-03-04 16:40:00'
  FROM users u WHERE u.email = 'james.wilson@example.com';

COMMIT;

-- Summary
SET SERVEROUTPUT ON;
DECLARE
  v_users NUMBER;
  v_posts NUMBER;
BEGIN
  SELECT COUNT(*) INTO v_users FROM users;
  SELECT COUNT(*) INTO v_posts FROM posts;
  DBMS_OUTPUT.PUT_LINE('Seeded users=' || v_users || ' posts=' || v_posts);
END;
/
```

## Sequences (pre-12c, or explicit ids)

If the table uses a sequence rather than an identity column:

```sql
INSERT INTO users (id, name, email)
VALUES (users_seq.NEXTVAL, 'Sarah Chen', 'sarah.chen@example.com');
```

To reference the row you just inserted from inside PL/SQL, use `RETURNING`:

```sql
DECLARE
  v_id users.id%TYPE;
BEGIN
  INSERT INTO users (name, email) VALUES ('Sarah Chen', 'sarah.chen@example.com')
    RETURNING id INTO v_id;
  INSERT INTO posts (user_id, title) VALUES (v_id, 'Getting started with widgets');
END;
/
```

## Idempotent upsert (MERGE)

```sql
MERGE INTO users t
USING (
  SELECT 'sarah.chen@example.com'   AS email, 'Sarah Chen'   AS name, 1 AS is_active FROM dual
  UNION ALL
  SELECT 'james.wilson@example.com',          'James Wilson',        1            FROM dual
) src
ON (t.email = src.email)
WHEN MATCHED THEN UPDATE SET t.name = src.name, t.is_active = src.is_active
WHEN NOT MATCHED THEN INSERT (name, email, is_active) VALUES (src.name, src.email, src.is_active);
COMMIT;
```

## Gotchas

| Gotcha                  | Solution                                                                                                                            |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| No multi-tuple `VALUES` | Use `INSERT ALL ... SELECT 1 FROM dual`, `INSERT ... SELECT ... UNION ALL`, or one INSERT per row                                   |
| `&` in string data      | `SET DEFINE OFF;` at the top of the script                                                                                          |
| Empty string = NULL     | `''` is stored as `NULL`; never use it for a `NOT NULL` column — supply a real value                                                |
| Booleans                | No SQL `BOOLEAN` before 23c; use `NUMBER(1)` (0/1) or `CHAR(1)` ('Y'/'N')                                                           |
| Dates/times             | `DATE '2025-01-15'`, `TIMESTAMP '2025-01-15 10:30:00'`, or `TO_DATE('15-01-2025','DD-MM-YYYY')`; `SYSDATE` / `SYSTIMESTAMP` for now |
| Identity vs sequence    | 12c+ `GENERATED ... AS IDENTITY` auto-fills; otherwise use `seq.NEXTVAL`                                                            |
| GUIDs                   | `SYS_GUID()` returns `RAW(16)`                                                                                                      |
| Large text              | Use `CLOB`; plain string literals cap at 4000 bytes (32767 with extended types) — split long content                                |
| Single quotes in data   | Double them (`'O''Brien'`) or use a quoted literal `q'[O'Brien]'`                                                                   |
| Terminators             | `;` ends a SQL statement; a lone `/` on its own line runs the preceding PL/SQL block                                                |
| Commit                  | Oracle does not autocommit — end the script with `COMMIT;`                                                                          |
