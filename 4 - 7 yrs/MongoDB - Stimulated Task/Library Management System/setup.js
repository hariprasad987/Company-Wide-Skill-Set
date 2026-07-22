// Run with: mongosh "mongodb://127.0.0.1:27017" setup.js

const libraryDB = db.getSiblingDB("library");

// Reset only this exercise's collections so the script is repeatable.
libraryDB.loans.drop();
libraryDB.books.drop();
libraryDB.members.drop();

libraryDB.createCollection("members", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "email", "joinedAt", "active"],
      properties: {
        name: { bsonType: "string", minLength: 2 },
        email: { bsonType: "string", pattern: "^.+@.+\\..+$" },
        joinedAt: { bsonType: "date" },
        active: { bsonType: "bool" }
      }
    }
  }
});

libraryDB.createCollection("books", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["title", "author", "isbn", "genre", "availableCopies"],
      properties: {
        title: { bsonType: "string", minLength: 1 },
        author: { bsonType: "string", minLength: 2 },
        isbn: { bsonType: "string", minLength: 10 },
        genre: { bsonType: "string" },
        availableCopies: { bsonType: "int", minimum: 0 }
      }
    }
  }
});

libraryDB.createCollection("loans", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["memberId", "bookId", "borrowedAt", "dueAt"],
      properties: {
        memberId: { bsonType: "objectId" },
        bookId: { bsonType: "objectId" },
        borrowedAt: { bsonType: "date" },
        dueAt: { bsonType: "date" },
        returnedAt: { bsonType: ["date", "null"] }
      }
    }
  }
});

libraryDB.members.createIndex({ email: 1 }, { unique: true });
libraryDB.books.createIndex({ isbn: 1 }, { unique: true });
libraryDB.books.createIndex({ title: "text", author: "text" });
libraryDB.loans.createIndex({ memberId: 1, returnedAt: 1 });
libraryDB.loans.createIndex({ dueAt: 1, returnedAt: 1 });

libraryDB.members.insertMany([
  { name: "Aisha Rao", email: "aisha@example.com", joinedAt: ISODate("2026-01-10T09:00:00Z"), active: true },
  { name: "Daniel Kim", email: "daniel@example.com", joinedAt: ISODate("2026-02-18T11:30:00Z"), active: true },
  { name: "Sofia Martin", email: "sofia@example.com", joinedAt: ISODate("2026-04-05T14:00:00Z"), active: true }
]);

libraryDB.books.insertMany([
  { title: "Clean Code", author: "Robert C. Martin", isbn: "9780132350884", genre: "Software", availableCopies: NumberInt(2) },
  { title: "Designing Data-Intensive Applications", author: "Martin Kleppmann", isbn: "9781449373320", genre: "Technology", availableCopies: NumberInt(1) },
  { title: "The Pragmatic Programmer", author: "David Thomas", isbn: "9780135957059", genre: "Software", availableCopies: NumberInt(0) },
  { title: "Atomic Habits", author: "James Clear", isbn: "9780735211292", genre: "Self Development", availableCopies: NumberInt(3) }
]);

const aisha = libraryDB.members.findOne({ email: "aisha@example.com" });
const daniel = libraryDB.members.findOne({ email: "daniel@example.com" });
const sofia = libraryDB.members.findOne({ email: "sofia@example.com" });
const cleanCode = libraryDB.books.findOne({ isbn: "9780132350884" });
const dataApps = libraryDB.books.findOne({ isbn: "9781449373320" });
const pragmatic = libraryDB.books.findOne({ isbn: "9780135957059" });

libraryDB.loans.insertMany([
  {
    memberId: aisha._id,
    bookId: pragmatic._id,
    borrowedAt: ISODate("2026-07-01T10:00:00Z"),
    dueAt: ISODate("2026-07-15T23:59:59Z"),
    returnedAt: null
  },
  {
    memberId: daniel._id,
    bookId: dataApps._id,
    borrowedAt: ISODate("2026-07-18T12:00:00Z"),
    dueAt: ISODate("2026-08-01T23:59:59Z"),
    returnedAt: null
  },
  {
    memberId: sofia._id,
    bookId: cleanCode._id,
    borrowedAt: ISODate("2026-06-10T09:30:00Z"),
    dueAt: ISODate("2026-06-24T23:59:59Z"),
    returnedAt: ISODate("2026-06-22T15:00:00Z")
  }
]);

print("Library database created successfully.");
print(`Members inserted: ${libraryDB.members.countDocuments()}`);
print(`Books inserted: ${libraryDB.books.countDocuments()}`);
print(`Loans inserted: ${libraryDB.loans.countDocuments()}`);
