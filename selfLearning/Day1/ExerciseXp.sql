/* ==================================================
   EXERCISE 1: ITEMS AND CUSTOMERS
   ================================================== */

-- 1. Create Tables
-- Note: 'public' is usually the default schema in PostgreSQL.
-- We create the tables directly here.

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

-- 2. Insert Items
INSERT INTO items (item_name, price) VALUES
('Small Desk', 100),
('Large desk', 300),
('Fan', 80);

-- 3. Insert Customers
INSERT INTO customers (first_name, last_name) VALUES
('Greg', 'Jones'),
('Sandra', 'Jones'),
('Scott', 'Scott'),
('Trevor', 'Green'),
('Melanie', 'Johnson');

-- 4. Fetch Data

-- All the items
SELECT * FROM items;

-- All the items with a price above 80 (80 not included)
SELECT * FROM items WHERE price > 80;

-- All the items with a price below 300 (300 included)
-- We use '<=' to include 300
SELECT * FROM items WHERE price <= 300;

-- All customers whose last name is ‘Smith’
-- Outcome: This will return an empty result because there is no 'Smith' in the table.
SELECT * FROM customers WHERE last_name = 'Smith';

-- All customers whose last name is ‘Jones’
SELECT * FROM customers WHERE last_name = 'Jones';

-- All customers whose firstname is not ‘Scott’
SELECT * FROM customers WHERE first_name != 'Scott';
