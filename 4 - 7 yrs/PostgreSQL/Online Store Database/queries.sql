\connect online_store

\echo '\n=== ALL PRODUCTS ==='
SELECT
  product_id,
  name,
  description,
  price
FROM products
ORDER BY product_id;

\echo '\n=== ORDERS PLACED BY ALICE ==='
SELECT
  o.order_id,
  o.order_date,
  p.name AS product,
  oi.quantity,
  p.price AS unit_price,
  (oi.quantity * p.price)::NUMERIC(10, 2) AS line_total
FROM orders AS o
JOIN users AS u ON u.user_id = o.user_id
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products AS p ON p.product_id = oi.product_id
WHERE u.username = 'alice'
ORDER BY o.order_date, oi.order_item_id;

\echo '\n=== ORDER TOTALS ==='
SELECT
  o.order_id,
  u.username,
  o.order_date,
  SUM(oi.quantity * p.price)::NUMERIC(10, 2) AS order_total
FROM orders AS o
JOIN users AS u ON u.user_id = o.user_id
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products AS p ON p.product_id = oi.product_id
GROUP BY o.order_id, u.username, o.order_date
ORDER BY o.order_id;

\echo '\n=== TOTAL STORE REVENUE ==='
SELECT
  SUM(oi.quantity * p.price)::NUMERIC(12, 2) AS total_revenue
FROM order_items AS oi
JOIN products AS p ON p.product_id = oi.product_id;
