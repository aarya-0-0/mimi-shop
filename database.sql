-- Mimi Shop V1
-- Sample database schema
-- Contains fictional sample product data only.

CREATE DATABASE IF NOT EXISTS minishop;
USE minishop;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    user_password VARCHAR(255) NOT NULL,
    user_role VARCHAR(50) DEFAULT 'customer',
    failed_attempts INT DEFAULT 0,
    locked INT DEFAULT 0
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    product_description TEXT,
    product_price DECIMAL(10,2) NOT NULL,
    product_quantity INT NOT NULL DEFAULT 0,
    product_image VARCHAR(255)
);



CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


INSERT INTO products
(product_name, product_description, product_price, product_quantity, product_image)
VALUES
('Desk Mat', 'A simple desk mat for a clean workspace.', 1200.00, 10, 'deskmat.png'),
('Wireless Mouse', 'A basic wireless mouse for everyday use.', 1800.00, 15, 'mouse.png'),
('Mechanical Keyboard', 'A compact mechanical keyboard.', 5500.00, 8, 'keyboard.png'),
('USB-C Cable', 'A durable USB-C charging and data cable.', 700.00, 25, 'usbc.png'),
('Laptop Stand', 'An adjustable stand for laptops.', 2500.00, 12, 'laptopstand.png'),
('USB Hub', 'A compact USB hub with multiple ports.', 1600.00, 10, 'usbhub.png');

-- Users and orders are intentionally left empty.
-- Users can be created through the Mimi Shop registration page.