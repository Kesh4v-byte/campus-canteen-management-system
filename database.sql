CREATE DATABASE IF NOT EXISTS canteen_db;
USE canteen_db;

CREATE TABLE IF NOT EXISTS food_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    available TINYINT(1) DEFAULT 1
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    food_id INT NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(8,2) NOT NULL,
    total DECIMAL(8,2) NOT NULL,
    order_status VARCHAR(30) DEFAULT 'Pending',
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES food_items(id)
);

INSERT INTO food_items (name, price, available)
SELECT 'Veg Sandwich', 40.00, 1 WHERE NOT EXISTS (SELECT 1 FROM food_items WHERE name='Veg Sandwich');
INSERT INTO food_items (name, price, available)
SELECT 'Samosa', 15.00, 1 WHERE NOT EXISTS (SELECT 1 FROM food_items WHERE name='Samosa');
INSERT INTO food_items (name, price, available)
SELECT 'Masala Maggi', 50.00, 1 WHERE NOT EXISTS (SELECT 1 FROM food_items WHERE name='Masala Maggi');
INSERT INTO food_items (name, price, available)
SELECT 'Tea', 10.00, 1 WHERE NOT EXISTS (SELECT 1 FROM food_items WHERE name='Tea');
INSERT INTO food_items (name, price, available)
SELECT 'Cold Coffee', 45.00, 1 WHERE NOT EXISTS (SELECT 1 FROM food_items WHERE name='Cold Coffee');
