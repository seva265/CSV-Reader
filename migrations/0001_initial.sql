-- migration 0001: создание таблицы marks

CREATE TABLE IF NOT EXISTS marks (
    id SERIAL PRIMARY KEY,
    record_date DATE NOT NULL,
    group_number VARCHAR(50) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    grade INTEGER NOT NULL CHECK (grade >= 2 AND grade <= 5)
);

CREATE INDEX IF NOT EXISTS idx_marks_grade_name ON marks(grade, full_name);
