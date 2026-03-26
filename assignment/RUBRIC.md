# Assignment Rubric & Grading Guide

## Total Points: 100

### Component Breakdown

---

## 1. Query Correctness (40 points)

### All Required Columns Present (10 points)
- [ ] emp_no ✓
- [ ] full_name ✓
- [ ] latest_salary ✓
- [ ] recent_department ✓
- [ ] max_title ✓
- [ ] years_of_exp ✓
- [ ] age ✓

**Scoring:**
- 10/10: All 7 columns present and correctly named
- 5/10: Missing 1-2 columns
- 0/10: Missing 3+ columns

---

### Data Accuracy (15 points)

#### emp_no and full_name (5 points)
- [ ] emp_no matches actual employee IDs
- [ ] full_name is readable concatenation of first and last name
- [ ] No extra spaces or formatting issues

**Scoring:**
- 5/5: Perfect concatenation, no errors
- 3/5: Minor formatting issues
- 0/5: Wrong data or empty column

#### Salary Data (5 points)
- [ ] latest_salary shows current/most recent salary
- [ ] No NULL values
- [ ] Values are reasonable (typically $40k-$150k)
- [ ] Only ONE salary per employee (no duplicates showing)

**Scoring:**
- 5/5: Latest salary correct for all employees
- 3/5: Latest salary mostly correct but some employees have issues
- 1/5: Showing historical salaries or many NULL values
- 0/5: Completely wrong

#### Department & Title Data (5 points)
- [ ] Department names are readable (not just codes)
- [ ] Titles are current positions
- [ ] One row per employee (no duplication)
- [ ] No NULL values

**Scoring:**
- 5/5: Correct current department and title for all
- 3/5: Mostly correct with minor errors
- 1/5: Some wrong, some NULL
- 0/5: Completely wrong or missing

---

### Date Calculations (15 points)

#### Years of Experience (7 points)
- [ ] Calculated from hire_date to today (CURDATE())
- [ ] Results are reasonable (typically 20-40 years)
- [ ] Shown as complete years (not decimals)
- [ ] Formula: TIMESTAMPDIFF(YEAR, hire_date, CURDATE())

**Scoring:**
- 7/7: All correct, proper calculation
- 4/7: Mostly correct, minor calculation errors
- 2/7: Some correct, many calculation errors
- 0/7: Completely wrong or missing

#### Age Calculation (8 points)
- [ ] Calculated from birth_date to today (CURDATE())
- [ ] Results are reasonable (typically 55-75 years)
- [ ] Shown as complete years (not decimals)
- [ ] Formula: TIMESTAMPDIFF(YEAR, birth_date, CURDATE())

**Scoring:**
- 8/8: All correct, proper calculation
- 5/8: Mostly correct, minor errors
- 2/8: Some correct, many errors
- 0/8: Completely wrong or missing

---

## 2. Query Structure & Technique (30 points)

### JOIN Implementation (15 points)

#### Employees-Salaries JOIN (3 points)
- [ ] Correctly joins on emp_no
- [ ] Uses subquery to get latest salary
- [ ] Pattern: AND s.to_date = (SELECT MAX(...) FROM salaries ...)

**Scoring:**
- 3/3: Perfect join with latest-record filter
- 1/3: Join works but missing/wrong subquery
- 0/3: Join missing or incorrect

#### Employees-Dept_emp-Departments JOINs (6 points)
- [ ] dept_emp joined to employees on emp_no
- [ ] dept_emp filtered for latest department (with subquery)
- [ ] departments joined to dept_emp on dept_no
- [ ] Pattern: Two joins as described above

**Scoring:**
- 6/6: Both joins perfect with subqueries
- 3/6: Joins present but subquery logic wrong/missing
- 1/6: One join missing or both incomplete
- 0/6: Joins missing or completely wrong

#### Employees-Titles JOIN (3 points)
- [ ] Correctly joins on emp_no
- [ ] Uses subquery to get latest title
- [ ] Pattern: AND t.to_date = (SELECT MAX(...) FROM titles ...)

**Scoring:**
- 3/3: Perfect join with latest-record filter
- 1/3: Join works but subquery missing/wrong
- 0/3: Join missing or incorrect

#### Overall JOIN Quality (3 points)
- [ ] Correct number of JOINs (4 total)
- [ ] All joins use proper aliases
- [ ] Join logic flows correctly from one to next
- [ ] No unnecessary or missing JOINs

**Scoring:**
- 3/3: All 4 JOINs perfect
- 2/3: 3 JOINs correct
- 1/3: 2 JOINs correct
- 0/3: 0-1 JOINs correct

---

### Subquery Implementation (10 points)

#### Subquery Count & Placement (5 points)
- [ ] 3 subqueries total (one each for salaries, dept_emp, titles)
- [ ] Each finds MAX(to_date) for filtering latest records
- [ ] All placed in JOIN ON conditions

**Scoring:**
- 5/5: 3 perfect subqueries in correct locations
- 3/5: 2-3 subqueries present but some issues
- 1/5: 1 subquery or all have significant issues
- 0/5: No subqueries or completely wrong

#### Subquery Correctness (5 points)
- [ ] Each subquery finds MAX(to_date) correctly
- [ ] All use different table alias in subquery (s2, de2, t2)
- [ ] Subqueries correctly correlated to outer query
- [ ] WHERE clause in subquery includes emp_no match

**Scoring:**
- 5/5: All subqueries perfect
- 3/5: Subqueries mostly correct with minor issues
- 1/5: Subqueries present but with significant issues
- 0/5: Subqueries missing or completely wrong

---

### String & Function Usage (5 points)

#### CONCAT() for Names (2 points)
- [ ] Uses CONCAT() function
- [ ] Format: CONCAT(first_name, ' ', last_name)
- [ ] Results are readable full names

**Scoring:**
- 2/2: Perfect CONCAT implementation
- 1/2: CONCAT present but minor issues
- 0/2: CONCAT missing or wrong

#### TIMESTAMPDIFF() for Calculations (3 points)
- [ ] 2 TIMESTAMPDIFF calls (one for experience, one for age)
- [ ] Format: TIMESTAMPDIFF(YEAR, start_date, end_date)
- [ ] Uses CURDATE() for current date

**Scoring:**
- 3/3: Both TIMESTAMPDIFF calls perfect
- 2/3: Both present with minor issues
- 1/3: One correct, one has issues
- 0/3: Missing or wrong

---

## 3. Code Quality (15 points)

### Comments & Documentation (8 points)

#### Header Comment (2 points)
- [ ] Explains what the query does
- [ ] Lists main techniques used

**Scoring:**
- 2/2: Clear, comprehensive header
- 1/2: Header present but minimal
- 0/2: No header

#### Join Comments (4 points)
- [ ] Each JOIN has a comment explaining its purpose
- [ ] Subquery purpose is explained
- [ ] Logic is clear to readers

**Scoring:**
- 4/4: Excellent comments for all JOINs
- 2/4: Comments present but some missing
- 1/4: Minimal comments
- 0/4: No comments

#### Column Explanation (2 points)
- [ ] Each SELECT column has a brief comment
- [ ] Calculated fields explain the formula

**Scoring:**
- 2/2: All columns explained
- 1/2: Most columns explained
- 0/2: No explanation

---

### Code Formatting (7 points)

#### Readability (4 points)
- [ ] Proper indentation
- [ ] Consistent line breaks
- [ ] Opens/closes parentheses aligned
- [ ] Keywords in consistent case (typically uppercase)

**Scoring:**
- 4/4: Excellent formatting throughout
- 3/4: Good formatting with minor issues
- 2/4: Readable but inconsistent
- 1/4: Hard to read, poor formatting
- 0/4: Highly unreadable

#### Alias Usage (3 points)
- [ ] Clear, short aliases (e, s, d, de, t)
- [ ] Aliases consistently used throughout
- [ ] Subquery aliases clearly different (s2, de2, t2)
- [ ] No confusion between aliases

**Scoring:**
- 3/3: Perfect alias usage
- 2/3: Good aliases with minor issues
- 1/3: Aliases present but inconsistent/confusing
- 0/3: No aliases or very confusing

---

## 4. Documentation & Explanation (15 points)

### Written Explanation (10 points)

#### Clarity (5 points)
- [ ] Explains why subqueries are needed
- [ ] Describes the historical data problem
- [ ] Shows how joins connect the tables
- [ ] Language is clear and professional

**Scoring:**
- 5/5: Excellent, thorough explanation
- 3/5: Good explanation with minor gaps
- 2/5: Adequate but could be clearer
- 1/5: Basic explanation, hard to follow
- 0/5: Missing or incomprehensible

#### Completeness (5 points)
- [ ] Explains purpose of each JOIN
- [ ] Describes subquery logic
- [ ] Discusses date calculation approach
- [ ] Mentions concatenation strategy

**Scoring:**
- 5/5: Covers all aspects thoroughly
- 3/5: Covers most aspects
- 2/5: Covers some aspects
- 1/5: Covers minimal aspects
- 0/5: Missing or very incomplete

---

### Sample Output or Testing Evidence (5 points)

- [ ] Shows first 10 rows of actual output
- [ ] Output matches expected format
- [ ] Shows all 7 columns with correct data types
- [ ] Demonstrates query actually runs without errors

**Scoring:**
- 5/5: Complete, correct output provided
- 3/5: Output provided with minor issues
- 1/5: Partial or unclear output
- 0/5: No output or query doesn't run

---

## 5. Bonus Points (Optional, max +10)

### Optimization (up to 3 points)
- Alternative approaches using CTEs or window functions
- Index creation strategy
- Query performance analysis

### Advanced Features (up to 4 points)
- Added filtering by department/title
- Salary categories added
- Tenure in current position calculated
- Sort order optimization

### Exceptional Documentation (up to 3 points)
- Created visual diagrams of schema relationships
- Provided multiple implementation approaches
- Advanced troubleshooting guide
- Performance comparison

---

## Grading Summary Sheet

| Category | Points | Earned | Notes |
|----------|--------|--------|-------|
| Query Correctness | 40 | ___ | |
| - All columns (10) | | | |
| - Data accuracy (15) | | | |
| - Date calculations (15) | | | |
| Query Structure | 30 | ___ | |
| - JOINs (15) | | | |
| - Subqueries (10) | | | |
| - Functions (5) | | | |
| Code Quality | 15 | ___ | |
| - Comments (8) | | | |
| - Formatting (7) | | | |
| Documentation | 15 | ___ | |
| - Explanation (10) | | | |
| - Output (5) | | | |
| **TOTAL** | **100** | **___** | |
| BONUS | +10 | ___ | Optional |
| **FINAL SCORE** | **110** | **___** | |

---

## Grading Benchmarks

| Score | Grade | Status |
|-------|-------|--------|
| 95-100 | A+ | Excellent - Ready for production |
| 90-94 | A | Very Good - Minor improvements only |
| 85-89 | B+ | Good - Some improvements needed |
| 80-84 | B | Satisfactory - Several refinements needed |
| 75-79 | C+ | Acceptable - Significant improvements needed |
| 70-74 | C | Passing - Major revisions recommended |
| <70 | F | Below Standard - Resubmit required |

---

## Feedback Template (For Graders)

```
---
STUDENT: _________________
SCORE: ___/100 (+ ___ BONUS)

STRENGTHS:
- [What they did well]

AREAS FOR IMPROVEMENT:
- [What could be better]

SPECIFIC FEEDBACK:
- Query: [comments]
- Documentation: [comments]
- Code Quality: [comments]

RECOMMENDATIONS FOR NEXT ASSIGNMENT:
- [Suggestions]

---
```

---

This rubric can be customized based on your specific learning objectives and student level. Adjust point values as needed for your course!
