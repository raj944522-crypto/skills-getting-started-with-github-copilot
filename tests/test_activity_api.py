from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_student_can_signup_and_then_unregister():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name.replace(' ', '%20')}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        f"/activities/{activity_name.replace(' ', '%20')}/participants/{email}"
    )
    assert delete_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_deleting_missing_participant_returns_not_found():
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name.replace(' ', '%20')}/participants/{email}"
    )
    assert response.status_code == 404
