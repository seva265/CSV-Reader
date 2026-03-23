import pytest
import os
import sys
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def mock_database():
    """Mock database for all tests."""
    with patch('app.database.get_db') as mock_get_db, \
         patch('app.database.db_pool', AsyncMock()):
        mock_conn = AsyncMock()
        mock_conn.executemany.return_value = None
        mock_conn.fetch.return_value = [
            {"full_name": "Иванов Иван Иванович", "count_twos": 4},
            {"full_name": "Сидоров Сидор Сидорович", "count_twos": 2}
        ]
        mock_get_db.return_value.__aenter__.return_value = mock_conn
        yield


@pytest.fixture
def sample_csv_content():
    """Sample valid CSV content."""
    return '''Дата;Номер группы;ФИО;Оценка
01.01.2024;ИТ-301;Иванов Иван Иванович;5
02.01.2024;ИТ-301;Петров Петр Петрович;4
03.01.2024;ИТ-302;Сидоров Сидор Сидорович;3'''
