# Car Rental Management System

A full-stack web application built using **Flask (Python)** and **MySQL** to manage car rentals efficiently.  
This system allows users to manage cars, customers, and rental transactions through a simple and intuitive interface.

---

##  Overview

The Car Rental Management System is designed to streamline the process of renting vehicles.  
It provides functionalities for managing inventory, customers, and rental operations, along with real-time insights through a dashboard.

---

## Key Features

###  Car Management
- Add new cars
- View all cars
- Track availability status (Available / Rented / Maintenance)

###  Customer Management
- Add new customers
- View customer details

### Rental Management
- Rent cars to customers
- Prevent double booking (date conflict check)
- Automatic cost calculation
- Return car with late fine calculation

### Dashboard
- Total Cars
- Available Cars
- Total Customers
- Total Revenue

---

##  Technology Stack

| Layer     | Technology Used |
|----------|----------------|
| Frontend | HTML, CSS      |
| Backend  | Flask (Python) |
| Database | MySQL          |
| Tools    | VS Code        |

---

## Project Structure
car_rental_project/
│
├── app.py
├── db_config.py
│
├── static/
│ └── style.css
│
├── templates/
│ ├── index.html
│ ├── add_car.html
│ ├── add_customer.html
│ ├── rent_car.html
│ ├── view_cars.html
│ ├── view_customers.html
│ └── view_rentals.html
│
└── README.md


---

##  Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/car-rental-project.git
cd car-rental-project
2️⃣ Install Dependencies
pip install flask mysql-connector-python
3️⃣ Database Setup
CREATE DATABASE car_rental;
USE car_rental;

CREATE TABLE Cars (
    car_id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50),
    model VARCHAR(50),
    year INT,
    price_per_day INT,
    status VARCHAR(20)
);

CREATE TABLE Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    license_no VARCHAR(50)
);

CREATE TABLE Rentals (
    rental_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    car_id INT,
    start_date DATE,
    end_date DATE,
    total_amount INT,
    status VARCHAR(20)
);
4️⃣ Configure Database Connection

Update db_config.py:

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="car_rental"
    )
5️⃣ Run the Application
python app.py




## Open in browser:
👉 http://127.0.0.1:5000/

## Core Functionalities :

Car availability tracking
Date conflict handling
Revenue calculation
Late return fine system
🚀 Future Enhancements
🔐 User Authentication
🔍 Search & Filter
✏️ Edit/Delete Features
📱 Responsive UI
💳 Payment Integration
📊 Advanced Dashboard
    Author

Khushi Jindal

---
