# Employee Database SQL Assignment

## 📋 Overview

This assignment teaches advanced SQL concepts using a real-world employee database scenario. You'll master JOINs, subqueries, date calculations, and string manipulation by writing a comprehensive query that retrieves employee information from multiple tables.

**Difficulty:** Intermediate | **Time:** 2-4 hours | **Skills:** Advanced SQL

---

## 🗂️ Project Structure

```
employee_sql_assignment/
│
├── README.md                          (This file)
│
├── schema/
│   ├── create_tables.sql              (Table definitions)
│   └── sample_data.sql                (Test data - optional reference)
│
├── queries/
│   ├── main_query.sql                 (Your task)
│   └── practice_queries.sql           (Learning steps)
│
├── outputs/
│   └── expected_output.csv            (Expected results)
│
├── docs/
│   ├── problem_statement.md           (Assignment objectives)
│   ├── explanation.md                 (Concept explanations)
│   └── test_cases.md                  (Validation checklist)
│
└── screenshots/
    └── result.png                     (Example output)
```

---

## 🚀 Quick Start

### 1. **Understand the Problem**
Read [docs/problem_statement.md](docs/problem_statement.md)

### 2. **Review the Schema**
Check [schema/create_tables.sql](schema/create_tables.sql) to understand the database structure

### 3. **Work Through Learning Steps**
Follow [queries/practice_queries.sql](queries/practice_queries.sql) incrementally

### 4. **Implement the Main Query**
Complete [queries/main_query.sql](queries/main_query.sql)

### 5. **Verify Your Results**
Compare output against [outputs/expected_output.csv](outputs/expected_output.csv)

### 6. **Deep Dive (Optional)**
Read [docs/explanation.md](docs/explanation.md) for concept explanations

---

## 📖 Documentation

| File | Purpose |
|------|---------|
| [docs/problem_statement.md](docs/problem_statement.md) | Complete assignment objectives and requirements |
| [docs/explanation.md](docs/explanation.md) | Deep technical explanations of SQL concepts |
| [docs/test_cases.md](docs/test_cases.md) | How to validate your solution |

---

## 💻 SQL Files

| File | Purpose |
|------|---------|
| [schema/create_tables.sql](schema/create_tables.sql) | CREATE TABLE statements for all 5 tables |
| [schema/sample_data.sql](schema/sample_data.sql) | INSERT statements (reference only) |
| [queries/practice_queries.sql](queries/practice_queries.sql) | Step-by-step learning queries |
| [queries/main_query.sql](queries/main_query.sql) | Your assignment task |

---

## ✅ Assignment Task

Write a SQL query that retrieves comprehensive employee information including:

- Employee ID & Full Name
- Current Salary
- Current Department
- Current Job Title
- Years of Experience
- Age

**Required Tables:** employees, salaries, departments, dept_emp, titles

**Key Concepts:** JOINs, Subqueries, Date Functions, String Concatenation

---

## 🎯 Learning Objectives

After completing this assignment, you will:

✅ Write complex queries with 4+ table JOINs
✅ Use subqueries for advanced filtering
✅ Handle historical/temporal data
✅ Calculate derived fields (age, experience)
✅ Write professional, documented code

---

## 📊 Expected Output

Your query should return results like:

```
emp_no | full_name       | latest_salary | recent_department | max_title       | years_of_exp | age
-------|-----------------|---------------|-------------------|-----------------|--------------|-----
10001  | Georgi Facello  | 88958         | Finance           | Senior Engineer | 37           | 70
10002  | Bezalel Simmel  | 72527         | Sales             | Senior Staff    | 38           | 71
```

See [outputs/expected_output.csv](outputs/expected_output.csv) for complete sample

---

## 🔍 Validation

Use [docs/test_cases.md](docs/test_cases.md) to verify your solution:

- [ ] All 7 columns present
- [ ] One row per employee
- [ ] Correct data types
- [ ] No NULL values
- [ ] Calculations accurate

---

## 📚 Learning Path

### Beginner
1. Read: problem_statement.md
2. Study: schema/create_tables.sql (understand tables)
3. Follow: queries/practice_queries.sql (steps 1-8)
4. Implement: queries/main_query.sql
5. Verify: outputs/expected_output.csv
6. Learn: docs/explanation.md

### Intermediate
1. Review: problem_statement.md (5 min)
2. Quick check: schema/create_tables.sql (2 min)
3. Implement: queries/main_query.sql (30-60 min)
4. Verify: outputs/expected_output.csv

### Advanced
1. Skim: problem_statement.md (2 min)
2. Implement: queries/main_query.sql (20-30 min)
3. Compare: docs/explanation.md (5 min)

---

## 🆘 Getting Help

**Stuck on the query?**
→ Follow [queries/practice_queries.sql](queries/practice_queries.sql) step by step

**Don't understand why something works?**
→ Read [docs/explanation.md](docs/explanation.md)

**Need to debug?**
→ Check [docs/test_cases.md](docs/test_cases.md) for debugging queries

**Wrong results?**
→ Compare against [outputs/expected_output.csv](outputs/expected_output.csv)

---

## 🏆 Submission Checklist

Before submitting:

- [ ] Query runs without errors
- [ ] All 7 required columns present
- [ ] One row per employee
- [ ] Results match expected output format
- [ ] Code includes comments
- [ ] Explanation document completed

---

## 📞 Files Quick Reference

| Need | File |
|------|------|
| Assignment goal | [docs/problem_statement.md](docs/problem_statement.md) |
| Understand tables | [schema/create_tables.sql](schema/create_tables.sql) |
| Learn step-by-step | [queries/practice_queries.sql](queries/practice_queries.sql) |
| Your task | [queries/main_query.sql](queries/main_query.sql) |
| Check results | [outputs/expected_output.csv](outputs/expected_output.csv) |
| Understand concepts | [docs/explanation.md](docs/explanation.md) |
| Validate solution | [docs/test_cases.md](docs/test_cases.md) |

---

## 💡 Key SQL Concepts

This assignment teaches:

- **Multiple JOINs** - Combining 4+ tables
- **Subqueries** - Filtering for latest records
- **TIMESTAMPDIFF()** - Date calculations
- **CONCAT()** - String concatenation
- **Table Aliases** - Code organization
- **Historical Data** - Temporal patterns

---

**Status:** Ready to use
**Database:** MySQL (existing connection)
**Last Updated:** March 2026

Good luck! Start with [docs/problem_statement.md](docs/problem_statement.md) 🚀
