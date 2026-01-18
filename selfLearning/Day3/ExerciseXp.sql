-- ==================================================
-- EXERCISE 1: DVD RENTAL
-- ==================================================

-- 1. Get a list of all the languages
SELECT name FROM language;

-- 2. Get a list of all films joined with their languages
-- Selecting film title, description, and language name
SELECT f.title, f.description, l.name AS language_name
FROM film f
JOIN language l ON f.language_id = l.language_id;

-- 3. Get all languages, even if there are no films in those languages
-- Using LEFT JOIN starting from the language table ensures we keep languages with 0 films
SELECT f.title, f.description, l.name AS language_name
FROM language l
LEFT JOIN film f ON l.language_id = f.language_id;

-- 4. Create a new table called new_film
CREATE TABLE new_film (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO new_film (name) VALUES
('Interstellar'),
('The Matrix 4'),
('Titanic 2');

-- 5. Create a new table called customer_review
-- Includes ON DELETE CASCADE for the film_id foreign key
CREATE TABLE customer_review (
    review_id SERIAL PRIMARY KEY,
    film_id INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    title VARCHAR(255),
    score INTEGER,
    review_text TEXT,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_film
        FOREIGN KEY (film_id)
        REFERENCES new_film(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_language
        FOREIGN KEY (language_id)
        REFERENCES language(language_id)
);

-- 6. Add 2 movie reviews linked to valid objects
INSERT INTO customer_review (film_id, language_id, title, score, review_text)
VALUES
(
    (SELECT id FROM new_film WHERE name = 'Interstellar'),
    (SELECT language_id FROM language WHERE name = 'English'),
    'Masterpiece',
    10,
    'Great visual effects and story.'
),
(
    (SELECT id FROM new_film WHERE name = 'Titanic 2'),
    (SELECT language_id FROM language WHERE name = 'English'),
    'Not good',
    2,
    'The sequel was unnecessary.'
);

-- 7. Delete a film from new_film
-- Observation: The corresponding review in customer_review will be automatically deleted.
DELETE FROM new_film WHERE name = 'Titanic 2';


-- ==================================================
-- EXERCISE 2: DVD RENTAL
-- ==================================================

-- 1. Use UPDATE to change the language of some films
-- Updating films with ID 1, 2, and 3 to French (assuming French exists in language table)
UPDATE film
SET language_id = (SELECT language_id FROM language WHERE name = 'French')
WHERE film_id IN (1, 2, 3);

-- 2. Foreign keys for the customer table
-- The customer table typically has 'address_id' (references address) and 'store_id' (references store).
-- This means we must ensure the address and store exist before inserting a new customer.

-- 3. Drop the customer_review table
DROP TABLE customer_review;

-- 4. Find out how many rentals are still outstanding
SELECT COUNT(*)
FROM rental
WHERE return_date IS NULL;

-- 5. Find the 30 most expensive movies which are outstanding
SELECT f.title, f.replacement_cost
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE r.return_date IS NULL
ORDER BY f.replacement_cost DESC
LIMIT 30;

-- 6. INVESTIGATION: Helping the friend find movies

-- Movie 1: Sumo wrestler, Actor Penelope Monroe
SELECT f.title
FROM film f
JOIN film_actor fa ON f.film_id = fa.film_id
JOIN actor a ON fa.actor_id = a.actor_id
WHERE (f.description LIKE '%sumo%' OR f.description LIKE '%Sumo%')
AND a.first_name = 'Penelope'
AND a.last_name = 'Monroe';

-- Movie 2: Documentary, less than 1 hour, Rated 'R'
SELECT f.title
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
WHERE c.name = 'Documentary'
AND f.length < 60
AND f.rating = 'R';

-- Movie 3: Rented by Matthew Mahan, > $4.00, returned between July 28 and Aug 1, 2005
SELECT f.title, p.amount, r.return_date
FROM rental r
JOIN customer c ON r.customer_id = c.customer_id
JOIN payment p ON r.rental_id = p.rental_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE c.first_name = 'Matthew'
AND c.last_name = 'Mahan'
AND p.amount > 4.00
AND r.return_date >= '2005-07-28'
AND r.return_date < '2005-08-02'; -- Using < Aug 02 ensures we catch rentals returned late on Aug 01

-- Movie 4: Rented by Matthew Mahan, contains "boat", expensive replacement
SELECT f.title, f.description, f.replacement_cost
FROM rental r
JOIN customer c ON r.customer_id = c.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
WHERE c.first_name = 'Matthew'
AND c.last_name = 'Mahan'
AND (f.title LIKE '%boat%' OR f.description LIKE '%boat%' OR f.title LIKE '%Boat%' OR f.description LIKE '%Boat%')
ORDER BY f.replacement_cost DESC
LIMIT 1;
