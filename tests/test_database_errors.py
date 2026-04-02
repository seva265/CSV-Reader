import pytest
from unittest.mock import patch
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
