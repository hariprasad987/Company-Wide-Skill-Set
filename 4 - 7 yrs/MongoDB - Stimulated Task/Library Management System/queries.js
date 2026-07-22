// Run with: mongosh "mongodb://127.0.0.1:27017/library" queries.js

print("\n=== AVAILABLE BOOKS ===");
db.books
  .find({ availableCopies: { $gt: 0 } }, { _id: 0, title: 1, author: 1, availableCopies: 1 })
  .sort({ title: 1 })
  .forEach((book) => printjson(book));

const loanDetails = [
  { $match: { returnedAt: null } },
  { $lookup: { from: "members", localField: "memberId", foreignField: "_id", as: "member" } },
  { $lookup: { from: "books", localField: "bookId", foreignField: "_id", as: "book" } },
  { $unwind: "$member" },
  { $unwind: "$book" },
  {
    $project: {
      _id: 0,
      member: "$member.name",
      email: "$member.email",
      book: "$book.title",
      borrowedAt: 1,
      dueAt: 1
    }
  },
  { $sort: { dueAt: 1 } }
];

print("\n=== ACTIVE LOANS ===");
db.loans.aggregate(loanDetails).forEach((loan) => printjson(loan));

print("\n=== OVERDUE LOANS AS OF 2026-07-22 ===");
db.loans
  .aggregate([
    { $match: { returnedAt: null, dueAt: { $lt: ISODate("2026-07-22T00:00:00Z") } } },
    ...loanDetails.slice(1)
  ])
  .forEach((loan) => printjson(loan));

print("\n=== COLLECTION SUMMARY ===");
printjson({
  members: db.members.countDocuments(),
  books: db.books.countDocuments(),
  activeLoans: db.loans.countDocuments({ returnedAt: null }),
  returnedLoans: db.loans.countDocuments({ returnedAt: { $ne: null } })
});
