// Create the database if it doesn't exist
var dbName = process.env.MONGO_INITDB_DATABASE;
var db = db.getSiblingDB(dbName);
var dbRootUsername = process.env.MONGO_INITDB_ROOT_USERNAME;
var dbRootPassword = process.env.MONGO_INITDB_ROOT_PASSWORD;

// Create collections
db.createCollection("users");

// Create root user
db.createUser({
    user: dbRootUsername,
    pwd: dbRootPassword,
    roles: [
        { role: "dbOwner", db: `${dbName}` }
    ]
});

// Create indexes
// Users collection indexes
db.users.createIndex(
    { username: 1 },
    { unique: true, name: "username_unique_idx" }
);

db.users.createIndex(
    { email: 1 },
    { unique: true, sparse: true, name: "email_unique_idx" }
);
