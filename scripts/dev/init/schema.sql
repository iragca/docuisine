CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title TEXT NOT NULL,
    instructions TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id),
    name TEXT NOT NULL,
    quantity TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE store (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT
);


CREATE INDEX idx_user_email ON users(email);
