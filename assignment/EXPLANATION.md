# Employee Database Assignment - Detailed Explanation

## Overview
This document explains the logic, structure, and reasoning behind the solution to the employee database assignment.

---

## What the Query Does

The query creates a comprehensive **employee snapshot report** showing:
- Who each employee is (ID and full name)
- How much they currently earn (latest salary)
- Where they work (current department)
- What position they hold (current job title)
- How long they've been with the company (years of experience)
- How old they are (calculated from birth date)

---

## Why This Query Is Complex

The assignment is challenging because the **employee database tracks history**. This means:

### Problem 1: Multiple Salary Records
```
emp_no | salary | from_date  | to_date
-------|--------|------------|------------
10001  | 60000  | 1986-06-26 | 1987-06-26
10001  | 65000  | 1987-06-26 | 1988-06-25
10001  | 71046  | 1988-06-25 | 2001-09-09  ← LATEST
```
Employee 10001 has had multiple salaries! We need ONLY the most recent one (latest `to_date`).

### Problem 2: Multiple Department Assignments
An employee may have worked in different departments over time. We need to track which department they currently work in.

### Problem 3: Multiple Job Titles
Similarly, employees have had different titles throughout their career. We need their current title.

### Solution: Use Subqueries to Filter
For each employee, find the records with the **maximum `to_date`** value - that's the latest one!

---

## Breaking Down the Query

### Section 1: SELECT Clause

```sql
SELECT 
    e.emp_no,
    CONCAT(e.first_name, ' ', e.last_name) AS full_name,
    s.salary AS latest_salary,
    d.dept_name AS recent_department,
    t.title AS max_title,
    TIMESTAMPDIFF(YEAR, e.hire_date, CURDATE()) AS years_of_exp,
    TIMESTAMPDIFF(YEAR, e.birth_date, CURDATE()) AS age
```

**What's happening:**
- `e.emp_no` - Get the employee ID from the `employees` table
- `CONCAT(e.first_name, ' ', e.last_name) AS full_name` - Combine first and last names into one readable field
- `s.salary AS latest_salary` - Get salary from the `salaries` table
- `d.dept_name AS recent_department` - Get department name from `departments` table
- `t.title AS max_title` - Get job title from `titles` table
- `TIMESTAMPDIFF(...)` - Calculate years as a time difference

**Key Point:** We're pulling data from multiple tables that we'll JOIN next.

---

### Section 2: FROM Clause

```sql
FROM employees e
```

**What's happening:**
- Start with the `employees` table as the main/left table
- Use alias `e` for brevity (instead of typing `employees` every time)

**Why:** Every query needs a starting table. Employees is our main entity, and we'll add other data to it.

---

### Section 3: JOIN SALARIES

```sql
JOIN salaries s 
    ON e.emp_no = s.emp_no 
    AND s.to_date = (
        SELECT MAX(s2.to_date)
        FROM salaries s2
        WHERE s2.emp_no = e.emp_no
    )
```

**What's happening:**

1. **`JOIN salaries s`** - Connect to the salaries table, alias it as `s`

2. **`ON e.emp_no = s.emp_no`** - First condition: Match employee records to salary records by employee ID

3. **`AND s.to_date = (...subquery...)`** - Second condition: ONLY match the salary record where `to_date` is the maximum (latest)

4. **Subquery breakdown:**
   ```sql
   SELECT MAX(s2.to_date)
   FROM salaries s2
   WHERE s2.emp_no = e.emp_no
   ```
   This finds the latest date for the current employee. We use `s2` (different alias) to avoid confusion with the outer `s`.

**Example:** For employee 10001:
- Without the second condition: Would return 3 salary records
- With the subquery: Returns ONLY the record with the maximum to_date (the latest one)

**Why it matters:** Without this subquery, each employee would appear multiple times in the result!

---

### Section 4: JOIN DEPT_EMP and DEPARTMENTS

```sql
JOIN dept_emp de 
    ON e.emp_no = de.emp_no 
    AND de.to_date = (
        SELECT MAX(de2.to_date)
        FROM dept_emp de2
        WHERE de2.emp_no = e.emp_no
    )

JOIN departments d 
    ON de.dept_no = d.dept_no
```

**What's happening:**

1. **First JOIN (dept_emp):**
   - Connect to `dept_emp` table which maps employees to departments
   - Use same subquery pattern: match employee AND filter for latest department assignment
   - Use alias `de` for dept_emp table
   - Use `de2` in subquery (different alias for clarity)

2. **Second JOIN (departments):**
   - Connect to `departments` table
   - Simple join: `de.dept_no = d.dept_no` (no subquery needed here)
   - Why? Because we want the readable department name (d.dept_name) which corresponds to the dept_no from our latest dept_emp record

**Why two joins?**
- `dept_emp` has employee and department IDs, but NOT the department name
- `departments` has the pretty names like "Finance", "Sales", etc.
- So we need both tables to get the full information

**Visual flow:**
```
employees → dept_emp → departments
10001       (10001, d001) → (d001, "Finance")
                           ↓
                    "Finance" (readable name)
```

---

### Section 5: JOIN TITLES

```sql
JOIN titles t 
    ON e.emp_no = t.emp_no 
    AND t.to_date = (
        SELECT MAX(t2.to_date)
        FROM titles t2
        WHERE t2.emp_no = e.emp_no
    )
```

**What's happening:**
- Connect to `titles` table
- Same pattern as salaries: match employee AND filter for latest title
- Use `t` for titles, `t2` for subquery
- Result: Get only the current title for each employee

**Example:** If employee 10001 was "Engineer" then "Senior Engineer" then "Manager":
- Without subquery: Would return all 3 title history records
- With subquery: Returns ONLY "Manager" (the current title)

---

## Critical Insight: Why Subqueries Work

### The Problem They Solve

In historical databases, each fact (salary, department, title) is stored as a series of records with dates:

| emp_no | salary | from_date | to_date |
|--------|--------|-----------|---------|
| 10001  | 50000  | 1986-06 | 1987-06 |
| 10001  | 60000  | 1987-06 | 1988-06 |
| 10001  | 70000  | 1988-06 | 2001-09 | ← **Latest** (to_date is maximum)

Without filtering, a JOIN would return all rows. But we want ONLY the latest.

### The Solution

```sql
AND s.to_date = (SELECT MAX(s2.to_date) FROM salaries s2 WHERE s2.emp_no = e.emp_no)
```

This says: "Match ONLY if the salary's to_date equals the maximum to_date for this employee"

Result: Only the row with 70000 is returned.

### Why Use MAX(to_date)?

In this database:
- **to_date = future date** → Record is currently active (e.g., 9999-01-01)
- **to_date = past date** → Record is historical (e.g., 1988-06-25)

The `MAX()` always finds the most recent date, regardless of format!

---

## How the Joins Connect

Here's how a single row is built:

```
Employee Record (e)
    ↓
+ Latest Salary (s, filtered by MAX(to_date))
    ↓
+ Latest Department Assignment (de, filtered by MAX(to_date))
    ↓
+ Department Name (d, joined from dept_no)
    ↓
+ Latest Title (t, filtered by MAX(to_date))
    ↓
+ Calculated Fields (CONCAT, TIMESTAMPDIFF)
    ↓
= One complete row showing current snapshot
```

Each JOIN adds information to the building row.

---

## Date Calculations Explained

### TIMESTAMPDIFF Function

```sql
TIMESTAMPDIFF(YEAR, e.birth_date, CURDATE()) AS age
```

**Breakdown:**
- `TIMESTAMPDIFF(unit, start_date, end_date)` - Returns difference between dates
- `YEAR` - We want the difference in complete years
- `e.birth_date` - Starting point (when they were born)
- `CURDATE()` - Ending point (today's date)
- Result: Complete years of age

**Example:**
- Born: 1962-12-05
- Today: 2026-03-26
- Result: 63 complete years (will turn 64 later this year)

### CONCAT for Full Names

```sql
CONCAT(e.first_name, ' ', e.last_name) AS full_name
```

**Breakdown:**
- `CONCAT()` - String concatenation function
- `e.first_name` - First value ("Georgi")
- `' '` - Literal space
- `e.last_name` - Last value ("Facello")
- Result: "Georgi Facello"

**Why this matters:** Readable output for humans!

---

## Common Variations & Extensions

### Finding Employees in a Specific Department
```sql
-- Add WHERE clause at the end
WHERE d.dept_name = 'Sales'
```

### Finding only specific titles
```sql
WHERE t.title = 'Senior Engineer'
```

### Filtering by salary range
```sql
WHERE s.salary BETWEEN 50000 AND 100000
```

### Calculating tenure in current position
```sql
SELECT 
    ...,
    TIMESTAMPDIFF(YEAR, de.from_date, CURDATE()) AS years_in_current_dept
FROM ...
```

### Finding employees hired in specific year
```sql
WHERE YEAR(e.hire_date) = 2000
```

---

## Performance Considerations

### Current Query Performance

The query runs **5 subqueries** (one for each table with historical data). For large databases (100k+ employees), this could be slow.

### Optimization Approach 1: Using Window Functions (MySQL 8.0+)
```sql
WITH latest_records AS (
    SELECT 
        emp_no,
        salary,
        ROW_NUMBER() OVER (PARTITION BY emp_no ORDER BY to_date DESC) AS rn
    FROM salaries
)
SELECT * FROM latest_records WHERE rn = 1
```

This is often faster than subqueries.

### Optimization Approach 2: Indexing
Ensure these indexes exist:
```sql
CREATE INDEX idx_emp_no ON salaries(emp_no, to_date);
CREATE INDEX idx_emp_no ON dept_emp(emp_no, to_date);
CREATE INDEX idx_emp_no ON titles(emp_no, to_date);
```

---

## Key Takeaways

✅ **Subqueries are powerful** for filtering historical data
✅ **Multiple JOINs** let you combine data from many tables
✅ **Table aliases** keep code readable (e vs employees)
✅ **Different aliases in subqueries** prevent confusion (s vs s2)
✅ **Date calculations** add business logic (age, experience)
✅ **Understanding data structure** is key - Why is there a dept_emp table? Why historical dates?

---

## Troubleshooting Common Issues

### Issue: "0 rows returned"
**Cause:** Wrong JOIN condition or subquery filtering nothing
**Solution:** Test each subquery independently to verify it returns valid to_date values

### Issue: "Duplicate rows per employee"
**Cause:** Missing AND condition with subquery
**Solution:** Verify the `AND [table].to_date = (SELECT MAX...)` is present on all historical tables

### Issue: "Wrong department name showing"
**Cause:** Missing the departments JOIN or used wrong alias
**Solution:** Verify you have both `JOIN dept_emp` AND `JOIN departments d ON de.dept_no = d.dept_no`

### Issue: "Null values in results"
**Cause:** Using LEFT JOIN instead of INNER JOIN, or employee has no data in a table
**Solution:** Use INNER JOIN (current query) if you want only complete records, or LEFT JOIN if you want all employees even without some data

---

This completes the explanation. Practice writing this query step-by-step, and you'll master these important SQL techniques!
