
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
    modified TIMESTAMP,
    visible INTEGER
);
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    question TEXT,
    answer TEXT,
    options TEXT, --format: "option1,option2,option3"
    visible INTEGER
);
CREATE TABLE performance (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    student_id INTEGER REFERENCES users,
    points INTEGER,
    maximum INTEGER,
    visible INTEGER
);