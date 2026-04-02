from typing import List, Tuple, Dict, Any

async def insert_marks(conn, marks: List[Tuple[Any, str, str, int]]) -> Tuple[int, int]:
    student_cache: Dict[str, int] = {}
    group_cache: Dict[str, int] = {}
    inserted = 0

    for record_date, group_number, full_name, grade in marks:
        sid = student_cache.get(full_name)
        if sid is None:
            sid = await conn.fetchval('SELECT id FROM students WHERE full_name=$1', full_name)
            if sid is None:
                sid = await conn.fetchval('INSERT INTO students(full_name) VALUES($1) RETURNING id', full_name)
            student_cache[full_name] = sid

        gid = group_cache.get(group_number)
        if gid is None:
            gid = await conn.fetchval('SELECT id FROM groups WHERE group_number=$1', group_number)
            if gid is None:
                gid = await conn.fetchval('INSERT INTO groups(group_number) VALUES($1) RETURNING id', group_number)
            group_cache[group_number] = gid

        await conn.execute(
            'INSERT INTO marks (student_id, group_id, record_date, grade) VALUES ($1, $2, $3, $4)',
            sid, gid, record_date, grade,
        )
        inserted += 1

    return inserted, len(student_cache)


async def get_students_with_more_than_n_twos(conn, n: int):
    rows = await conn.fetch(
        '''
        SELECT s.full_name, COUNT(*) AS count_twos
        FROM marks m
        JOIN students s ON m.student_id = s.id
        WHERE m.grade = 2
        GROUP BY s.full_name
        HAVING COUNT(*) > $1
        ''',
        n,
    )
    return [{"full_name": r["full_name"], "count_twos": r["count_twos"]} for r in rows]


async def get_students_with_less_than_n_twos(conn, n: int):
    rows = await conn.fetch(
        '''
        SELECT s.full_name, COUNT(*) FILTER (WHERE m.grade = 2) AS count_twos
        FROM marks m
        JOIN students s ON m.student_id = s.id
        GROUP BY s.full_name
        HAVING COUNT(*) FILTER (WHERE m.grade = 2) < $1
        ''',
        n,
    )
    return [{"full_name": r["full_name"], "count_twos": r["count_twos"]} for r in rows]
