-- - 1. Count how many actors are in the table
SELECT COUNT(*) FROM actors;

-- 2. Try to add a new actor with some blank fields
-- Assumption: The table was created with NOT NULL constraints on first_name/last_name.
-- We try to insert a record where the first_name is NULL (missing).

INSERT INTO actors (first_name, last_name, age, number_oscars)
VALUES (NULL, 'Damon', '1970-10-08', 5);
