# Employee Database Assignment - Learning Guide

## Complete Step-by-Step Tutorial

This guide will walk you through solving the assignment progressively, from simple to complex.

---

## Step 1: Understanding the Data Structure

### First, explore the employees table:

```sql
SELECT * FROM employees LIMIT 5;
```

**Output columns:**
- `emp_no` - Unique employee identifier
- `birth_date` - Date of birth (YYYY-MM-DD format)
- `first_name` - First name
- `last_name` - Last name
- `gender` - M or F
- `hire_date` - When hired (YYYY-MM-DD format)

### Explore other tables:

```sql
-- Check the salaries table structure
SELECT * FROM salaries WHERE emp_no = 10001 LIMIT 5;

-- Check the departments table
SELECT * FROM departments LIMIT 5;

-- Check the dept_emp table
SELECT * FROM dept_emp WHERE emp_no = 10001 LIMIT 5;

-- Check the titles table
SELECT * FROM titles WHERE emp_no = 10001 LIMIT 5;
```

**Key observation:** Each employee can have multiple records in `salaries`, `dept_emp`, and `titles` because these represent historical data.

---

## Step 2: Creating Full Names with CONCAT()

### Learn the CONCAT function:

```sql
-- Simple concatenation
SELECT 
    emp_no,
    CONCAT(first_name, ' ', last_name) AS full_name
FROM employees
LIMIT 5;
```

**Output:**
```
emp_no | full_name
10001  | Georgi Facello
10002  | Bezalel Simmel
```

---

## Step 3: Understanding TIMESTAMPDIFF()

### Learn date difference calculations:

```sql
-- Calculate age from birth_date
SELECT 
    emp_no,
    birth_date,
    TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age
FROM employees
LIMIT 5;
```

**Explanation:**
- `TIMESTAMPDIFF(YEAR, start_date, end_date)` returns the number of complete years between two dates
- `CURDATE()` returns today's date
- This gives you the age in complete years

### Calculate years of experience:

```sql
-- Calculate experience from hire_date
SELECT 
    emp_no,
    hire_date,
    TIMESTAMPDIFF(YEAR, hire_date, CURDATE()) AS years_of_exp
FROM employees
LIMIT 5;
```

---

## Step 4: Fetching Latest Records with Subqueries

### The Problem: Employees have multiple salary records

```sql
-- See how many salary records employee 10001 has
SELECT emp_no, salary, from_date, to_date
FROM salaries
WHERE emp_no = 10001
ORDER BY to_date DESC;
```

You'll see multiple records! We need ONLY the latest one.

### The Solution: Use a subquery to find MAX(to_date)

```sql
-- Get only the latest salary for employee 10001
SELECT salary
FROM salaries
WHERE emp_no = 10001
AND to_date = (
    SELECT MAX(to_date)
    FROM salaries
    WHERE emp_no = 10001
);
```

**How it works:**
1. Inner query: `SELECT MAX(to_date) FROM salaries WHERE emp_no = 10001` finds the maximum date
2. Outer query: Returns only the record with that maximum date
3. Result: Only ONE salary record (the latest one)

---

## Step 5: Joining Employees and Salaries

### Now combine employees with their latest salary:

```sql
SELECT 
    e.emp_no,
    CONCAT(e.first_name, ' ', e.last_name) AS full_name,
    s.salary AS latest_salary
FROM employees e
JOIN salaries s 
    ON e.emp_no = s.emp_no 
    AND s.to_date = (
        SELECT MAX(s2.to_date)
        FROM salaries s2
        WHERE s2.emp_no = e.emp_no
    )
LIMIT 5;
```

**Key points:**
- `e` is an alias for `employees` table
- `s` is an alias for `salaries` table
- The JOIN condition has TWO parts:
  1. `e.emp_no = s.emp_no` - Match employees to their salary records
  2. `s.to_date = (subquery)` - Keep only the latest salary
- In the subquery, use `s2` as a different alias to avoid confusion

---

## Step 6: Adding Department Information

### Similar approach for departments:

```sql
SELECT 
    e.emp_no,
    CONCAT(e.first_name, ' ', e.last_name) AS full_name,
    s.salary AS latest_salary,
    d.dept_name AS recent_department
FROM employees e
JOIN salaries s 
    ON e.emp_no = s.emp_no 
    AND s.to_date = (
        SELECT MAX(s2.to_date)
        FROM salaries s2
        WHERE s2.emp_no = e.emp_no
    )
JOIN dept_emp de 
    ON e.emp_no = de.emp_no 
    AND de.to_date = (
        SELECT MAX(de2.to_date)
        FROM dept_emp de2
        WHERE de2.emp_no = e.emp_no
    )
JOIN departments d 
    ON de.dept_no = d.dept_no
LIMIT 5;
```

**New concepts:**
- `de` is an alias for `dept_emp` table (department-employee mapping)
- We need TWO joins: first to `dept_emp` to get the latest department assignment, then to `departments` to get the department name
- Each JOIN follows the same pattern: match AND filter for latest record

---

## Step 7: Adding Job Title

### Add one more table for titles:

```sql
SELECT 
    e.emp_no,
    CONCAT(e.first_name, ' ', e.last_name) AS full_name,
    s.salary AS latest_salary,
    d.dept_name AS recent_department,
    t.title AS max_title
FROM employees e
JOIN salaries s 
    ON e.emp_no = s.emp_no 
    AND s.to_date = (
        SELECT MAX(s2.to_date)
        FROM salaries s2
        WHERE s2.emp_no = e.emp_no
    )
JOIN dept_emp de 
    ON e.emp_no = de.emp_no 
    AND de.to_date = (
        SELECT MAX(de2.to_date)
        FROM dept_emp de2
        WHERE de2.emp_no = e.emp_no
    )
JOIN departments d 
    ON de.dept_no = d.dept_no
JOIN titles t 
    ON e.emp_no = t.emp_no 
    AND t.to_date = (
        SELECT MAX(t2.to_date)
        FROM titles t2
        WHERE t2.emp_no = e.emp_no
    )
LIMIT 5;
```

---

## Step 8: Final Query with Date Calculations

### Complete solution combining everything:

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
    AND s.to_date = (
        SELECT MAX(s2.to_date)
        FROM salaries s2
        WHERE s2.emp_no = e.emp_no
    )
JOIN dept_emp de 
    ON e.emp_no = de.emp_no 
    AND de.to_date = (
        SELECT MAX(de2.to_date)
        FROM dept_emp de2
        WHERE de2.emp_no = e.emp_no
    )
JOIN departments d 
    ON de.dept_no = d.dept_no
JOIN titles t 
    ON e.emp_no = t.emp_no 
    AND t.to_date = (
        SELECT MAX(t2.to_date)
        FROM titles t2
        WHERE t2.emp_no = e.emp_no
    )
LIMIT 10;
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Forgetting the Subquery
```sql
-- WRONG - This returns multiple rows per employee
SELECT e.emp_no, s.salary
FROM employees e
JOIN salaries s ON e.emp_no = s.emp_no;
```

### ✅ Correct: Include the subquery filter
```sql
-- CORRECT - Returns one salary per employee (latest)
SELECT e.emp_no, s.salary
FROM employees e
JOIN salaries s 
    ON e.emp_no = s.emp_no 
    AND s.to_date = (SELECT MAX(s2.to_date) FROM salaries s2 WHERE s2.emp_no = e.emp_no);
```

---

### ❌ Mistake 2: Using Wrong Table Alias in Subquery
```sql
-- WRONG - Subquery references wrong table alias
SELECT e.emp_no, t.title
FROM employees e
JOIN titles t 
    ON e.emp_no = t.emp_no 
    AND t.to_date = (SELECT MAX(s.to_date) FROM titles s WHERE s.emp_no = e.emp_no);
    -- Using 's' instead of 't2' causes confusion
```

### ✅ Correct: Use consistent naming
```sql
-- CORRECT - Clear subquery alias
SELECT e.emp_no, t.title
FROM employees e
JOIN titles t 
    ON e.emp_no = t.emp_no 
    AND t.to_date = (SELECT MAX(t2.to_date) FROM titles t2 WHERE t2.emp_no = e.emp_no);
```

---

### ❌ Mistake 3: Forgetting Secondary Join
```sql
-- WRONG - dept_emp doesn't have dept_name
SELECT e.emp_no, de.dept_name
FROM employees e
JOIN dept_emp de ON e.emp_no = de.emp_no;
-- dept_emp has dept_no, not dept_name!
```

### ✅ Correct: Join departments table too
```sql
-- CORRECT - Two joins to get department name
SELECT e.emp_no, d.dept_name
FROM employees e
JOIN dept_emp de ON e.emp_no = de.emp_no
JOIN departments d ON de.dept_no = d.dept_no;
```

---

## Testing Tips

### Test each component separately:

```sql
-- Test 1: Employee names
SELECT emp_no, CONCAT(first_name, ' ', last_name) FROM employees LIMIT 3;

-- Test 2: Age calculation
SELECT emp_no, birth_date, TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age FROM employees LIMIT 3;

-- Test 3: Latest salary for one employee
SELECT * FROM salaries WHERE emp_no = 10001 ORDER BY to_date DESC;

-- Test 4: Join logic
SELECT e.emp_no, s.salary FROM employees e
JOIN salaries s ON e.emp_no = s.emp_no
WHERE e.emp_no = 10001;
```

---

## Advanced Challenges

Once you complete the basic assignment, try these:

### Challenge 1: Add salary range categories
```sql
-- Add a new column categorizing salary as "Low", "Medium", "High"
SELECT 
    ...,
    CASE 
        WHEN s.salary < 50000 THEN 'Low'
        WHEN s.salary < 100000 THEN 'Medium'
        ELSE 'High'
    END AS salary_range
FROM ...
```

### Challenge 2: Filter by department or title
```sql
-- Show only employees in specific departments
WHERE d.dept_name = 'Sales';

-- Show only employees with specific titles
WHERE t.title = 'Senior Engineer';
```

### Challenge 3: Calculate tenure in current position
```sql
-- How long has employee been in current department?
TIMESTAMPDIFF(YEAR, de.from_date, CURDATE()) AS years_in_dept
```

### Challenge 4: Optimization with CTEs
```sql
-- Use Common Table Expressions (CTE) to organize the query
WITH latest_salaries AS (
    SELECT emp_no, salary, to_date
    FROM salaries
    WHERE to_date = (SELECT MAX(to_date) FROM salaries)
),
...
SELECT * FROM employees e
JOIN latest_salaries ls ON e.emp_no = ls.emp_no;
```

---

## Debugging Guide

If your query returns no results or errors:

### Problem: "Column not found"
**Solution:** Check your table aliases and column names. Remember `dept_emp` has `dept_no`, not `dept_name`.

### Problem: "Too many rows" (more than expected)
**Solution:** You're missing a subquery filter. Add the `AND ... = (SELECT MAX(...))` condition.

### Problem: "Wrong number of columns in result"
**Solution:** Check your SELECT statement. Did you include all 7 required columns?

### Problem: "Dates seem wrong"
**Solution:** Verify you're using `TIMESTAMPDIFF(YEAR, older_date, newer_date)` in the right order.

---

Good luck! Remember: SQL is about asking the right questions and filtering data logically. Test incrementally and you'll master this!
