-- ============================================================================
-- Employee Database Schema
-- ============================================================================
-- This file defines the 5 core tables used in the assignment.
-- Database: employee_db (or equivalent on your MySQL server)
--
-- NOTE: These tables already exist in your MySQL database.
-- This file is for reference only to understand the structure.
-- ============================================================================

-- TABLE 1: EMPLOYEES
-- Master table with core employee information
-- One row per employee

CREATE TABLE employees (
    emp_no INT PRIMARY KEY,
    birth_date DATE NOT NULL,
    first_name VARCHAR(14) NOT NULL,
    last_name VARCHAR(16) NOT NULL,
    gender ENUM('M','F') NOT NULL,
    hire_date DATE NOT NULL
);

-- ============================================================================
-- TABLE 2: SALARIES (Historical - Multiple rows per employee)
-- Tracks salary changes over time

CREATE TABLE salaries (
    emp_no INT NOT NULL,
    salary INT NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    PRIMARY KEY (emp_no, from_date),
    FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
);

-- ============================================================================
-- TABLE 3: DEPARTMENTS
-- List of all departments (small reference table)

CREATE TABLE departments (
    dept_no CHAR(4) PRIMARY KEY,
    dept_name VARCHAR(40) NOT NULL
);

-- ============================================================================
-- TABLE 4: DEPT_EMP (Historical - Multiple rows per employee)
-- Maps employees to departments over time

CREATE TABLE dept_emp (
    emp_no INT NOT NULL,
    dept_no CHAR(4) NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    PRIMARY KEY (emp_no, dept_no, from_date),
    FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
    FOREIGN KEY (dept_no) REFERENCES departments(dept_no)
);

-- ============================================================================
-- TABLE 5: TITLES (Historical - Multiple rows per employee)
-- Tracks job title changes over time

CREATE TABLE titles (
    emp_no INT NOT NULL,
    title VARCHAR(50) NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    PRIMARY KEY (emp_no, title, from_date),
    FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
);

-- ============================================================================
-- KEY CONCEPTS
-- ============================================================================
--
-- HISTORICAL DATA:
-- Each of the 4 tables (salaries, dept_emp, titles, and to some extent employees)
-- contains historical data. Records have from_date and to_date fields.
--
-- CURRENT vs HISTORICAL:
-- - to_date = 9999-01-01   → Record is currently active
-- - to_date = past date    → Record is historical
--
-- GETTING LATEST RECORDS:
-- Use subqueries with MAX(to_date) to filter for current records only.
--
-- RELATIONSHIPS:
-- employees → salaries (emp_no)
-- employees → dept_emp (emp_no)
-- dept_emp → departments (dept_no)
-- employees → titles (emp_no)
--
-- ============================================================================

-- USEFUL QUERIES TO UNDERSTAND THE DATA:

-- Count employees
-- SELECT COUNT(DISTINCT emp_no) FROM employees;

-- Check salary history for one employee
-- SELECT * FROM salaries WHERE emp_no = 10001 ORDER BY to_date;

-- Get latest salary for one employee
-- SELECT salary FROM salaries 
-- WHERE emp_no = 10001 AND to_date = (SELECT MAX(to_date) FROM salaries WHERE emp_no = 10001);

-- Check department assignment history
-- SELECT * FROM dept_emp WHERE emp_no = 10001 ORDER BY to_date;

-- Check current employees in Marketing
-- SELECT e.emp_no, e.first_name, e.last_name, d.dept_name
-- FROM employees e
-- JOIN dept_emp de ON e.emp_no = de.emp_no
-- JOIN departments d ON de.dept_no = d.dept_no
-- WHERE d.dept_name = 'Marketing' AND de.to_date = 9999-01-01;
