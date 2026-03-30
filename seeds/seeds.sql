-- seeds for normalized schema: students, groups, marks
TRUNCATE TABLE marks, students, groups RESTART IDENTITY CASCADE;

INSERT INTO students (full_name) VALUES
('Иванов Иван Иванович'),
('Петров Петр Петрович'),
('Сидоров Сидор Сидорович'),
('Кузнецов Алексей Иванович'),
('Морозова Анна Сергеевна'),
('Смирнов Иван Петрович'),
('Лебедев Андрей Михайлович'),
('Козлова Мария Ивановна'),
('Новиков Олег Владимирович'),
('Федоров Василий Петрович'),
('Григорьева Светлана Николаевна'),
('Зайцев Денис Олегович'),
('Павлова Елена Андреевна'),
('Орлов Игорь Сергеевич'),
('Васильева Ольга Игоревна');

INSERT INTO groups (group_number) VALUES ('101'), ('102'), ('103');

INSERT INTO marks (student_id, group_id, record_date, grade) VALUES
((SELECT id FROM students WHERE full_name='Иванов Иван Иванович'), (SELECT id FROM groups WHERE group_number='101'), '2024-03-01', 5),
((SELECT id FROM students WHERE full_name='Петров Петр Петрович'), (SELECT id FROM groups WHERE group_number='101'), '2024-03-01', 4),
((SELECT id FROM students WHERE full_name='Сидоров Сидорович'), (SELECT id FROM groups WHERE group_number='101'), '2024-03-01', 3),
((SELECT id FROM students WHERE full_name='Кузнецов Алексей Иванович'), (SELECT id FROM groups WHERE group_number='102'), '2024-03-02', 2),
((SELECT id FROM students WHERE full_name='Морозова Анна Сергеевна'), (SELECT id FROM groups WHERE group_number='102'), '2024-03-02', 5),
((SELECT id FROM students WHERE full_name='Смирнов Иван Петрович'), (SELECT id FROM groups WHERE group_number='103'), '2024-03-03', 2),
((SELECT id FROM students WHERE full_name='Лебедев Андрей Михайлович'), (SELECT id FROM groups WHERE group_number='101'), '2024-03-04', 3),
((SELECT id FROM students WHERE full_name='Козлова Мария Ивановна'), (SELECT id FROM groups WHERE group_number='102'), '2024-03-04', 4),
((SELECT id FROM students WHERE full_name='Новиков Олег Владимирович'), (SELECT id FROM groups WHERE group_number='103'), '2024-03-05', 5),
((SELECT id FROM students WHERE full_name='Федоров Василий Петрович'), (SELECT id FROM groups WHERE group_number='101'), '2024-03-06', 2),
((SELECT id FROM students WHERE full_name='Григорьева Светлана Николаевна'), (SELECT id FROM groups WHERE group_number='102'), '2024-03-06', 3),
((SELECT id FROM students WHERE full_name='Зайцев Денис Олегович'), (SELECT id FROM groups WHERE group_number='103'), '2024-03-07', 4),
((SELECT id FROM students WHERE full_name='Павлова Елена Андреевна'), (SELECT id FROM groups WHERE group_number='101'), '2024-03-07', 5),
((SELECT id FROM students WHERE full_name='Орлов Игорь Сергеевич'), (SELECT id FROM groups WHERE group_number='102'), '2024-03-08', 3),
((SELECT id FROM students WHERE full_name='Васильева Ольга Игоревна'), (SELECT id FROM groups WHERE group_number='103'), '2024-03-08', 2);
