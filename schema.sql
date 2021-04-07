
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER,
    visible INTEGER
);
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    topic TEXT UNIQUE,
    content TEXT,
    owner_id INTEGER REFERENCES users,
    created TIMESTAMP,
    visible INTEGER
);
CREATE TABLE participants (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    student_id INTEGER REFERENCES users,
    visible INTEGER
);