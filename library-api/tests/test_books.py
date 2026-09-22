from fastapi.testclient import TestClient


class TestCreateBook:
    def test_create_book_success(self, client: TestClient):
        book_data = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "publication_date": "2008-08-01",
            "summary": "A handbook of agile software craftsmanship"
        }
        response = client.post("/api/v1/books/", json=book_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == book_data["title"]
        assert data["author"] == book_data["author"]
        assert data["publication_date"] == book_data["publication_date"]
        assert data["summary"] == book_data["summary"]
        assert "id" in data

    def test_create_book_without_summary(self, client: TestClient):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "publication_date": "2023-01-01"
        }
        response = client.post("/api/v1/books/", json=book_data)

        assert response.status_code == 201
        data = response.json()
        assert data["summary"] is None

    def test_create_book_invalid_date(self, client: TestClient):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "publication_date": "invalid-date"
        }
        response = client.post("/api/v1/books/", json=book_data)

        assert response.status_code == 422

    def test_create_book_missing_required_fields(self, client: TestClient):
        book_data = {"title": "Test Book"}
        response = client.post("/api/v1/books/", json=book_data)

        assert response.status_code == 422


class TestListBooks:
    def test_list_books_empty(self, client: TestClient):
        response = client.get("/api/v1/books/")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_books_with_data(self, client: TestClient):
        book1 = {"title": "Clean Code", "author": "Robert Martin", "publication_date": "2008-08-01"}
        book2 = {"title": "Design Patterns", "author": "Gang of Four", "publication_date": "1994-10-31"}

        client.post("/api/v1/books/", json=book1)
        client.post("/api/v1/books/", json=book2)

        response = client.get("/api/v1/books/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_books_filter_by_title(self, client: TestClient):
        client.post(
            "/api/v1/books/",
            json={"title": "Clean Code", "author": "Robert Martin", "publication_date": "2008-08-01"},
        )
        client.post(
            "/api/v1/books/",
            json={"title": "Design Patterns", "author": "Gang of Four", "publication_date": "1994-10-31"},
        )

        response = client.get("/api/v1/books/?title=clean")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Clean Code"

    def test_list_books_filter_by_author(self, client: TestClient):
        client.post(
            "/api/v1/books/",
            json={"title": "Clean Code", "author": "Robert Martin", "publication_date": "2008-08-01"},
        )
        client.post(
            "/api/v1/books/",
            json={"title": "Clean Architecture", "author": "Robert Martin", "publication_date": "2017-09-10"},
        )
        client.post(
            "/api/v1/books/",
            json={"title": "Design Patterns", "author": "Gang of Four", "publication_date": "1994-10-31"},
        )

        response = client.get("/api/v1/books/?author=martin")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(b["author"] == "Robert Martin" for b in data)

    def test_list_books_filter_by_both(self, client: TestClient):
        client.post(
            "/api/v1/books/",
            json={"title": "Clean Code", "author": "Robert Martin", "publication_date": "2008-08-01"},
        )
        client.post(
            "/api/v1/books/",
            json={"title": "Clean Architecture", "author": "Robert Martin", "publication_date": "2017-09-10"},
        )

        response = client.get("/api/v1/books/?title=clean&author=martin")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
