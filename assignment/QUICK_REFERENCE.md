# Employee Database Assignment - Quick Reference

## Assignment at a Glance

**Goal:** Write a SQL query that retrieves comprehensive employee information combining data from 5 tables.

**Difficulty:** Intermediate (Requires: JOINs, Subqueries, Date Functions, String Concatenation)

**Time to Complete:** 2-3 hours for beginners, 30-45 minutes for experienced SQL developers

---

## What You're Building

A single SQL query that returns this output:

```
emp_no | full_name | latest_salary | recent_department | max_title | years_of_exp | age
-------|-----------|---------------|-------------------|-----------|--------------|-----
10001  | Name Here | 88958         | Finance           | Engineer  | 33           | 62
```

---

## The 6 Key SQL Concepts

| # | Concept | Example |
|---|---------|---------|
| 1 | **CONCAT()** | `CONCAT(first_name, ' ', last_name)` |
| 2 | **INNER JOIN** | `JOIN table2 ON condition` |
| 3 | **Subqueries** | `(SELECT MAX(to_date) FROM ...)` |
| 4 | **MAX() Function** | Find latest date across multiple records |
| 5 | **TIMESTAMPDIFF()** | `TIMESTAMPDIFF(YEAR, start_date, end_date)` |
| 6 | **Table Aliases** | Use `e`, `s`, `d`, `de`, `t` for each table |

---

## 5 Tables You'll Use

```
employees ──→ salaries (get latest salary)
          ──→ dept_emp ──→ departments (get current dept)
          ──→ titles (get latest title)
```

---

## The Query Structure (Scaffold)

```sql
SELECT 
    e.emp_no,
    CONCAT(e.first_name, ' ', e.last_name) AS full_name,
    s.salary AS latest_salary,
    d.dept_name AS recent_department,
    t.title AS max_title,
    TIMESTAMPDIFF(YEAR, e.hire_date, CURDATE()) AS years_of_exp,
    TIMESTAMPDIFF(YEAR, e.birth_date, CURDATE()) AS age
FROM employees e
JOIN salaries s 
    ON e.emp_no = s.emp_no 
    AND s.to_date = (SELECT MAX(s2.to_date) FROM salaries s2 WHERE s2.emp_no = e.emp_no)
JOIN dept_emp de 
    ON e.emp_no = de.emp_no 
    AND de.to_date = (SELECT MAX(de2.to_date) FROM dept_emp de2 WHERE de2.emp_no = e.emp_no)
JOIN departments d ON de.dept_no = d.dept_no
JOIN titles t 
    ON e.emp_no = t.emp_no 
    AND t.to_date = (SELECT MAX(t2.to_date) FROM titles t2 WHERE t2.emp_no = e.emp_no);
```

---

## Step-by-Step Implementation

### Step 1: Start with Employees
```sql
SELECT e.emp_no FROM employees e LIMIT 5;
```

### Step 2: Add Names
```sql
SELECT 
    e.emp_no,
    CONCAT(e.first_name, ' ', e.last_name) AS full_name
FROM employees e LIMIT 5;
```

### Step 3: Add Salary JOIN
```sql
SELECT 
    e.emp_no,
    CONCAT(e.first_name, ' ', e.last_name) AS full_name,
    s.salary
FROM employees e
JOIN salaries s ON e.emp_no = s.emp_no
LIMIT 5;  -- Will show duplicates per employee
```

### Step 4: Filter Latest Salary
```sql
SELECT 
    e.emp_no,
    CONCAT(e.first_name, ' ', e.last_name) AS full_name,
    s.salary
FROM employees e
JOIN salaries s 
    ON e.emp_no = s.emp_no 
    AND s.to_date = (SELECT MAX(s2.to_date) FROM salaries s2 WHERE s2.emp_no = e.emp_no)
LIMIT 5;  -- Now shows one row per employee
```

### Step 5: Add Department
```sql
-- Add dept_emp JOIN + departments JOIN (see full query above)
```

### Step 6: Add Title
```sql
-- Add titles JOIN (see full query above)
```

### Step 7: Add Calculations
```sql
-- Add TIMESTAMPDIFF for years_of_exp and age (see full query above)
```

---

## Critical Pattern: Getting Latest Records

**Problem:** Some tables have multiple records per employee

**Solution:** Use this pattern for each historical table:
```sql
AND [table].to_date = (
    SELECT MAX([table2].to_date) 
    FROM [table] [table2] 
    WHERE [table2].emp_no = e.emp_no
)
```

**Apply to:** salaries, dept_emp, titles

**Don't apply to:** employees (1 row per employee), departments (just a lookup table)

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| No columns named `dept_name` | dept_emp doesn't have dept names | Join departments table |
| Duplicate rows per employee | Missing subquery on historical table | Add AND with (SELECT MAX(...)) |
| Wrong department showing | Missing dept_emp table | Add JOIN dept_emp BEFORE JOIN departments |
| Syntax error near subquery | Missing comma or parenthesis | Check surrounding syntax |
| NULL in years_of_exp | Wrong date order in TIMESTAMPDIFF | Use (YEAR, older_date, newer_date) |

---

## Useful Debugging Queries

```sql
-- Check employee 10001's salary history
SELECT * FROM salaries WHERE emp_no = 10001 ORDER BY to_date DESC;

-- Check what's the latest salary
SELECT MAX(to_date) FROM salaries WHERE emp_no = 10001;

-- Test the subquery logic
SELECT s.salary FROM salaries s
WHERE emp_no = 10001 
AND s.to_date = (SELECT MAX(s2.to_date) FROM salaries s2 WHERE s2.emp_no = 10001);

-- Check if employee has empty tables
SELECT e.emp_no, COUNT(s.emp_no) as salary_count
FROM employees e
LEFT JOIN salaries s ON e.emp_no = s.emp_no
WHERE e.emp_no = 10001;
```

---

## Performance Tips

✅ **Use indexes** on `emp_no` and `to_date` in historical tables
✅ **LIMIT 10** when testing to see results faster
✅ **Add WHERE clause** to filter specific employees while debugging
✅ **Run piece by piece** - don't run entire query if testing one part

---

## Requirements Checklist

- [ ] Query selects all 7 required columns
- [ ] emp_no values are correct (integers)
- [ ] full_name is concatenated and readable
- [ ] latest_salary shows current salary (not historical)
- [ ] recent_department shows current department
- [ ] max_title shows current job title
- [ ] years_of_exp calculated correctly
- [ ] age calculated correctly
- [ ] No NULL values in any column
- [ ] No duplicate rows (one row per employee)
- [ ] All table JOINs are correct
- [ ] Subqueries filter for latest records
- [ ] Code is well-commented

---

## Advanced Enhancements (Optional)

Once basic query works, try these:

1. **Add salary categories**
   ```sql
   CASE WHEN salary < 50000 THEN 'Entry' 
        WHEN salary < 100000 THEN 'Mid' 
        ELSE 'Senior' END
   ```

2. **Filter by department**
   ```sql
   WHERE d.dept_name = 'Sales'
   ```

3. **Calculate tenure in current role**
   ```sql
   TIMESTAMPDIFF(YEAR, de.from_date, CURDATE()) AS current_dept_years
   ```

4. **Sort by salary descending**
   ```sql
   ORDER BY s.salary DESC
   ```

5. **Convert to CTE version** (MySQL 8.0+)
   ```sql
   WITH latest_salaries AS (
       SELECT emp_no, salary FROM salaries WHERE to_date = 9999-01-01
   )
   SELECT * FROM employees e JOIN latest_salaries USING (emp_no)
   ```

---

## Resources

| Resource | Link |
|----------|------|
| See [PROBLEM_STATEMENT.md](PROBLEM_STATEMENT.md) | Full assignment details and learning objectives |
| See [LEARNING_GUIDE.md](LEARNING_GUIDE.md) | Step-by-step tutorial building the query |
| See [EXPLANATION.md](EXPLANATION.md) | Detailed explanation of every part |
| See [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) | Complete schema reference |
| See [solution.sql](solution.sql) | Complete working solution with comments |
| See [SAMPLE_OUTPUT.txt](SAMPLE_OUTPUT.txt) | Expected output format |

---

## Quick Answer Key

**If you're stuck:**

1. Check [LEARNING_GUIDE.md](LEARNING_GUIDE.md) for step-by-step instructions
2. Reference [EXPLANATION.md](EXPLANATION.md) for detailed explanations
3. Review [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) to understand table relationships
4. Compare against [solution.sql](solution.sql) to see the complete query
5. Check [SAMPLE_OUTPUT.txt](SAMPLE_OUTPUT.txt) for expected results

---

**Good luck! Remember: Take it step by step, test frequently, and refer to the docs when stuck.**
