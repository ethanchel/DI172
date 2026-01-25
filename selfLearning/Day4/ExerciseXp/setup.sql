-- Run this in pgAdmin or psql to set up the database

-- Create the database (run this separately if needed)
-- CREATE DATABASE restaurant_db;

-- Connect to the database first, then run:
CREATE TABLE IF NOT EXISTS Menu_Items (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(30) NOT NULL,
    item_price SMALLINT DEFAULT 0
);

-- Optional: Insert some test data
-- INSERT INTO Menu_Items (item_name, item_price) VALUES ('Burger', 35);
-- INSERT INTO Menu_Items (item_name, item_price) VALUES ('Beef Stew', 45);
-- INSERT INTO Menu_Items (item_name, item_price) VALUES ('Salad', 25);
