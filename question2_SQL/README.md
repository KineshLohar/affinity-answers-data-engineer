# Rfam SQL Terminal — Question 1

You can also double-click `run.bat`.

or

## Setup

1. Install Node.js LTS from https://nodejs.org/
2. Extract the project ZIP.
3. Open PowerShell in the extracted project folder.
4. Install the required packages:

```powershell
npm install
```

## Run the SQL Terminal

```powershell
npm start
```

When the `SQL>` prompt appears, enter your SQL queries. End each query with a semicolon (`;`). Type `exit` to close the terminal.

## Question 1: Count Acacia Types

### Approach

**Step 1: Identify the database schema**

We inspected the database schema and identified the `taxonomy` table and its `species` column as relevant to the question.

```sql
DESCRIBE taxonomy;
```

**Step 2: Inspect sample data**

We used `LIMIT` to view a small number of records and understand how taxonomy names were stored.

```sql
SELECT *
FROM taxonomy
LIMIT 10;
```

**Step 3: Search for Acacia anywhere in the name**

Initially, we used wildcards on both sides of `Acacia` to find names containing that text anywhere.

```sql
SELECT *
FROM taxonomy
WHERE species LIKE "%Acacia%"
LIMIT 100;
```

The `%` wildcard matches any sequence of characters.

**Step 4: Refine the filter**

After inspecting the results, we changed the pattern to `Acacia%` so that the name must begin with `Acacia`.

```sql
SELECT *
FROM taxonomy
WHERE species LIKE "Acacia%"
LIMIT 100;
```

**Step 5: Count matching rows**

```sql
SELECT COUNT(*)
FROM taxonomy
WHERE species LIKE "Acacia%";
```

Result: `326`

**Step 6: Count distinct species names**

To check whether duplicate `species` values affected the count, we ran:

```sql
SELECT COUNT(DISTINCT species)
FROM taxonomy
WHERE species LIKE "Acacia%";
```

Result: `326`

Both counts were the same, indicating that the matching rows contained no duplicate `species` values.

### Final Result

**326 distinct `species` values** begin with `Acacia` in the `taxonomy` table.

This result counts matching database values. The table may include varieties or hybrids, so the result should be described as distinct matching `species` values rather than assuming each value represents a separate botanical species.

### SQL Concepts Used

- `LIMIT` — inspect sample records.
- `LIKE` — match a text pattern.
- `%` — wildcard for any sequence of characters.
- `COUNT(*)` — count matching rows.
- `COUNT(DISTINCT species)` — count unique species values.
