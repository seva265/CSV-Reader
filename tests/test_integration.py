"""
Integration tests that require a real database connection.
These tests are skipped by default unless USE_REAL_DB environment variable is set.

To run integration tests:
    export USE_REAL_DB=1
    pytest tests/test_integration.py -v

Make sure your .env file has correct database credentials or set them via environment variables.
"""
import pytest
import os
import sys
import asyncpg

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.main import app
from fastapi.testclient import TestClient
from app.config import DB_URL
from unittest.mock import patch


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def db_pool():
    """Create a real database connection pool for integration tests."""
    if not os.getenv("USE_REAL_DB"):
        pytest.skip("Integration tests are disabled. Set USE_REAL_DB=1 to enable.")
    
    try:
        pool = await asyncpg.create_pool(DB_URL, min_size=1, max_size=2)
        yield pool
        await pool.close()
    except Exception as e:
        pytest.skip(f"Cannot connect to database: {e}")


@pytest.fixture(scope="module", autouse=True)
async def setup_test_data(db_pool):
    """Setup and teardown test data for integration tests."""
    if not os.getenv("USE_REAL_DB"):
        return
    
    conn = await db_pool.acquire()
    try:
        # Clean up any existing test data
        await conn.execute("""
            DELETE FROM marks WHERE group_id IN (SELECT id FROM groups WHERE group_number = 'TEST-001');
            DELETE FROM students WHERE full_name LIKE 'Test Student%';
            DELETE FROM groups WHERE group_number = 'TEST-001';
        """)
        
        # Insert test data
        group_id = await conn.fetchval(
            "INSERT INTO groups (group_number) VALUES ('TEST-001') RETURNING id"
        )
        
        student_ids = []
        for i in range(3):
            sid = await conn.fetchval(
                "INSERT INTO students (full_name) VALUES ($1) RETURNING id",
                f"Test Student {i+1}"
            )
            student_ids.append(sid)
        
        # Insert marks: Student 1 gets 4 twos, Student 2 gets 2 twos, Student 3 gets no twos
        marks_data = [
            (student_ids[0], group_id, "2024-01-01", 2),
            (student_ids[0], group_id, "2024-01-02", 2),
            (student_ids[0], group_id, "2024-01-03", 2),
            (student_ids[0], group_id, "2024-01-04", 2),
            (student_ids[0], group_id, "2024-01-05", 5),
            
            (student_ids[1], group_id, "2024-01-01", 2),
            (student_ids[1], group_id, "2024-01-02", 2),
            (student_ids[1], group_id, "2024-01-03", 4),
            (student_ids[1], group_id, "2024-01-04", 5),
            
            (student_ids[2], group_id, "2024-01-01", 4),
            (student_ids[2], group_id, "2024-01-02", 5),
            (student_ids[2], group_id, "2024-01-03", 5),
        ]
        
        await conn.executemany(
            "INSERT INTO marks (student_id, group_id, record_date, grade) VALUES ($1, $2, $3, $4)",
            marks_data
        )
        
        yield
        
    finally:
        # Cleanup after tests
        await conn.execute("""
            DELETE FROM marks WHERE group_id IN (SELECT id FROM groups WHERE group_number = 'TEST-001');
            DELETE FROM students WHERE full_name LIKE 'Test Student%';
            DELETE FROM groups WHERE group_number = 'TEST-001';
        """)
        await db_pool.release(conn)


@pytest.fixture
def integration_client(db_pool):
    """Create test client with real database connection."""
    if not os.getenv("USE_REAL_DB"):
        pytest.skip("Integration tests are disabled. Set USE_REAL_DB=1 to enable.")
    
    with patch('app.database.db_pool', db_pool):
        yield TestClient(app)


class TestIntegrationAnalysis:
    """Integration tests for analysis endpoints with real database."""

    def test_more_than_3_twos_real_db(self, integration_client):
        """Test more-than-3-twos endpoint with real database."""
        response = integration_client.get("/students/more-than-3-twos")
        assert response.status_code == 200
        result = response.json()
        
        assert isinstance(result, list)
        # Should find exactly one student (Test Student 1) with more than 3 twos
        assert len(result) == 1
        assert result[0]["full_name"] == "Test Student 1"
        assert result[0]["count_twos"] == 4

    def test_less_than_5_twos_real_db(self, integration_client):
        """Test less-than-5-twos endpoint with real database."""
        response = integration_client.get("/students/less-than-5-twos")
        assert response.status_code == 200
        result = response.json()
        
        assert isinstance(result, list)
        # Should find all 3 test students (all have less than 5 twos)
        names = [student["full_name"] for student in result]
        assert "Test Student 1" in names
        assert "Test Student 2" in names
        assert "Test Student 3" in names


class TestIntegrationUpload:
    """Integration tests for CSV upload with real database."""

    def test_upload_grades_real_db(self, integration_client, db_pool):
        """Test CSV upload endpoint with real database."""
        csv_content = """Дата;Номер группы;ФИО;Оценка
15.06.2024;TEST-002;Integration Test User;4
16.06.2024;TEST-002;Integration Test User;5
17.06.2024;TEST-002;Another Test User;2"""

        files = {"file": ("test.csv", csv_content.encode('utf-8'), "text/csv")}
        
        response = integration_client.post("/upload-grades", files=files)
        assert response.status_code == 200
        result = response.json()
        
        assert result["status"] == "success"
        assert result["records_loaded"] == 3
        assert result["students"] == 2
        
        # Verify data was actually inserted into the database
        import asyncio
        async def verify_data():
            conn = await db_pool.acquire()
            try:
                count = await conn.fetchval(
                    "SELECT COUNT(*) FROM marks WHERE group_id IN (SELECT id FROM groups WHERE group_number = 'TEST-002')"
                )
                assert count == 3
                
                student_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM students WHERE full_name IN ('Integration Test User', 'Another Test User')"
                )
                assert student_count == 2
            finally:
                await db_pool.release(conn)
        
        asyncio.get_event_loop().run_until_complete(verify_data())
        
        # Cleanup
        async def cleanup():
            conn = await db_pool.acquire()
            try:
                await conn.execute("""
                    DELETE FROM marks WHERE group_id IN (SELECT id FROM groups WHERE group_number = 'TEST-002');
                    DELETE FROM students WHERE full_name IN ('Integration Test User', 'Another Test User');
                    DELETE FROM groups WHERE group_number = 'TEST-002';
                """)
            finally:
                await db_pool.release(conn)
        
        asyncio.get_event_loop().run_until_complete(cleanup())
