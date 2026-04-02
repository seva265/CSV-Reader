import pytest
import os
import sys
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.main import app


@pytest.fixture
def mock_db_default():
    """Default mock database with test data."""
    with patch('app.database.get_db') as mock_get_db, \
         patch('app.database.db_pool', AsyncMock()):
        mock_conn = AsyncMock()
        mock_conn.executemany.return_value = None
        mock_conn.fetch.return_value = [
            {"full_name": "Иванов Иван Иванович", "count_twos": 4},
            {"full_name": "Сидоров Сидор Сидорович", "count_twos": 2}
        ]
        
        # Setup async context manager properly
        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_get_db.return_value = mock_ctx
        
        yield mock_get_db


@pytest.fixture
def client(mock_db_default):
    """Create test client with default database mock."""
    return TestClient(app)


@pytest.fixture
def mock_db_with_data():
    """Mock database with test data (alias for default)."""
    with patch('app.database.get_db') as mock_get_db, \
         patch('app.database.db_pool', AsyncMock()):
        mock_conn = AsyncMock()
        mock_conn.executemany.return_value = None
        mock_conn.fetch.return_value = [
            {"full_name": "Иванов Иван Иванович", "count_twos": 4},
            {"full_name": "Сидоров Сидор Сидорович", "count_twos": 2}
        ]
        
        # Setup async context manager properly
        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_get_db.return_value = mock_ctx
        
        yield mock_get_db


@pytest.fixture
def mock_db_empty():
    """Mock database with empty result."""
    with patch('app.database.get_db') as mock_get_db, \
         patch('app.database.db_pool', AsyncMock()):
        mock_conn = AsyncMock()
        mock_conn.fetch.return_value = []
        
        # Setup async context manager properly
        mock_ctx = MagicMock()
        mock_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_ctx.__aexit__ = AsyncMock(return_value=None)
        mock_get_db.return_value = mock_ctx
        
        yield mock_get_db


@pytest.fixture
def client_with_data(mock_db_with_data):
    """Create test client with database mock containing data."""
    return TestClient(app)


@pytest.fixture
def client_empty_db(mock_db_empty):
    """Create test client with empty database mock."""
    return TestClient(app)


@pytest.fixture
def sample_csv_content():
    """Sample valid CSV content."""
    return '''Дата;Номер группы;ФИО;Оценка
01.01.2024;ИТ-301;Иванов Иван Иванович;5
02.01.2024;ИТ-301;Петров Петр Петрович;4
03.01.2024;ИТ-302;Сидоров Сидор Сидорович;3'''
