// Run with: mongosh "mongodb://127.0.0.1:27017" setup.js

const blogDB = db.getSiblingDB("blog");

// Make the exercise repeatable without creating duplicate sample data.
blogDB.posts.drop();
blogDB.users.drop();

blogDB.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["username", "email", "password", "createdAt"],
      properties: {
        username: { bsonType: "string", minLength: 3 },
        email: { bsonType: "string", pattern: "^.+@.+\\..+$" },
        password: { bsonType: "string", minLength: 10 },
        createdAt: { bsonType: "date" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

blogDB.createCollection("posts", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["title", "content", "author", "createdAt"],
      properties: {
        title: { bsonType: "string", minLength: 1 },
        content: { bsonType: "string", minLength: 1 },
        author: { bsonType: "objectId" },
        createdAt: { bsonType: "date" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

blogDB.users.createIndex({ username: 1 }, { unique: true });
blogDB.users.createIndex({ email: 1 }, { unique: true });
blogDB.posts.createIndex({ author: 1 });
blogDB.posts.createIndex({ createdAt: -1 });

const users = [
  {
    username: "anita",
    email: "anita@example.com",
    password: "$2b$12$demoHashForAnitaOnly",
    createdAt: ISODate("2026-07-01T09:00:00Z")
  },
  {
    username: "marcus",
    email: "marcus@example.com",
    password: "$2b$12$demoHashForMarcusOnly",
    createdAt: ISODate("2026-07-02T10:30:00Z")
  },
  {
    username: "priya",
    email: "priya@example.com",
    password: "$2b$12$demoHashForPriyaOnly",
    createdAt: ISODate("2026-07-03T14:15:00Z")
  }
];

blogDB.users.insertMany(users);

const anita = blogDB.users.findOne({ username: "anita" });
const marcus = blogDB.users.findOne({ username: "marcus" });
const priya = blogDB.users.findOne({ username: "priya" });

blogDB.posts.insertMany([
  {
    title: "Welcome to Our Engineering Blog",
    content: "A place to share practical lessons from our engineering work.",
    author: anita._id,
    createdAt: ISODate("2026-07-10T08:00:00Z")
  },
  {
    title: "Getting Started with MongoDB",
    content: "MongoDB stores flexible documents while supporting schema validation.",
    author: marcus._id,
    createdAt: ISODate("2026-07-12T11:20:00Z")
  },
  {
    title: "Designing Useful Database Indexes",
    content: "Indexes should follow the queries an application needs to answer.",
    author: priya._id,
    createdAt: ISODate("2026-07-15T16:45:00Z")
  },
  {
    title: "Referencing Authors in Blog Posts",
    content: "The author field stores an ObjectId that references a users document.",
    author: anita._id,
    createdAt: ISODate("2026-07-18T13:10:00Z")
  }
]);

print("Blog database created successfully.");
print(`Users inserted: ${blogDB.users.countDocuments()}`);
print(`Posts inserted: ${blogDB.posts.countDocuments()}`);
