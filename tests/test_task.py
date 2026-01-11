import pytest
from fastapi import status

# Test data for task
TASK_DATA = {
    "title": "Complete project",
    "description": "Finish the API implementation",
    "completed": False,
    "priority": 1
}


class TestCreateTask:
    """Tests for creating tasks."""

    def test_create_success(self, client):
        """Test creating a valid task."""
        response = client.post("/tasks/", json=TASK_DATA)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "id" in data
        assert data["title"] == TASK_DATA["title"]
        assert data["description"] == TASK_DATA["description"]
        assert data["completed"] == TASK_DATA["completed"]
        assert data["priority"] == TASK_DATA["priority"]

    def test_create_minimal(self, client):
        """Test creating task with only required fields."""
        response = client.post("/tasks/", json={"title": "Minimal task"})
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Minimal task"
        assert data["completed"] is False
        assert data["priority"] == 0

    def test_create_missing_title(self, client):
        """Test creating task without title fails."""
        response = client.post("/tasks/", json={"description": "No title"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_empty_title(self, client):
        """Test creating task with empty title fails."""
        response = client.post("/tasks/", json={"title": ""})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_invalid_priority(self, client):
        """Test creating task with invalid priority fails."""
        response = client.post("/tasks/", json={"title": "Test", "priority": 10})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestReadTask:
    """Tests for reading tasks."""

    def test_list_empty(self, client):
        """Test listing tasks when database is empty."""
        response = client.get("/tasks/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_with_data(self, client):
        """Test listing tasks with existing data."""
        # Create test data first
        client.post("/tasks/", json=TASK_DATA)

        response = client.get("/tasks/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == TASK_DATA["title"]

    def test_list_with_pagination(self, client):
        """Test listing tasks with pagination."""
        # Create multiple items
        for i in range(5):
            client.post("/tasks/", json={"title": f"Task {i}"})

        # Test pagination
        response = client.get("/tasks/?skip=0&limit=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

    def test_list_filter_completed(self, client):
        """Test filtering tasks by completed status."""
        # Create completed and incomplete tasks
        client.post("/tasks/", json={"title": "Incomplete"})
        client.post("/tasks/", json={"title": "Complete", "completed": True})

        # Filter for completed
        response = client.get("/tasks/?completed=true")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Complete"

    def test_get_by_id_success(self, client):
        """Test getting task by ID."""
        # Create item first
        create_response = client.post("/tasks/", json=TASK_DATA)
        task_id = create_response.json()["id"]

        # Get by ID
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == task_id
        assert response.json()["title"] == TASK_DATA["title"]

    def test_get_by_id_not_found(self, client):
        """Test getting non-existent task."""
        response = client.get("/tasks/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Task not found" in response.json()["detail"]


class TestUpdateTask:
    """Tests for updating tasks."""

    def test_update_success(self, client):
        """Test updating task successfully."""
        # Create item first
        create_response = client.post("/tasks/", json=TASK_DATA)
        task_id = create_response.json()["id"]

        # Update
        update_data = {"title": "Updated Title", "completed": True}
        response = client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Updated Title"
        assert response.json()["completed"] is True
        assert response.json()["updated_at"] is not None

    def test_update_partial(self, client):
        """Test partial update of task."""
        # Create item first
        create_response = client.post("/tasks/", json=TASK_DATA)
        task_id = create_response.json()["id"]

        # Partial update (only one field)
        response = client.put(f"/tasks/{task_id}", json={"priority": 5})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["priority"] == 5
        # Original values preserved
        assert response.json()["title"] == TASK_DATA["title"]

    def test_update_not_found(self, client):
        """Test updating non-existent task."""
        response = client.put("/tasks/99999", json={"title": "test"})
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteTask:
    """Tests for deleting tasks."""

    def test_delete_success(self, client):
        """Test deleting task successfully."""
        # Create item first
        create_response = client.post("/tasks/", json=TASK_DATA)
        task_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deleted
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_not_found(self, client):
        """Test deleting non-existent task."""
        response = client.delete("/tasks/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
