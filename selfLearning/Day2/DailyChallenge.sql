/* ==================================================
   SQL PUZZLE : THE "NOT IN + NULL" TRAP
   ================================================== */

-- Q1. What will be the OUTPUT of the following statement?
SELECT COUNT(*)
FROM FirstTab AS ft WHERE ft.id NOT IN ( SELECT id FROM SecondTab WHERE id IS NULL );

-- ANSWER: 0
-- EXPLANATION:
-- The subquery returns [NULL].
-- The condition becomes: "id NOT IN (NULL)".
-- In SQL, comparing anything to NULL results in "UNKNOWN".
-- Since the WHERE clause only keeps "TRUE" results (not "UNKNOWN"), 0 rows are selected.


-- Q2. What will be the OUTPUT of the following statement?
SELECT COUNT(*)
FROM FirstTab AS ft WHERE ft.id NOT IN ( SELECT id FROM SecondTab WHERE id = 5 );

-- ANSWER: 2
-- EXPLANATION:
-- The subquery returns [5].
-- The condition becomes: "id NOT IN (5)".
-- We check the rows in FirstTab:
-- 5 NOT IN (5)    -> False
-- 6 NOT IN (5)    -> True  (Counted)
-- 7 NOT IN (5)    -> True  (Counted)
-- NULL NOT IN (5) -> Unknown (Not counted)
-- Total count: 2 (Sharlee and Krish).


-- Q3. What will be the OUTPUT of the following statement?
SELECT COUNT(*)
FROM FirstTab AS ft WHERE ft.id NOT IN ( SELECT id FROM SecondTab );

-- ANSWER: 0
-- EXPLANATION:
-- The subquery returns [5, NULL].
-- The condition becomes: "id NOT IN (5, NULL)".
-- This is equivalent to: "id != 5 AND id != NULL".
-- Because of the "id != NULL" part, the entire expression evaluates to UNKNOWN for every single row.
-- Therefore, 0 rows are returned. This is the biggest trap in SQL.


-- Q4. What will be the OUTPUT of the following statement?
SELECT COUNT(*)
FROM FirstTab AS ft WHERE ft.id NOT IN ( SELECT id FROM SecondTab WHERE id IS NOT NULL );

-- ANSWER: 2
-- EXPLANATION:
-- The subquery filters out the NULL first. It returns only [5].
-- This makes the logic identical to Question 2.
-- The NULL in FirstTab is still ignored (because NULL != 5 is Unknown), but 6 and 7 are counted.
-- Total count: 2.
