-- ============================================================================
-- Employee Database Assignment - Complete Solution
-- ============================================================================
-- 
-- This query retrieves a comprehensive snapshot of employee information,
-- including current salary, department, job title, experience, and age.
--
-- Key concepts demonstrated:
-- 1. Multiple JOINs to combine data from 5 different tables
-- 2. Correlated subqueries to retrieve "latest" records
-- 3. Date/time functions for calculated fields
-- 4. String concatenation for better readability
--
-- ============================================================================

SELECT 
    -- Employee identification
    e.emp_no,
    
    -- Full name created by concatenating first and last name
    CONCAT(e.first_name, ' ', e.last_name) AS full_name,

    -- Latest Salary: Most recent salary record for the employee
    s.salary AS latest_salary,

    -- Recent Department: Employee's current department assignment
    d.dept_name AS recent_department,

    -- Latest Title: Most recent job title held by employee
    t.title AS max_title,

    -- Years of Experience: Calculated from hire date until today
    TIMESTAMPDIFF(YEAR, e.hire_date, CURDATE()) AS years_of_exp,

    -- Age: Calculated from birth date until today
    TIMESTAMPDIFF(YEAR, e.birth_date, CURDATE()) AS age

FROM employees e

-- ============================================================================
-- JOIN 1: SALARIES TABLE
-- Purpose: Get the latest salary for each employee
-- ============================================================================
-- Condition: Match employee AND get ONLY the record with the maximum to_date
-- The subquery ensures we get the most recent salary entry
JOIN salaries s 
    ON e.emp_no = s.emp_no 
    AND s.to_date = (
        -- Subquery: Find the maximum (latest) to_date for this employee
        SELECT MAX(s2.to_date)
        FROM salaries s2
        WHERE s2.emp_no = e.emp_no
    )

-- ============================================================================
-- JOIN 2: DEPT_EMP TABLE (Department-Employee mapping)
-- Purpose: Get the latest department assignment for each employee
-- ============================================================================
-- Condition: Match employee AND get ONLY the record with the maximum to_date
-- This tells us which department the employee currently belongs to
JOIN dept_emp de 
    ON e.emp_no = de.emp_no 
    AND de.to_date = (
        -- Subquery: Find the maximum (latest) to_date for this employee-dept mapping
        SELECT MAX(de2.to_date)
        FROM dept_emp de2
        WHERE de2.emp_no = e.emp_no
    )

-- ============================================================================
-- JOIN 3: DEPARTMENTS TABLE
-- Purpose: Get the department name from department ID
-- ============================================================================
-- Condition: Match the department number from dept_emp to departments table
-- This gives us the readable department name instead of just dept_no
JOIN departments d 
    ON de.dept_no = d.dept_no

-- ============================================================================
-- JOIN 4: TITLES TABLE
-- Purpose: Get the latest job title for each employee
-- ============================================================================
-- Condition: Match employee AND get ONLY the record with the maximum to_date
-- The subquery ensures we get the most recent title entry
JOIN titles t 
    ON e.emp_no = t.emp_no 
    AND t.to_date = (
        -- Subquery: Find the maximum (latest) to_date for this employee's titles
        SELECT MAX(t2.to_date)
        FROM titles t2
        WHERE t2.emp_no = e.emp_no
    );

-- ============================================================================
-- EXPLANATION OF KEY TECHNIQUES
-- ============================================================================
--
-- TECHNIQUE 1: Using Subqueries for "Latest" Records
-- ─────────────────────────────────────────────────────
-- The employee database stores historical data. Each table (salaries, dept_emp, 
-- titles) has multiple records per employee showing their history.
--
-- To get ONLY the latest record, we use:
--   AND [table].to_date = (SELECT MAX([table2].to_date) FROM [table2] WHERE ...)
--
-- This ensures we match only the record with the maximum to_date, which 
-- represents the most recent entry.
--
--
-- TECHNIQUE 2: Table Aliases in Subqueries
-- ──────────────────────────────────────────
-- Important: Use different aliases for the outer and inner table references.
-- Example for titles:
--   JOIN titles t ON ... AND t.to_date = (SELECT MAX(t2.to_date) FROM titles t2 ...)
--
-- The 't' refers to the outer query, and 't2' refers to the subquery.
-- This prevents confusion and ensures correct correlation.
--
--
-- TECHNIQUE 3: CONCAT() for String Concatenation
-- ────────────────────────────────────────────────
-- CONCAT(e.first_name, ' ', e.last_name) combines multiple fields.
-- The space ' ' in the middle creates readable full names.
-- Result: "Georgi Facello" instead of "Georgi" and "Facello" separately.
--
--
-- TECHNIQUE 4: TIMESTAMPDIFF() for Date Calculations
-- ───────────────────────────────────────────────────
-- TIMESTAMPDIFF(YEAR, start_date, end_date) calculates complete years between dates.
--
-- For years of experience:
--   TIMESTAMPDIFF(YEAR, e.hire_date, CURDATE())
--   Returns: Years from hire date until today
--
-- For age:
--   TIMESTAMPDIFF(YEAR, e.birth_date, CURDATE())
--   Returns: Years from birth date until today
--
-- CURDATE() returns today's date in YYYY-MM-DD format.
--
-- ============================================================================
-- SAMPLE OUTPUT
-- ============================================================================
--
-- emp_no | full_name         | latest_salary | recent_department | max_title        | years_of_exp | age
-- -------|-------------------|---------------|-------------------|------------------|--------------|------
-- 10001  | Georgi Facello    | 88958         | Finance           | Senior Engineer  | 33           | 63
-- 10002  | Bezalel Simmel    | 72527         | Sales             | Senior Staff     | 33           | 64
-- 10003  | Parto Bamford     | 43311         | Production        | Senior Engineer  | 33           | 65
-- 10004  | Chirstian Koblick | 74612         | Production        | Technique Lead   | 33           | 62
-- 10005  | Kyoichi Maliniak  | 94692         | Human Resources   | Senior Engineer  | 33           | 61
--
-- ============================================================================
