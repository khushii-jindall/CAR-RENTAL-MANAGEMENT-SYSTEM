CREATE DATABASE CarRentalDB;
USE CarRentalDB;

CREATE TABLE Cars (
    car_id INT PRIMARY KEY AUTO_INCREMENT,
    brand VARCHAR(50),
    model VARCHAR(50),
    year INT,
    price_per_day DECIMAL(10,2),
    status ENUM('available', 'rented', 'maintenance')
);

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    license_no VARCHAR(50) UNIQUE
);

CREATE TABLE Rentals (
    rental_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    car_id INT,
    start_date DATE,
    end_date DATE,
    total_amount DECIMAL(15,2),
    status ENUM('ongoing', 'completed', 'cancelled'),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (car_id) REFERENCES Cars(car_id) ON DELETE CASCADE
);
CREATE DATABASE CarRentalDB;
USE CarRentalDB;

CREATE TABLE Cars (
    car_id INT PRIMARY KEY AUTO_INCREMENT,
    brand VARCHAR(50),
    model VARCHAR(50),
    year INT,
    price_per_day DECIMAL(10,2),
    status ENUM('available', 'rented', 'maintenance')
);

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    license_no VARCHAR(50) UNIQUE
);

CREATE TABLE Rentals (
    rental_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    car_id INT,
    start_date DATE,
    end_date DATE,
    total_amount DECIMAL(15,2),
    status ENUM('ongoing', 'completed', 'cancelled'),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (car_id) REFERENCES Cars(car_id) ON DELETE CASCADE
);

CREATE TABLE Rental_History (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    rental_id INT,
    action_date DATE,
    action VARCHAR(50),
    FOREIGN KEY (rental_id) REFERENCES Rentals(rental_id) ON DELETE CASCADE
);

SELECT * FROM Cars;
SELECT * FROM Customers;
SELECT * FROM Rentals;
SELECT * FROM Rental_History;

SELECT * FROM Cars
WHERE status = 'available';

SELECT name, email, phone FROM Customers;

SELECT * FROM Rentals
WHERE status = 'ongoing';

SELECT * FROM Rentals
WHERE status = 'completed';

SELECT 
    r.rental_id,
    c.name AS customer_name,
    car.brand,
    car.model,
    r.start_date,
    r.end_date,
    r.total_amount,
    r.status
FROM Rentals r
JOIN Customers c ON r.customer_id = c.customer_id
JOIN Cars car ON r.car_id = car.car_id;

SELECT SUM(total_amount) AS total_revenue FROM Rentals;

SELECT car_id, COUNT(*) AS total_rentals
FROM Rentals
GROUP BY car_id
ORDER BY total_rentals DESC;