/* ==================================================
   EXERCISE 1 : ORDERING AND LIMITING
   ================================================== */

   /* ==================================================
   EXERCISE 1: ITEMS AND CUSTOMERS (FULL VERSION)
   ================================================== */

-- --------------------------------------------------
-- PART 1: SETUP (Creating tables and data)
-- --------------------------------------------------

-- We drop the tables if they already exist to avoid errors
-- if you run this script multiple times.
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS customers;

-- Create the items table
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    price INTEGER NOT NULL
);

-- Create the customers table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

-- Insert data into items
INSERT INTO items (item_name, price) VALUES
('Small Desk', 100),
('Large desk', 300),
('Fan', 80);

-- Insert data into customers
INSERT INTO customers (first_name, last_name) VALUES
('Greg', 'Jones'),
('Sandra', 'Jones'),
('Scott', 'Scott'),
('Trevor', 'Green'),
('Melanie', 'Johnson');


-- --------------------------------------------------
-- PART 2: SOLUTION (The Queries)
-- --------------------------------------------------

-- 1. All items, ordered by price (lowest to highest)
SELECT * FROM items
ORDER BY price ASC;

-- 2. Items with a price above 80 (80 included), ordered by price (highest to lowest)
SELECT * FROM items
WHERE price >= 80
ORDER BY price DESC;

-- 3. The first 3 customers in alphabetical order of the first name (A-Z)
-- "Exclude the primary key column" means we explicitly select columns
SELECT first_name, last_name
FROM customers
ORDER BY first_name ASC
LIMIT 3;

-- 4. All last names (no other columns!), in reverse alphabetical order (Z-A)
SELECT last_name
FROM customers
ORDER BY last_name DESC;

-- Exercise 2

/* ==================================================
   DVD RENTAL DATABASE EXERCISES
   ================================================== */

-- 1. Select all columns from the “customer” table.
SELECT * FROM customer;

-- 2. Display the names (first_name, last_name) using an alias named “full_name”.
-- In PostgreSQL, we use || to concatenate strings.
SELECT first_name || ' ' || last_name AS full_name
FROM customer;

-- 3. Select all the create_date from the “customer” table (no duplicates).
SELECT DISTINCT create_date
FROM customer;

-- 4. Get all customer details, sorted by first name (descending).
SELECT * FROM customer
ORDER BY first_name DESC;

-- 5. Get film ID, title, description, release year, and rental rate (ascending order).
SELECT film_id, title, description, release_year, rental_rate
FROM film
ORDER BY rental_rate ASC;

-- 6. Get the address and phone of all customers living in the Texas district.
SELECT address, phone
FROM address
WHERE district = 'Texas';

-- 7. Retrieve all movie details where the movie id is either 15 or 150.
SELECT * FROM film
WHERE film_id IN (15, 150);

-- 8. Check if your favorite movie exists in the database.
-- (Replace 'Interstellar' with your favorite movie. If it's not there, the result is empty).
SELECT film_id, title, description, length, rental_rate
FROM film
WHERE title = 'Interstellar';

-- 9. Get movies starting with the two first letters of your favorite movie.
-- Assuming 'In' for Interstellar.
SELECT film_id, title, description, length, rental_rate
FROM film
WHERE title LIKE 'In%';

-- 10. Find the 10 cheapest movies.
SELECT film_id, title, rental_rate
FROM film
ORDER BY rental_rate ASC
LIMIT 10;

-- 11. Find the NEXT 10 cheapest movies (skipping the first 10).
SELECT film_id, title, rental_rate
FROM film
ORDER BY rental_rate ASC
OFFSET 10
LIMIT 10;

-- 11 BONUS: Try to not use LIMIT.
-- The ANSI SQL standard alternative to LIMIT is "FETCH FIRST".
SELECT film_id, title, rental_rate
FROM film
ORDER BY rental_rate ASC
OFFSET 10 ROWS
FETCH NEXT 10 ROWS ONLY;

-- 12. Join customer and payment tables.
-- Get first name, last name, amount, and date of every payment, ordered by customer id.
SELECT c.first_name, c.last_name, p.amount, p.payment_date
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
ORDER BY c.customer_id;

-- 13. Get all movies which are NOT in inventory.
-- We use a LEFT JOIN and check for NULL in the inventory table.
SELECT f.title
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
WHERE i.inventory_id IS NULL;

-- 14. Find which city is in which country.
SELECT ci.city, co.country
FROM city ci
JOIN country co ON ci.country_id = co.country_id;

-- 15 BONUS: Seller performance (Staff members).
-- ordered by the id of the staff member who sold them the dvd.
SELECT c.customer_id, c.first_name, c.last_name, p.amount, p.payment_date, p.staff_id
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
ORDER BY p.staff_id;
