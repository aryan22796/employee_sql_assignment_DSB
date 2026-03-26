# Employee Database Assignment - Problem Statement

## Overview
In this assignment, you will work with the **Employee Database** to retrieve comprehensive employee information including current salary, department, title, experience, and age. This exercise will help you master advanced SQL concepts including JOINs, subqueries, and date/time functions.

---

## Learning Objectives

By completing this assignment, you will learn to:

✅ **Master Multiple JOINs** - Combine data from multiple tables (employees, salaries, departments, titles, dept_emp)

✅ **Use Subqueries Effectively** - Filter records based on maximum values within subqueries

✅ **Apply Date/Time Functions** - Use `TIMESTAMPDIFF()` to calculate years of experience and age

✅ **Handle Historical Data** - Navigate temporal data where records have `to_date` fields

✅ **Concatenate Strings** - Combine first and last names using `CONCAT()`

✅ **Optimize Queries** - Understand how to fetch the latest records from historical data

---

## Database Context

### Tables Involved

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| **employees** | Employee master data | `emp_no`, `first_name`, `last_name`, `hire_date`, `birth_date` |
| **salaries** | Historical salary records | `emp_no`, `salary`, `from_date`, `to_date` |
| **departments** | List of departments | `dept_no`, `dept_name` |
| **dept_emp** | Department assignments (historical) | `emp_no`, `dept_no`, `from_date`, `to_date` |
| **titles** | Job title history | `emp_no`, `title`, `from_date`, `to_date` |

**Important Note:** The `to_date` field indicates when a record was last applicable. A value of `9999-01-01` typically means the record is currently active.

---

## Assignment Task

### Objective
Write a SQL query to retrieve a comprehensive snapshot of each employee's current information, including:

### Required Output Columns

1. **emp_no** - Employee ID number
2. **full_name** - Concatenated first and last name
3. **latest_salary** - Current/most recent salary
4. **recent_department** - Current/most recent department
5. **max_title** - Current/most recent job title
6. **years_of_exp** - Years since hire date until today
7. **age** - Years since birth date until today

---

## Key Concepts to Master

### 1. **Joining Tables**
- Use INNER JOINs to connect related tables
- Join condition must match employee IDs
- Handle multiple conditions for multiple JOINs

### 2. **Getting Latest Records**
- Subqueries find the maximum `to_date` for each employee in each table
- Correlated subqueries match the outer query's employee
- Example: `AND s.to_date = (SELECT MAX(s2.to_date) FROM salaries s2 WHERE s2.emp_no = e.emp_no)`

### 3. **Date/Time Calculations**
- `TIMESTAMPDIFF(YEAR, start_date, end_date)` calculates years between dates
- `CURDATE()` returns today's date
- Apply to both hire date (for experience) and birth date (for age)

### 4. **String Concatenation**
- `CONCAT(first_name, ' ', last_name)` combines fields with a space separator
- Improves readability of output

---

## Expected Output Format

Your query should return results similar to this:

| emp_no | full_name | latest_salary | recent_department | max_title | years_of_exp | age |
|--------|-----------|----------------|-------------------|-----------|--------------|-----|
| 10001 | Georgi Facello | 88958 | Finance | Senior Engineer | 33 | 63 |
| 10002 | Bezalel Simmel | 72527 | Sales | Senior Staff | 33 | 64 |
| 10003 | Parto Bamford | 43311 | Production | Senior Engineer | 33 | 65 |

---

## Submission Requirements

Your submission should include:

1. **SQL Query File** - Save your query as `solution.sql`
   - Include comments explaining each JOIN
   - Add comments for subqueries
   - Document the purpose of date calculations

2. **Explanation Document** - Create `EXPLANATION.md`
   - Explain why each JOIN is necessary
   - Describe how subqueries filter for "latest" records
   - Give examples of the business logic

3. **Test Results** - Save first 10 rows of output as `sample_output.txt`

---

## Challenges & Edge Cases

### Challenge 1: Handling Multiple Historical Records
- Some employees may have many salary or title changes
- Your subquery must return ONLY the latest one
- What happens if you forget the MAX() subquery condition?

### Challenge 2: Date Calculations
- Some employees may have birth dates that make age calculation tricky
- Some hire dates may be far in the past
- Ensure CURDATE() is used for consistent results

### Challenge 3: NULL Values
- What if an employee has no salary? No department? What will happen?
- Test with INNER vs LEFT JOINs

### Challenge 4: Performance Considerations
- This query runs 5 subqueries - can it be optimized?
- What if the database has 100,000+ employees?
- How would you add an INDEX to improve performance?

---

## Tips for Success

1. **Start Simple** - First, just SELECT from the `employees` table
2. **Add Joins Incrementally** - Add one table join at a time
3. **Test Subqueries** - Test each subquery independently first
4. **Check Data Types** - Verify your date calculations are returning numbers
5. **Verify Results** - Run simple SELECT queries to validate your joins
6. **Use Aliases** - Use table aliases (e.g., `s` for salaries) for clarity

---

## Resources

- [MySQL CONCAT() Documentation](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_concat)
- [MySQL TIMESTAMPDIFF() Documentation](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timestampdiff)
- [MySQL JOIN Types](https://dev.mysql.com/doc/refman/8.0/en/join.html)
- [MySQL Subqueries](https://dev.mysql.com/doc/refman/8.0/en/subqueries.html)

---

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| Query returns all required columns | 20 |
| Correct use of all 5 JOINs | 20 |
| Latest records retrieved correctly | 20 |
| Date calculations accurate | 15 |
| Code clarity and comments | 15 |
| Explanation document complete | 10 |
| **Total** | **100** |

---

## Questions to Consider

As you work through this assignment, think about:

1. Why do we need subqueries to get the "latest" record?
2. What would happen if we used LEFT JOIN instead of INNER JOIN?
3. How would you modify the query to filter for employees hired in a specific year?
4. Can you add salary ranges or age groups to the output?
5. How would you calculate total years at each level (salary, department, title)?

---

**Good luck! Feel free to reference the sample solution if you get stuck, but try to solve it first on your own.**
