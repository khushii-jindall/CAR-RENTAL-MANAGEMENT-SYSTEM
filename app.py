from flask import Flask, render_template, request, redirect, flash
from db_config import get_db_connection
from datetime import datetime
app = Flask(__name__)
app.secret_key = "secret123"

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_cars FROM Cars")
    total_cars = cursor.fetchone()['total_cars']

    cursor.execute("SELECT COUNT(*) AS available_cars FROM Cars WHERE status='Available'")
    available_cars = cursor.fetchone()['available_cars']

    cursor.execute("SELECT COUNT(*) AS total_customers FROM Customers")
    total_customers = cursor.fetchone()['total_customers']

    cursor.execute("SELECT SUM(total_amount) AS revenue FROM Rentals")
    revenue = cursor.fetchone()['revenue'] or 0

    conn.close()

    return render_template('index.html',
                           total_cars=total_cars,
                           available_cars=available_cars,
                           total_customers=total_customers,
                           revenue=revenue)

@app.route('/view_cars')
def view_cars():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Cars")
    cars = cursor.fetchall()

    conn.close()
    return render_template('view_cars.html', cars=cars)

@app.route('/available_cars')
def available_cars():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Cars WHERE status='Available'")
    cars = cursor.fetchall()

    conn.close()
    return render_template('view_cars.html', cars=cars)

@app.route('/view_customers')
def view_customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()

    conn.close()
    return render_template('view_customers.html', customers=customers)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            license_no = request.form.get('license_no')

            if not name or not email:
                flash("All fields are required!", "error")
                return redirect('/add_customer')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Customers (name, email, phone, license_no)
                VALUES (%s, %s, %s, %s)
            """, (name, email, phone, license_no))

            conn.commit()
            conn.close()

            flash("Customer added successfully!", "success")
            return redirect('/')

        except Exception as e:
            return str(e)

    return render_template('add_customer.html')
@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        try:
            brand = request.form.get('brand')
            model = request.form.get('model')
            year = request.form.get('year')
            price = request.form.get('price_per_day')
            status = request.form.get('status')

            if not brand or not model:
                flash("Fill all fields!", "error")
                return redirect('/add_car')

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Cars (brand, model, year, price_per_day, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (brand, model, year, price, status))

            conn.commit()
            conn.close()

            flash("Car added successfully!", "success")
            return redirect('/')

        except Exception as e:
            return str(e)

    return render_template('add_car.html')

@app.route('/rent_car', methods=['GET', 'POST'])
def rent_car():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()

    cursor.execute("SELECT * FROM Cars WHERE status='Available'")
    cars = cursor.fetchall()

    if request.method == 'POST':
        try:
            customer_id = request.form.get('customer_id')
            car_id = request.form.get('car_id')
            start = request.form.get('start')
            end = request.form.get('end')

            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")

            if start_date > end_date:
                flash("Invalid date!", "error")
                return redirect('/rent_car')

            cursor.execute("""
                SELECT * FROM Rentals
                WHERE car_id=%s AND (start_date <= %s AND end_date >= %s)
            """, (car_id, end, start))

            if cursor.fetchone():
                flash("Car already booked!", "error")
                return redirect('/rent_car')

            days = (end_date - start_date).days + 1

            cursor.execute("SELECT price_per_day FROM Cars WHERE car_id=%s", (car_id,))
            price = cursor.fetchone()['price_per_day']

            total = days * price

            cursor.execute("""
                INSERT INTO Rentals (customer_id, car_id, start_date, end_date, total_amount, status)
                VALUES (%s, %s, %s, %s, %s, 'Ongoing')
            """, (customer_id, car_id, start, end, total))

            cursor.execute("UPDATE Cars SET status='Rented' WHERE car_id=%s", (car_id,))

            conn.commit()
            conn.close()

            flash("Car rented!", "success")
            return redirect('/view_rentals')

        except Exception as e:
            return str(e)

    conn.close()
    return render_template('rent_car.html', customers=customers, cars=cars)

@app.route('/view_rentals')
def view_rentals():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.rental_id, c.name, ca.model,
               r.start_date, r.end_date, r.total_amount, r.status
        FROM Rentals r
        JOIN Customers c ON r.customer_id = c.customer_id
        JOIN Cars ca ON r.car_id = ca.car_id
    """)

    rentals = cursor.fetchall()

    cursor.execute("SELECT SUM(total_amount) AS revenue FROM Rentals")
    revenue = cursor.fetchone()['revenue'] or 0

    conn.close()

    return render_template('view_rentals.html',
                           rentals=rentals,
                           total_revenue_inr=revenue)

@app.route('/return_car/<int:rental_id>', methods=['POST'])
def return_car(rental_id):
    return_date = request.form.get('actual_return_date')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT car_id, end_date FROM Rentals WHERE rental_id=%s", (rental_id,))
    rental = cursor.fetchone()

    actual = datetime.strptime(return_date, "%Y-%m-%d").date()
    planned = rental['end_date']

    fine = 0
    if actual > planned:
        fine = (actual - planned).days * 200

    cursor.execute("""
        UPDATE Rentals
        SET end_date=%s, total_amount=total_amount + %s, status='Completed'
        WHERE rental_id=%s
    """, (return_date, fine, rental_id))

    cursor.execute("UPDATE Cars SET status='Available' WHERE car_id=%s", (rental['car_id'],))

    conn.commit()
    conn.close()

    flash(f"Returned! Fine: ₹{fine}", "success")
    return redirect('/view_rentals')

if __name__ == '__main__':
    app.run(debug=True)