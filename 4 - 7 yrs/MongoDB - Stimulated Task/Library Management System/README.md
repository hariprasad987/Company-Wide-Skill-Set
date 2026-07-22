# Library Management System — Stimulated MongoDB Task

This simulated project models a small library with three validated MongoDB collections:

- `members` stores library-member profiles.
- `books` stores catalog and availability information.
- `loans` references members and books by `ObjectId`.

It includes unique, text, and compound indexes plus aggregation queries that join related documents.

## Run in VSCodium

Open this folder in VSCodium and select **Terminal → New Terminal**.

Confirm MongoDB is running:

```bash
sudo systemctl start mongod
sudo systemctl status mongod --no-pager
```

Create the database and sample records:

```bash
mongosh "mongodb://127.0.0.1:27017" setup.js
```

Run the library reports:

```bash
mongosh "mongodb://127.0.0.1:27017/library" queries.js
```

The reports display available books, all active loans, overdue loans, and collection totals.

## Explore interactively

```bash
mongosh "mongodb://127.0.0.1:27017/library"
```

```javascript
show collections
db.members.find()
db.books.find()
db.loans.find()
```
