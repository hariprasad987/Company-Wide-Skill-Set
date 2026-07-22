# MongoDB Blog Database Schema

This project creates a `blog` database with validated `users` and `posts` collections. A post references its author through the user's MongoDB `ObjectId`.

> The sample password values imitate hashes for demonstration. A real application must generate strong password hashes with a trusted library and must never store plaintext passwords.

## Open in VSCodium

1. Open VSCodium.
2. Select **File → Open Folder**.
3. Open `4 - 7 yrs/MongoDB/Blog Database Schema`.
4. Select **Terminal → New Terminal**.

## Check MongoDB

```bash
mongod --version
mongosh --version
sudo systemctl status mongod --no-pager
```

## Create the schema and sample data

From this project folder, run:

```bash
mongosh "mongodb://127.0.0.1:27017" setup.js
```

This safely recreates the two exercise collections and inserts three users and four posts.

## Run the queries

```bash
mongosh "mongodb://127.0.0.1:27017/blog" queries.js
```

The queries display users without passwords, join posts to their authors with `$lookup`, and find all posts written by Anita.

## Explore interactively

```bash
mongosh
```

Then enter:

```javascript
use blog
show collections
db.users.find({}, { password: 0 })
db.posts.find()
```

## Schema summary

### `users`

| Field | BSON type | Notes |
|---|---|---|
| `username` | String | Required and unique |
| `email` | String | Required and unique |
| `password` | String | Required; store a secure hash only |
| `createdAt` | Date | Required |

### `posts`

| Field | BSON type | Notes |
|---|---|---|
| `title` | String | Required |
| `content` | String | Required |
| `author` | ObjectId | References `users._id` |
| `createdAt` | Date | Required |
