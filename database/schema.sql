
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    username VARCHAR(50) UNIQUE NOT NULL,

    email VARCHAR(120) UNIQUE NOT NULL,

    password_hash TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


SELECT * FROM users;




CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    username VARCHAR(50) UNIQUE NOT NULL,

    email VARCHAR(120) UNIQUE NOT NULL,

    password_hash TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


SELECT * FROM users;

--------------------------------------------------------------------------------------------------

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'users';




CREATE TABLE profiles (
    profile_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,

    phone VARCHAR(20),
    college VARCHAR(200),
    branch VARCHAR(100),
    year VARCHAR(20),
    cgpa DECIMAL(4,2),
    skills TEXT,
    career_goal TEXT,

    CONSTRAINT fk_profile_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

SELECT * FROM profiles;

------------------------------------------------------------------

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'profiles'
ORDER BY ordinal_position;

GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLE profiles
TO admin;

GRANT USAGE, SELECT
ON SEQUENCE profiles_profile_id_seq
TO admin;

SELECT current_user;

----------------------------------------------------------------

--Aptitude table store--

-- 1. Aptitude Sections
CREATE TABLE aptitude_sections (
    section_id SERIAL PRIMARY KEY,
    section_name VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO aptitude_sections (section_name)
VALUES
('Quantitative Aptitude'),
('Logical Reasoning'),
('Verbal Ability'),
('Data Interpretation'),
('Psychometric Test');

SELECT * FROM aptitude_sections;



-- 2. Aptitude Topics
CREATE TABLE aptitude_topics (
    topic_id SERIAL PRIMARY KEY,
    section_id INTEGER NOT NULL,
    topic_name VARCHAR(150) NOT NULL,

    CONSTRAINT fk_topic_section
        FOREIGN KEY (section_id)
        REFERENCES aptitude_sections(section_id)
        ON DELETE CASCADE
);

INSERT INTO aptitude_topics (section_id, topic_name)
VALUES
(1, 'Number System'),
(1, 'Percentages'),
(1, 'Profit and Loss'),
(2, 'Coding and Decoding'),
(2, 'Blood Relations'),
(2, 'Logical Sequence'),
(3, 'Vocabulary'),
(3, 'Grammar'),
(3, 'Reading Comprehension'),
(4, 'Tables'),
(4, 'Bar Graphs'),
(4, 'Pie Charts'),
(5, 'Personality Test'),
(5, 'Work Style');

SELECT * FROM aptitude_topics;

--JOIN Query
SELECT
    s.section_name,
    t.topic_id,
    t.topic_name
FROM aptitude_sections s
JOIN aptitude_topics t
    ON s.section_id = t.section_id
ORDER BY s.section_id, t.topic_id;



-- 3. Aptitude Questions
CREATE TABLE aptitude_questions (
    question_id SERIAL PRIMARY KEY,
    topic_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,

    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,

    correct_answer CHAR(1) NOT NULL,
    explanation TEXT,

    CONSTRAINT fk_question_topic
        FOREIGN KEY (topic_id)
        REFERENCES aptitude_topics(topic_id)
        ON DELETE CASCADE,

    CONSTRAINT valid_correct_answer
        CHECK (correct_answer IN ('A', 'B', 'C', 'D'))
);


-- 4. Aptitude Attempts
CREATE TABLE aptitude_attempts (
    attempt_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,

    total_questions INTEGER NOT NULL,
    correct_answers INTEGER NOT NULL,
    score INTEGER NOT NULL,
    percentage NUMERIC(5,2) NOT NULL,

    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_attempt_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_attempt_topic
        FOREIGN KEY (topic_id)
        REFERENCES aptitude_topics(topic_id)
        ON DELETE CASCADE
);


--permisstion query beause of change password
GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLE aptitude_sections
TO admin;

GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLE aptitude_topics
TO admin;

GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLE aptitude_questions
TO admin;

GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLE aptitude_attempts
TO admin;

--This is important because your tables use SERIAL.
GRANT USAGE, SELECT, UPDATE
ON SEQUENCE aptitude_sections_section_id_seq
TO admin;

GRANT USAGE, SELECT, UPDATE
ON SEQUENCE aptitude_topics_topic_id_seq
TO admin;

GRANT USAGE, SELECT, UPDATE
ON SEQUENCE aptitude_questions_question_id_seq
TO admin;

GRANT USAGE, SELECT, UPDATE
ON SEQUENCE aptitude_attempts_attempt_id_seq
TO admin;

SELECT current_user;


--When i am run the query question are not see so this query i am run 
SELECT COUNT(*) FROM aptitude_questions;

SELECT * FROM aptitude_topics;

SELECT *
FROM aptitude_questions
WHERE topic_id = 1;

--API service.py error solve 

ALTER TABLE aptitude_questions
ADD COLUMN difficulty VARCHAR(20);

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'aptitude_questions'
ORDER BY ordinal_position;

GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLE aptitude_questions
TO admin;

GRANT USAGE, SELECT, UPDATE
ON SEQUENCE aptitude_questions_question_id_seq
TO admin;

--after run app.py check the below query run when gimini create the 10 question
SELECT COUNT(*)
FROM aptitude_questions;


-- my data are not store so add some column here query 
ALTER TABLE profiles
ADD COLUMN IF NOT EXISTS city VARCHAR(100),
ADD COLUMN IF NOT EXISTS semester VARCHAR(50),
ADD COLUMN IF NOT EXISTS graduation_year VARCHAR(20),
ADD COLUMN IF NOT EXISTS competitions TEXT,
ADD COLUMN IF NOT EXISTS academic_achievements TEXT,
ADD COLUMN IF NOT EXISTS strengths TEXT,
ADD COLUMN IF NOT EXISTS weaknesses TEXT,
ADD COLUMN IF NOT EXISTS project_title VARCHAR(255),
ADD COLUMN IF NOT EXISTS project_technologies TEXT,
ADD COLUMN IF NOT EXISTS project_description TEXT,
ADD COLUMN IF NOT EXISTS project_github TEXT,
ADD COLUMN IF NOT EXISTS linkedin TEXT,
ADD COLUMN IF NOT EXISTS github TEXT,
ADD COLUMN IF NOT EXISTS resume_link TEXT;
SELECT * FROM profiles;
ALTER TABLE profiles
ADD COLUMN IF NOT EXISTS career_goal TEXT;