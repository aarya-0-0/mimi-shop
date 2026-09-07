# Mimi Shop 🛍️

A simple shopping web application built as a learning project using **Python, Flask, HTML, CSS, and MySQL**.

Mimi Shop was created to practice combining web development, database integration, and basic cybersecurity concepts into a working application.

## Features

- User registration and login
- Password hashing
- Product browsing
- Add products to cart
- Checkout
- Order confirmation
- MySQL database integration
- Basic account lockout after repeated failed login attempts
- SQL injection assessment and mitigation

## Technologies Used

- **Python**
- **Flask**
- **HTML**
- **CSS**
- **MySQL**
- **Git & GitHub**

## Database Setup

The project uses MySQL. A sample database schema is provided in `database.sql`.

Import the SQL file into MySQL and update the database connection settings in `app.py` or environment variables before running the application.

## Security

After building the basic functionality, I performed a small security review of the application.

### Implemented

- Passwords are stored using password hashing rather than plaintext.
- SQL queries use parameterized statements to reduce SQL injection risk.
- Login attempts are tracked and the account is locked after repeated failed attempts.

### Assessed

- SQL Injection
- Path Traversal
- Brute-force attacks

Path traversal was considered **not applicable** to this version because the application does not currently use user-controlled file paths.

## Project Status

**Version 1  Completed**

This version focuses on core shopping functionality and basic security practices.

## Limitations

Mimi Shop V1 is intentionally kept simple and has several limitations:

- No admin accounts or admin dashboard
- No separate admin functionality for managing products or orders
- Orders cannot currently be updated or managed after being placed
- An `order_items` table has not been implemented; order information is kept in a simpler structure for V1
- No payment gateway integration
- No advanced role-based access control
- Account lockout is basic and does not currently include a timed unlock mechanism
- The application has not been designed or tested for production deployment

These limitations are planned considerations for future versions rather than goals for V1.

## Future Improvements

Possible improvements for future versions include:

- Admin accounts and an admin dashboard
- Product and order management
- `order_items` table and improved order database structure
- Better order status management
- More robust account lockout and rate limiting
- Additional security testing
- Improved error handling
- Payment integration

## Disclaimer

This project was created for educational and portfolio purposes and is **not intended for production use**.
