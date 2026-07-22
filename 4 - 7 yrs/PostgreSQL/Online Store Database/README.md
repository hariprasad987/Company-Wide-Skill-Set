# PostgreSQL Online Store Database

This project creates an `online_store` database with four related tables:

- `users`
- `products`
- `orders`
- `order_items`

It includes primary keys, foreign keys, uniqueness rules, validation constraints, indexes, and sample data.

> Sample password values imitate hashes. A real application must generate secure password hashes and never store plaintext passwords.

## Open in VSCodium

1. Open VSCodium.
2. Select **File → Open Folder**.
3. Open `4 - 7 yrs/PostgreSQL/Online Store Database`.
4. Select **Terminal → New Terminal**.

## Check PostgreSQL

```bash
psql --version
sudo systemctl status postgresql --no-pager
```

## Create the database, tables, and sample data

From this folder, run:

```bash
sudo -u postgres psql -v ON_ERROR_STOP=1 -f setup.sql
```

The script is safe to rerun. It preserves the database itself while recreating this exercise's tables and sample records.

## Run the reports

```bash
sudo -u postgres psql -v ON_ERROR_STOP=1 -f queries.sql
```

The reports display all products, Alice's orders, each order total, and total store revenue.

## Connect interactively

```bash
sudo -u postgres psql online_store
```

Useful `psql` commands:

```text
\dt
\d users
\d products
\d orders
\d order_items
\q
```
