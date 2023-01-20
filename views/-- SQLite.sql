-- SQLite
-- Get only the animal rows where the `id` field value is 3
SELECT
    a.id,
    a.name,
    a.breed,
    a.status,
    a.location_id,
    a.customer_id
FROM animal a
WHERE a.id = 5;

SELECT
    a.id,
    a.name, 
	a.address,
	a.email,
	a.password
FROM customer a
WHERE a.id = 2;


SELECT
    a.id,
    a.name, 
	a.address,
	a.location_id
FROM employee a
WHERE a.id = 4;


SELECT
    a.id,
    a.name, 
	a.address
FROM location a
WHERE a.id = 1;

SELECT
    a.id,
    a.name,
    a.breed,
    a.status,
    a.location_id,
    a.customer_id,
    l.name location_name,
    l.address location_address
FROM Animal a
JOIN Location l
    ON l.id = a.location_id


SELECT
    a.id,
    a.name,
    a.breed,
    a.status,
    a.location_id,
    a.customer_id,
    l.name location_name,
    l.address location_address,
    c.name customer_name
FROM Animal a
JOIN Location l
    ON l.id = a.location_id
JOIN Customer c
    ON c.id = a.customer_id

SELECT
    e.id,
    e.name,
    e.address,
    e.location_id,
    l.name location_name,
    l.address location_address
FROM Employee e
JOIN Location l
    ON l.id = e.location_id