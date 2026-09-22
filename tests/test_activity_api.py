from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def build_activity_path(activity_name: str, suffix: str = "") -> str:
    encoded_name = activity_name.replace(" ", "%20")
    return f"/activities/{encoded_name}{suffix}"


def test_student_can_signup_and_then_unregister():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    signup_response = client.post(f"{build_activity_path(activity_name, '/signup')}?email={email}")
    delete_response = client.delete(build_activity_path(activity_name, f"/participants/{email}"))
    all_activities = client.get("/activities").json()

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert email not in all_activities[activity_name]["participants"]


def test_deleting_missing_participant_returns_not_found():
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(build_activity_path(activity_name, f"/participants/{email}"))

    # Assert
    assert response.status_code == 404
