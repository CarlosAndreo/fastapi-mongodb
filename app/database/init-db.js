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
