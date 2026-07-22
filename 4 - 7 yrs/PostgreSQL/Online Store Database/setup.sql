-- Run as a PostgreSQL administrator:
-- sudo -u postgres psql -f setup.sql

-- Create the database only when it does not already exist.
SELECT 'CREATE DATABASE online_store'
WHERE NOT EXISTS (
  SELECT FROM pg_database WHERE datname = 'online_store'
)\gexec

\connect online_store

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
  product_id SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  description TEXT,
  price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
  order_id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(user_id),
  order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
  order_item_id SERIAL PRIMARY KEY,
  order_id INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
  product_id INTEGER NOT NULL REFERENCES products(product_id),
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  UNIQUE (order_id, product_id)
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Demonstration hashes only. Production applications must generate secure
-- password hashes and must never store plaintext passwords.
INSERT INTO users (username, email, password) VALUES
  ('alice', 'alice@example.com', '$2b$12$demoHashForAliceOnly'),
  ('ben', 'ben@example.com', '$2b$12$demoHashForBenOnly'),
  ('carla', 'carla@example.com', '$2b$12$demoHashForCarlaOnly');

INSERT INTO products (name, description, price) VALUES
  ('Mechanical Keyboard', 'Compact keyboard with tactile switches', 89.99),
  ('Wireless Mouse', 'Ergonomic rechargeable mouse', 39.50),
  ('USB-C Hub', 'Seven-port hub with HDMI and Ethernet', 54.75),
  ('Laptop Stand', 'Adjustable aluminium desk stand', 42.00),
  ('Noise-Cancelling Headphones', 'Over-ear wireless headphones', 149.95);

INSERT INTO orders (user_id, order_date) VALUES
  ((SELECT user_id FROM users WHERE username = 'alice'), '2026-07-10 09:30:00'),
  ((SELECT user_id FROM users WHERE username = 'ben'), '2026-07-12 14:15:00'),
  ((SELECT user_id FROM users WHERE username = 'alice'), '2026-07-18 11:45:00');

INSERT INTO order_items (order_id, product_id, quantity) VALUES
  (1, 1, 1),
  (1, 2, 2),
  (2, 5, 1),
  (2, 4, 1),
  (3, 3, 2),
  (3, 4, 1);

SELECT 'Online store database created successfully.' AS status;
SELECT COUNT(*) AS users_inserted FROM users;
SELECT COUNT(*) AS products_inserted FROM products;
SELECT COUNT(*) AS orders_inserted FROM orders;
SELECT COUNT(*) AS order_items_inserted FROM order_items;
