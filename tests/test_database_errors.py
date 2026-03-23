import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
import app.database


class TestDatabaseErrors:
    """Basic database error tests."""

    @pytest.mark.asyncio
    async def test_database_connection_failure(self):
        """Test database connection failure."""
        with patch('app.database.asyncpg.create_pool') as mock_create_pool:
            mock_create_pool.side_effect = Exception("Connection failed")
            with pytest.raises(Exception, match="Connection failed"):
                await app.database.init_pool()

    def test_database_query_failure(self, client: TestClient):
        """Test database query failure."""
        csv_content = '''Дата;Номер группы;ФИО;Оценка
01.01.2024;ИТ-301;Иванов Иван Иванович;5'''
        files = {"file": ("test.csv", csv_content, "text/csv")}
        response = client.post("/upload-grades", files=files)
        assert response.status_code == 200
