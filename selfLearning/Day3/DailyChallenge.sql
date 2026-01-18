/* ==================================================
   PART I: One-to-One Relationships and Joins
   ================================================== */
-- Instructions
-- You are going to practice tables relationships

-- Part I

-- Create 2 tables : Customer and Customer profile. They have a One to One relationship.

-- A customer can have only one profile, and a profile belongs to only one customer
-- The Customer table should have the columns : id, first_name, last_name NOT NULL
-- The Customer profile table should have the columns : id, isLoggedIn DEFAULT false (a Boolean), customer_id (a reference to the Customer table)

-- Insert those customers

-- John, Doe
-- Jerome, Lalu
-- Lea, Rive

-- Insert those customer profiles, use subqueries

-- John is loggedIn
-- Jerome is not logged in

-- Use the relevant types of Joins to display:

-- The first_name of the LoggedIn customers
-- All the customers first_name and isLoggedIn columns - even the customers those who don’t have a profile.
-- The number of customers that are not LoggedIn


-- Part II:

-- Create a table named Book, with the columns : book_id SERIAL PRIMARY KEY, title NOT NULL, author NOT NULL

-- Insert those books :
-- Alice In Wonderland, Lewis Carroll
-- Harry Potter, J.K Rowling
-- To kill a mockingbird, Harper Lee

-- Create a table named Student, with the columns : student_id SERIAL PRIMARY KEY, name NOT NULL UNIQUE, age. Make sure that the age is never bigger than 15 (Find an SQL method);

-- Insert those students:
-- John, 12
-- Lera, 11
-- Patrick, 10
-- Bob, 14

-- Create a table named Library, with the columns :
-- book_fk_id ON DELETE CASCADE ON UPDATE CASCADE
-- student_id ON DELETE CASCADE ON UPDATE CASCADE
-- borrowed_date
-- This table, is a junction table for a Many to Many relationship with the Book and Student tables : A student can borrow many books, and a book can be borrowed by many children
-- book_fk_id is a Foreign Key representing the column book_id from the Book table
-- student_fk_id is a Foreign Key representing the column student_id from the Student table
-- The pair of Foreign Keys is the Primary Key of the Junction Table

-- Add 4 records in the junction table, use subqueries.
-- the student named John, borrowed the book Alice In Wonderland on the 15/02/2022
-- the student named Bob, borrowed the book To kill a mockingbird on the 03/03/2021
-- the student named Lera, borrowed the book Alice In Wonderland on the 23/05/2021
-- the student named Bob, borrowed the book Harry Potter the on 12/08/2021

-- Display the data
-- Select all the columns from the junction table
-- Select the name of the student and the title of the borrowed books
-- Select the average age of the children, that borrowed the book Alice in Wonderland
-- Delete a student from the Student table, what happened in the junction table ?

-- 1. Create tables
CREATE TABLE Customer (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

CREATE TABLE CustomerProfile (
    id SERIAL PRIMARY KEY,
    isLoggedIn BOOLEAN DEFAULT false,
    customer_id INTEGER REFERENCES Customer(id),
    -- The UNIQUE constraint ensures a strict One-to-One relationship
    CONSTRAINT unique_customer UNIQUE (customer_id)
);

-- 2. Insert Customers
INSERT INTO Customer (first_name, last_name) VALUES
('John', 'Doe'),
('Jerome', 'Lalu'),
('Lea', 'Rive');

-- 3. Insert Profiles (using subqueries)
INSERT INTO CustomerProfile (isLoggedIn, customer_id)
VALUES (
    true,
    (SELECT id FROM Customer WHERE first_name = 'John')
);

INSERT INTO CustomerProfile (isLoggedIn, customer_id)
VALUES (
    false,
    (SELECT id FROM Customer WHERE first_name = 'Jerome')
);

-- 4. Display Queries (JOINS)

-- A. The first_name of the LoggedIn customers
SELECT c.first_name
FROM Customer c
JOIN CustomerProfile cp ON c.id = cp.customer_id
WHERE cp.isLoggedIn = true;

-- B. All the customers first_name and isLoggedIn columns - even those without a profile (LEFT JOIN)
SELECT c.first_name, cp.isLoggedIn
FROM Customer c
LEFT JOIN CustomerProfile cp ON c.id = cp.customer_id;

-- C. The number of customers that are not LoggedIn
-- (This includes those with isLoggedIn = false AND those with no profile at all)
SELECT COUNT(*)
FROM Customer c
LEFT JOIN CustomerProfile cp ON c.id = cp.customer_id
WHERE cp.isLoggedIn = false OR cp.isLoggedIn IS NULL;


/* ==================================================
   PART II: Many-to-Many Relationships
   ================================================== */

-- 1. Create Book table
CREATE TABLE Book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL
);

-- 2. Insert Books
INSERT INTO Book (title, author) VALUES
('Alice In Wonderland', 'Lewis Carroll'),
('Harry Potter', 'J.K Rowling'),
('To kill a mockingbird', 'Harper Lee');

-- 3. Create Student table with age constraint
CREATE TABLE Student (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    age INTEGER CHECK (age <= 15) -- SQL method to limit age
);

-- 4. Insert Students
INSERT INTO Student (name, age) VALUES
('John', 12),
('Lera', 11),
('Patrick', 10),
('Bob', 14);

-- 5. Create Library junction table
CREATE TABLE Library (
    book_fk_id INTEGER REFERENCES Book(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
    student_fk_id INTEGER REFERENCES Student(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
    borrowed_date DATE,
    PRIMARY KEY (book_fk_id, student_fk_id)
);

-- 6. Insert records into the junction table (using subqueries)

-- John / Alice In Wonderland / 15/02/2022
INSERT INTO Library (student_fk_id, book_fk_id, borrowed_date) VALUES (
    (SELECT student_id FROM Student WHERE name = 'John'),
    (SELECT book_id FROM Book WHERE title = 'Alice In Wonderland'),
    '2022-02-15'
);

-- Bob / To kill a mockingbird / 03/03/2021
INSERT INTO Library (student_fk_id, book_fk_id, borrowed_date) VALUES (
    (SELECT student_id FROM Student WHERE name = 'Bob'),
    (SELECT book_id FROM Book WHERE title = 'To kill a mockingbird'),
    '2021-03-03'
);

-- Lera / Alice In Wonderland / 23/05/2021
INSERT INTO Library (student_fk_id, book_fk_id, borrowed_date) VALUES (
    (SELECT student_id FROM Student WHERE name = 'Lera'),
    (SELECT book_id FROM Book WHERE title = 'Alice In Wonderland'),
    '2021-05-23'
);

-- Bob / Harry Potter / 12/08/2021
INSERT INTO Library (student_fk_id, book_fk_id, borrowed_date) VALUES (
    (SELECT student_id FROM Student WHERE name = 'Bob'),
    (SELECT book_id FROM Book WHERE title = 'Harry Potter'),
    '2021-08-12'
);

-- 7. Display Data

-- A. Select all columns from the junction table
SELECT * FROM Library;

-- B. Select the name of the student and the title of the borrowed books
SELECT s.name, b.title
FROM Library l
JOIN Student s ON l.student_fk_id = s.student_id
JOIN Book b ON l.book_fk_id = b.book_id;

-- C. Select the average age of the children that borrowed Alice in Wonderland
SELECT AVG(s.age) as average_age
FROM Library l
JOIN Student s ON l.student_fk_id = s.student_id
JOIN Book b ON l.book_fk_id = b.book_id
WHERE b.title = 'Alice In Wonderland';

-- D. Delete a student from the Student table
DELETE FROM Student WHERE name = 'Bob';
-- Note: Because ON DELETE CASCADE is set in the Library table,
-- all borrowing records for 'Bob' are automatically deleted from Library.
