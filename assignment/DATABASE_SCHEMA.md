# Employee Database Schema Reference

## Complete Database Structure

This document describes all tables used in the assignment and how they relate to each other.

---

## Table 1: EMPLOYEES

**Purpose:** Master table containing core employee information

### Columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `emp_no` | INT (Primary Key) | Unique employee identifier | 10001 |
| `birth_date` | DATE | Employee's date of birth | 1953-09-02 |
| `first_name` | VARCHAR(14) | Employee's first name | Georgi |
| `last_name` | VARCHAR(16) | Employee's last name | Facello |
| `gender` | ENUM('M','F') | Employee's gender | M |
| `hire_date` | DATE | Date employee was hired | 1986-06-26 |

### Key Characteristics:
- One row per employee (current or historical)
- `emp_no` is the primary key - uniquely identifies each employee
- Doesn't contain information about salary, department, or titles (stored in separate tables)

### Sample Data:
```sql
emp_no | birth_date | first_name | last_name | gender | hire_date
-------|------------|------------|-----------|--------|----------
10001  | 1953-09-02 | Georgi     | Facello   | M      | 1986-06-26
10002  | 1964-06-02 | Bezalel    | Simmel    | F      | 1985-11-21
10003  | 1959-12-03 | Parto      | Bamford   | M      | 1986-08-28
```

---

## Table 2: SALARIES (Historical Data)

**Purpose:** Tracks salary history for each employee

### Columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `emp_no` | INT (Foreign Key) | Employee ID | 10001 |
| `salary` | INT | Salary amount in dollars | 88958 |
| `from_date` | DATE | When this salary became effective | 1986-06-26 |
| `to_date` | DATE | When this salary ended | 1987-06-26 |

### Key Characteristics:
- **Multiple rows per employee** - Each salary change creates a new row
- `from_date` and `to_date` define the period when salary was active
- `to_date = 9999-01-01` typically means the record is currently active
- Composite key: (emp_no, from_date, to_date)

### Sample Data for Employee 10001:
```sql
emp_no | salary | from_date  | to_date
-------|--------|------------|------------
10001  | 60000  | 1986-06-26 | 1987-06-26
10001  | 65000  | 1987-06-26 | 1988-06-25
10001  | 71046  | 1988-06-25 | 1990-05-17
10001  | 75000  | 1990-05-17 | 1993-06-26
10001  | 88958  | 1993-06-26 | 9999-01-01  ← CURRENT
```

### Getting Latest Salary:
```sql
-- Wrong: Returns all historical salaries
SELECT salary FROM salaries WHERE emp_no = 10001;

-- Correct: Returns only current salary
SELECT salary FROM salaries 
WHERE emp_no = 10001 
AND to_date = (SELECT MAX(to_date) FROM salaries WHERE emp_no = 10001);
-- Result: 88958
```

---

## Table 3: DEPARTMENTS

**Purpose:** List of all departments in the company

### Columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `dept_no` | CHAR(4) (Primary Key) | Unique department identifier | d001 |
| `dept_name` | VARCHAR(40) | Department name | Sales |

### Key Characteristics:
- One row per department (no history tracking)
- `dept_no` is the primary key
- Small table with limited rows (typically 10-20 departments)
- Referenced by both `dept_emp` and used in reports

### Sample Data:
```sql
dept_no | dept_name
--------|------------------
d001    | Marketing
d002    | Finance
d003    | Human Resources
d004    | Production
d005    | Development
d006    | Quality Management
d007    | Sales
d008    | Research
d009    | Customer Service
```

---

## Table 4: DEPT_EMP (Department-Employee Mapping)

**Purpose:** Tracks which department each employee worked in (historical)

### Columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `emp_no` | INT (Foreign Key) | Employee ID | 10001 |
| `dept_no` | CHAR(4) (Foreign Key) | Department ID | d001 |
| `from_date` | DATE | When employee joined department | 1986-06-26 |
| `to_date` | DATE | When employee left department | 9999-01-01 |

### Key Characteristics:
- **Multiple rows per employee** - Each department transfer creates a new row
- Shows employee's career progression (department transfers)
- `to_date = 9999-01-01` means employee currently works in that department
- Composite key: (emp_no, dept_no, from_date, to_date)

### Sample Data for Employee 10001:
```sql
emp_no | dept_no | from_date  | to_date
-------|---------|------------|------------
10001  | d001    | 1986-06-26 | 1991-07-01
10001  | d004    | 1991-07-01 | 1995-12-15
10001  | d002    | 1995-12-15 | 9999-01-01  ← CURRENT
```

**Interpretation:** Employee 10001 started in d001, moved to d004, and now works in d002 (since 1995).

### Getting Current Department:
```sql
-- Find current department for employee 10001
SELECT dept_no FROM dept_emp
WHERE emp_no = 10001 
AND to_date = (SELECT MAX(to_date) FROM dept_emp WHERE emp_no = 10001);
-- Result: d002
```

---

## Table 5: TITLES (Job Title History)

**Purpose:** Tracks job title history for each employee

### Columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `emp_no` | INT (Foreign Key) | Employee ID | 10001 |
| `title` | VARCHAR(50) | Job title | Senior Engineer |
| `from_date` | DATE | When employee started this title | 1986-06-26 |
| `to_date` | DATE | When employee stopped this title | 1991-07-01 |

### Key Characteristics:
- **Multiple rows per employee** - Each title change creates a new row
- Shows employee's promotion/career progression
- `to_date = 9999-01-01` means employee currently holds that title
- Composite key: (emp_no, title, from_date, to_date)

### Sample Data for Employee 10001:
```sql
emp_no | title            | from_date  | to_date
-------|------------------|------------|------------
10001  | Engineer         | 1986-06-26 | 1995-12-15
10001  | Senior Engineer  | 1995-12-15 | 2001-09-09
10001  | Staff            | 2001-09-09 | 2003-12-09
10001  | Senior Staff     | 2003-12-09 | 9999-01-01  ← CURRENT
```

### Getting Current Title:
```sql
-- Find current title for employee 10001
SELECT title FROM titles
WHERE emp_no = 10001 
AND to_date = (SELECT MAX(to_date) FROM titles WHERE emp_no = 10001);
-- Result: Senior Staff
```

---

## Relationships Diagram

```
┌──────────────────┐
│   EMPLOYEES      │
│   (emp_no)       │
└────────┬─────────┘
         │ (emp_no)
         ├──→ SALARIES (salary history)
         ├──→ DEPT_EMP (dept_no) ──→ DEPARTMENTS
         └──→ TITLES (title history)
```

### How They Connect:

1. **EMPLOYEES → SALARIES**
   - Link: `emp_no`
   - Purpose: Find all salary records for an employee
   - Relationship: One employee has many salary records

2. **EMPLOYEES → DEPT_EMP**
   - Link: `emp_no`
   - Purpose: Find all department assignments for an employee
   - Relationship: One employee has many department records

3. **DEPT_EMP → DEPARTMENTS**
   - Link: `dept_no`
   - Purpose: Find department name from department ID
   - Relationship: One department code has one department name

4. **EMPLOYEES → TITLES**
   - Link: `emp_no`
   - Purpose: Find all job titles an employee has held
   - Relationship: One employee has many title records

---

## Understanding Historical Data

### Key Concept: The `to_date` Field

Most tables have a `to_date` column. Two possible values:

| to_date | Meaning | Example | Still Active? |
|---------|---------|---------|--------------|
| `9999-01-01` | Record is CURRENT | Employee still has this salary | YES |
| Specific date | Record is HISTORICAL | Employee had this salary until that date | NO |

### Why This Pattern?

In real databases, companies want to track history:
- "What was John's salary in 2020?" → Look for record where from_date ≤ 2020 and to_date ≥ 2020
- "What is John's current salary?" → Look for record where to_date = 9999-01-01

### The `to_date = 9999-01-01` Convention

Using date 9999-01-01 (far future) means:
- ✅ Easy to find "current" records: WHERE to_date = 9999-01-01
- ✅ Easy to find "historical" records: WHERE to_date < 9999-01-01
- ✅ All dates are real dates (no NULL values)
- ✅ Range queries work naturally

---

## Important Queries for Understanding

### Find All History for One Employee:

```sql
-- All salaries for employee 10001
SELECT * FROM salaries WHERE emp_no = 10001 
ORDER BY to_date;

-- All departments for employee 10001
SELECT * FROM dept_emp WHERE emp_no = 10001 
ORDER BY to_date;

-- All titles for employee 10001
SELECT * FROM titles WHERE emp_no = 10001 
ORDER BY to_date;
```

### Find Current State for One Employee:

```sql
-- Current salary
SELECT salary FROM salaries 
WHERE emp_no = 10001 AND to_date = 9999-01-01;

-- Current department
SELECT dept_no FROM dept_emp 
WHERE emp_no = 10001 AND to_date = 9999-01-01;

-- Current title
SELECT title FROM titles 
WHERE emp_no = 10001 AND to_date = 9999-01-01;
```

### Count How Many Records Per Employee:

```sql
-- How many salary changes?
SELECT emp_no, COUNT(*) AS salary_changes
FROM salaries
WHERE emp_no = 10001;

-- How many department transfers?
SELECT emp_no, COUNT(*) AS dept_transfers
FROM dept_emp
WHERE emp_no = 10001 AND to_date < 9999-01-01;

-- How many promotions?
SELECT emp_no, COUNT(*) AS promotions
FROM titles
WHERE emp_no = 10001 AND to_date < 9999-01-01;
```

---

## Data Statistics

Typical employee database contains:

| Table | Typical Row Count | Notes |
|-------|-------------------|-------|
| employees | ~300,000 | All current and historical employees |
| salaries | ~2,800,000 | Multiple records per employee (salary changes) |
| departments | ~12 | Static list |
| dept_emp | ~1,600,000 | Multiple records per employee (dept changes) |
| titles | ~440,000 | Multiple records per employee (title changes) |

---

## Common SQL Pattern: Getting Latest Record

Whenever you see a table with `from_date` and `to_date`, use this pattern:

```sql
JOIN [table] [alias]
    ON [main_table].emp_no = [alias].emp_no
    AND [alias].to_date = (
        SELECT MAX(to_date)
        FROM [table] [alias2]
        WHERE [alias2].emp_no = [main_table].emp_no
    )
```

This ensures you get ONLY the latest record, not all historical ones!

---

## Practice Queries

Test your understanding with these queries:

```sql
-- Q1: How many employees are in the database?
SELECT COUNT(*) FROM employees;

-- Q2: How many times has employee 10001 changed departments?
SELECT COUNT(*) FROM dept_emp WHERE emp_no = 10001;

-- Q3: What was employee 10001's first title?
SELECT title FROM titles WHERE emp_no = 10001 ORDER BY from_date LIMIT 1;

-- Q4: What's the average current salary?
SELECT AVG(s.salary) 
FROM salaries s
WHERE s.to_date = 9999-01-01;

-- Q5: Which department has the most employees?
SELECT d.dept_name, COUNT(de.emp_no) as emp_count
FROM dept_emp de
JOIN departments d ON de.dept_no = d.dept_no
WHERE de.to_date = 9999-01-01
GROUP BY d.dept_no, d.dept_name
ORDER BY emp_count DESC;
```

---

This schema is a great learning example because it demonstrates real-world database design: historical tracking, referential integrity, and complex queries across multiple tables!
