-- ============================================================================
-- PRACTICE QUERIES - Learning Steps
-- ============================================================================
-- 
-- Follow these steps to understand the assignment query.
-- Test each step by running it in your MySQL client.
-- Build your understanding progressively.
--
-- ============================================================================

-- STEP 1: Select basic employee information
-- PURPOSE: Understand the employees table
-- ============================================================================

SELECT 
    emp_no, 
    first_name, 
    last_name, 
    hire_date, 
    birth_date
FROM employees
LIMIT 5;

-- Expected: Shows 5 employees with basic info


-- ============================================================================
-- STEP 2: Concatenate names
-- PURPOSE: Learn CONCAT function
-- ============================================================================

SELECT 
    emp_no,
    CONCAT(first_name, ' ', last_name) AS full_name,
    hire_date,
    birth_date
FROM employees
LIMIT 5;

-- Expected: Shows employees with combined first and last names


-- ============================================================================
-- STEP 3: Calculate age
-- PURPOSE: Learn TIMESTAMPDIFF function
-- ============================================================================

SELECT 
    emp_no,
    CONCAT(first_name, ' ', last_name) AS full_name,
    birth_date,
    TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS age
FROM employees
LIMIT 5;

-- Expected: Shows age in complete years


-- ============================================================================
-- STEP 4: Calculate years of experience
-- PURPOSE: Use TIMESTAMPDIFF with hire_date
-- ============================================================================

SELECT 
    emp_no,
    CONCAT(first_name, ' ', last_name) AS full_name,
    hire_date,
    TIMESTAMPDIFF(YEAR, hire_date, CURDATE()) AS years_of_exp
FROM employees
LIMIT 5;

-- Expected: Shows years since hired


-- ============================================================================
-- STEP 5: Explore salaries table
-- PURPOSE: Understand historical data
-- ============================================================================

-- See how many salary records one employee has
SELECT emp_no, salary, from_date, to_date
FROM salaries
WHERE emp_no = 10001
ORDER BY to_date DESC;

-- Expected: Multiple salary records for employee 10001


-- ============================================================================
-- STEP 6: Get latest salary with subquery
-- PURPOSE: Learn to filter for "latest" records
-- ============================================================================

SELECT salary
FROM salaries
WHERE emp_no = 10001
AND to_date = (
    SELECT MAX(to_date)
    FROM salaries
    WHERE emp_no = 10001
);

-- Expected: Shows only one salary (the latest for emp_no 10001)


-- ============================================================================
-- STEP 7: Join employees and salaries
-- PURPOSE: Combine employee names with salaries
-- ============================================================================

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

-- Expected: Employee names with their latest salary (one per employee)


-- ============================================================================
-- STEP 8: Add department information
-- PURPOSE: Learn secondary joins
-- ============================================================================

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

-- Expected: Shows department names (two joins added)


-- ============================================================================
-- STEP 9: Add job title
-- PURPOSE: Complete the integration
-- ============================================================================

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

-- Expected: Complete query with all 5 columns


-- ============================================================================
-- STEP 10: Add date calculations
-- PURPOSE: Complete the assignment query
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

-- Expected: All 7 columns with complete data
-- This is the FINAL QUERY!

-- ============================================================================
-- TESTING TIPS
-- ============================================================================
--
-- 1. Run each step independently
-- 2. Start with LIMIT 5 to see results quickly
-- 3. Remove LIMIT once you understand the step
-- 4. If a step fails, check the error message
-- 5. Compare your results to expected output in outputs/expected_output.csv
--
-- ============================================================================
