-- ============================================================================
-- MAIN ASSIGNMENT QUERY
-- ============================================================================
-- 
-- TASK: Complete this query to retrieve comprehensive employee information
-- 
-- REQUIREMENTS:
-- - Retrieve all employees with their current information
-- - Include 7 specific columns (see below)
-- - Use JOINs to combine data from 5 tables
-- - Use subqueries to get latest records
-- - Use date functions for calculations
--
-- EXPECTED COLUMNS:
-- 1. emp_no          - Employee ID
-- 2. full_name       - Concatenated first and last name
-- 3. latest_salary   - Current salary
-- 4. recent_department - Current department name
-- 5. max_title       - Current job title
-- 6. years_of_exp    - Years since hire date
-- 7. age             - Current age
--
-- TABLES TO USE:
-- - employees (e)
-- - salaries (s)
-- - dept_emp (de)
-- - departments (d)
-- - titles (t)
--
-- ============================================================================

SELECT 
    e.emp_no,
    CONCAT(e.first_name, ' ', e.last_name) AS full_name,
    s.salary AS latest_salary,
    d.dept_name AS recent_department,
    t.title AS max_title,
    TIMESTAMPDIFF(YEAR, e.hire_date, CURDATE()) AS years_of_exp,
    TIMESTAMPDIFF(YEAR, e.birth_date, CURDATE()) AS age

FROM employees e

-- TODO: Add JOIN to salaries table
-- HINT: Use subquery to get latest salary (s.to_date = MAX(s.to_date))
-- JOIN salaries s 
--     ON e.emp_no = s.emp_no 
--     AND s.to_date = (
--         SELECT MAX(s2.to_date) FROM salaries s2 WHERE s2.emp_no = e.emp_no
--     )

-- TODO: Add JOIN to dept_emp table
-- HINT: Use subquery to get latest department assignment
-- JOIN dept_emp de 
--     ON e.emp_no = de.emp_no 
--     AND de.to_date = (
--         SELECT MAX(de2.to_date) FROM dept_emp de2 WHERE de2.emp_no = e.emp_no
--     )

-- TODO: Add JOIN to departments table
-- HINT: Simple join, no subquery needed
-- JOIN departments d ON de.dept_no = d.dept_no

-- TODO: Add JOIN to titles table
-- HINT: Use subquery to get latest title
-- JOIN titles t 
--     ON e.emp_no = t.emp_no 
--     AND t.to_date = (
--         SELECT MAX(t2.to_date) FROM titles t2 WHERE t2.emp_no = e.emp_no
--     );

-- ============================================================================
-- HELPFUL NOTES:
-- ============================================================================
-- 
-- 1. TABLE ALIASES:
--    Use single letters for clarity: e (employees), s (salaries), 
--    d (departments), de (dept_emp), t (titles)
--
-- 2. SUBQUERIES:
--    You need 3 subqueries (one each for salaries, dept_emp, titles)
--    Each finds MAX(to_date) for the current employee
--    Use different aliases in subqueries: s2, de2, t2
--
-- 3. LATEST RECORDS:
--    Historical tables (salaries, dept_emp, titles) have multiple rows per employee
--    Use MAX(to_date) subquery to get ONLY the latest record
--
-- 4. DATE CALCULATIONS:
--    TIMESTAMPDIFF(YEAR, start_date, end_date) = years between dates
--    CURDATE() = today's date
--
-- 5. STRING CONCATENATION:
--    CONCAT(first_name, ' ', last_name) = "John Doe"
--    The ' ' (space) goes between first and last name
--
-- ============================================================================
-- 
-- EXPECTED OUTPUT (First 3 rows):
-- emp_no | full_name          | latest_salary | recent_department | max_title        | years_of_exp | age
-- -------|--------------------|-----------|--------------------|------|------------|-----
-- 10001  | Georgi Facello     | 88958     | Finance            | Senior Staff     | 37           | 70
-- 10002  | Bezalel Simmel     | 72527     | Sales              | Senior Engineer  | 38           | 71
-- 10003  | Parto Bamford      | 43311     | Production         | Senior Engineer  | 37           | 70
--
-- ============================================================================
