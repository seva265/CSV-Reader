import pytest
from fastapi.testclient import TestClient


class TestAnalysisEndpoints:
    """Tests for analysis endpoints."""

    def test_more_than_3_twos_empty(self, client_empty_db: TestClient):
        """Test with no students having more than 3 twos (empty result)."""
        response = client_empty_db.get("/students/more-than-3-twos")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)
        assert len(result) == 0

    def test_more_than_3_twos_with_results(self, client_with_data: TestClient):
        """Test with students having more than 3 twos."""
        response = client_with_data.get("/students/more-than-3-twos")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)
        # Mock returns data - service filters to only those with > 3 twos
        assert len(result) >= 1
        assert result[0]["full_name"] == "Иванов Иван Иванович"
        assert result[0]["count_twos"] == 4

    def test_less_than_5_twos_empty(self, client_empty_db: TestClient):
        """Test with no students having less than 5 twos (empty result)."""
        response = client_empty_db.get("/students/less-than-5-twos")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)
        assert len(result) == 0

    def test_less_than_5_twos_with_results(self, client_with_data: TestClient):
        """Test with students having less than 5 twos."""
        response = client_with_data.get("/students/less-than-5-twos")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)
        # Mock returns data - service filters to only those with < 5 twos
        assert len(result) >= 1
