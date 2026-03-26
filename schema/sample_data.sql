-- ============================================================================
-- Sample Data Reference
-- ============================================================================
-- NOTE: This is for reference only.
-- Your MySQL database already contains this data.
-- Do NOT run these INSERT statements unless you're recreating the database.
--
-- These are examples of what the data looks like.
-- ============================================================================

-- Sample EMPLOYEES data:
-- emp_no | birth_date | first_name | last_name  | gender | hire_date
-- -------|------------|-----------|-----------|--------|----------
-- 10001  | 1953-09-02 | Georgi    | Facello   | M      | 1986-06-26
-- 10002  | 1964-06-02 | Bezalel   | Simmel    | F      | 1985-11-21
-- 10003  | 1959-12-03 | Parto     | Bamford   | M      | 1986-08-28

-- Sample SALARIES data (showing history for emp_no 10001):
-- emp_no | salary | from_date  | to_date
-- -------|--------|------------|------------
-- 10001  | 60000  | 1986-06-26 | 1987-06-26
-- 10001  | 65000  | 1987-06-26 | 1988-06-25
-- 10001  | 71046  | 1988-06-25 | 1990-05-17
-- 10001  | 75000  | 1990-05-17 | 1993-06-26
-- 10001  | 88958  | 1993-06-26 | 9999-01-01  ← CURRENT

-- Sample DEPARTMENTS data:
-- dept_no | dept_name
-- --------|------------------
-- d001    | Marketing
-- d002    | Finance
-- d003    | Human Resources
-- d004    | Production
-- d005    | Development
-- ...

-- Sample DEPT_EMP data (for emp_no 10001):
-- emp_no | dept_no | from_date  | to_date
-- -------|---------|------------|------------
-- 10001  | d001    | 1986-06-26 | 1991-07-01
-- 10001  | d004    | 1991-07-01 | 1995-12-15
-- 10001  | d002    | 1995-12-15 | 9999-01-01  ← CURRENT

-- Sample TITLES data (for emp_no 10001):
-- emp_no | title            | from_date  | to_date
-- -------|------------------|------------|------------
-- 10001  | Engineer         | 1986-06-26 | 1995-12-15
-- 10001  | Senior Engineer  | 1995-12-15 | 2001-09-09
-- 10001  | Staff            | 2001-09-09 | 2003-12-09
-- 10001  | Senior Staff     | 2003-12-09 | 9999-01-01  ← CURRENT

-- ============================================================================
-- Data Statistics
-- ============================================================================
-- employees:  ~300,000 rows
-- salaries:   ~2,800,000 rows (multiple per employee)
-- departments: ~10 rows
-- dept_emp:   ~1,600,000 rows (multiple per employee)
-- titles:     ~440,000 rows (multiple per employee)
-- ============================================================================
