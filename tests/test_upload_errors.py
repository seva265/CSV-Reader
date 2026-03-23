import pytest
import io
from fastapi.testclient import TestClient


class TestCSVUpload:
    """Basic tests for CSV upload endpoint."""

    def test_upload_no_file(self, client: TestClient):
        """Test uploading without a file."""
        response = client.post("/upload-grades")
        assert response.status_code == 422

    def test_upload_non_csv_file(self, client: TestClient):
        """Test uploading non-CSV file."""
        files = {"file": ("test.txt", "some text", "text/plain")}
        response = client.post("/upload-grades", files=files)
        assert response.status_code == 400
        assert response.json()["detail"] == 'Not a .csv'

    def test_upload_wrong_headers(self, client: TestClient):
        """Test uploading CSV with wrong headers."""
        csv_content = '''Date;Group;Name;Grade
01/01/2024;IT301;John Doe;5'''
        files = {"file": ("test.csv", csv_content, "text/csv")}
        response = client.post("/upload-grades", files=files)
        assert response.status_code == 400
        assert response.json()["detail"] == 'Invalid headers'

    def test_upload_invalid_marks_and_dates(self, client: TestClient):
        """Test uploading CSV with invalid marks and dates."""
        csv_content = '''Дата;Номер группы;ФИО;Оценка
01.01.2024;ИТ-301;Иванов Иван Иванович;1
02.01.2024;ИТ-301;Петров Петр Петрович;4
03.01.2024;ИТ-302;Сидоров Сидор Сидорович;6'''
        files = {"file": ("test.csv", csv_content, "text/csv")}
        response = client.post("/upload-grades", files=files)
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "ok"
        assert result["records_loaded"] == 1  # Only one valid record
