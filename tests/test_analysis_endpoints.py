import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient


class TestAnalysisEndpoints:
    """Basic tests for analysis endpoints."""

    def test_more_than_3_twos_empty(self, client: TestClient):
        """Test with no students having more than 3 twos."""
        response = client.get("/students/more-than-3-twos")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)

    def test_more_than_3_twos_with_results(self, client: TestClient):
        """Test with students having more than 3 twos."""
        response = client.get("/students/more-than-3-twos")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)

    def test_less_than_5_twos_empty(self, client: TestClient):
        """Test with no students having less than 5 twos."""
        response = client.get("/students/less-than-5-twos")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)

    def test_less_than_5_twos_with_results(self, client: TestClient):
        """Test with students having less than 5 twos."""
        response = client.get("/students/less-than-5-twos")
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)
