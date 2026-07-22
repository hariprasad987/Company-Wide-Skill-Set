// Run with: mongosh "mongodb://127.0.0.1:27017/blog" queries.js

print("\n=== USERS (password excluded) ===");
db.users
  .find({}, { password: 0 })
  .sort({ username: 1 })
  .forEach((user) => printjson(user));

print("\n=== POSTS WITH AUTHOR DETAILS ===");
db.posts
  .aggregate([
    {
      $lookup: {
        from: "users",
        localField: "author",
        foreignField: "_id",
        as: "authorDetails"
      }
    },
    { $unwind: "$authorDetails" },
    {
      $project: {
        _id: 0,
        title: 1,
        content: 1,
        createdAt: 1,
        author: "$authorDetails.username",
        authorEmail: "$authorDetails.email"
      }
    },
    { $sort: { createdAt: -1 } }
  ])
  .forEach((post) => printjson(post));

print("\n=== POSTS WRITTEN BY ANITA ===");
const anita = db.users.findOne({ username: "anita" });
db.posts
  .find({ author: anita._id }, { title: 1, createdAt: 1 })
  .sort({ createdAt: -1 })
  .forEach((post) => printjson(post));
