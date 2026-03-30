-- migration 0002: add students and groups and normalize marks

BEGIN;

CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    group_number VARCHAR(50) NOT NULL
);

ALTER TABLE marks ADD COLUMN IF NOT EXISTS student_id INTEGER;
ALTER TABLE marks ADD COLUMN IF NOT EXISTS group_id INTEGER;

INSERT INTO students (full_name)
SELECT DISTINCT full_name FROM marks WHERE full_name IS NOT NULL;

INSERT INTO groups (group_number)
SELECT DISTINCT group_number FROM marks WHERE group_number IS NOT NULL;

UPDATE marks SET student_id = s.id
FROM students s
WHERE marks.full_name = s.full_name;

UPDATE marks SET group_id = g.id
FROM groups g
WHERE marks.group_number = g.group_number;

ALTER TABLE marks ALTER COLUMN student_id SET NOT NULL;
ALTER TABLE marks ALTER COLUMN group_id SET NOT NULL;

ALTER TABLE marks DROP COLUMN IF EXISTS full_name;
ALTER TABLE marks DROP COLUMN IF EXISTS group_number;

CREATE INDEX IF NOT EXISTS idx_marks_student_group ON marks(student_id, group_id);

COMMIT;
