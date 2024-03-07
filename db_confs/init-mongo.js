// Create a new database and switch to it
db = db.getSiblingDB('wibo_test');


// Create a new collection and insert documents
db.users.insert([
  {
    name: "Francisco1",
    username: "admin",
    email: "fxev90@gmail.com",
    password: "$2b$12$3.Trhi3wYFfZVqMuaGV8SOH2j2MPPu3UF3jpWa79RcxWnBRsJMkzG"
  }
]);

db.cats.insert([
  {
    name: "koko",
    breed: "string",
    age:2,
    gender: "Male",
    status: "Alive",
    description: "Happy cat"
  },
  {
    name: "koko",
    breed: "string",
    age:2,
    gender: "Male",
    status: "Alive",
    description: "Happy cat"
  },
  {
    name: "koko",
    breed: "string",
    age:2,
    gender: "Male",
    status: "Alive",
    description: "Happy cat"
  },
  {
    name: "koko",
    breed: "string",
    age:2,
    gender: "Male",
    status: "Alive",
    description: "Happy cat"
  }
]);


// Create a user with read and write privileges for the database
db.createUser({
  user: 'myuser',
  pwd: 'mypass',
  roles: [
    { role: 'readWrite', db: 'wibo_test' }
  ]
});

