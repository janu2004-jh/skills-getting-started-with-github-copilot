from urllib.parse import quote


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200

    activities = response.json()
    assert "Chess Club" in activities

    chess = activities["Chess Club"]
    assert chess["description"] == "Learn strategies and compete in chess tournaments"
    assert chess["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert isinstance(chess["participants"], list)
    assert "michael@mergington.edu" in chess["participants"]


def test_signup_for_activity(client):
    email = "test.user@mergington.edu"
    response = client.post(
        f"/activities/{quote('Chess Club')}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_message(client):
    email = "michael@mergington.edu"
    response = client.post(
        f"/activities/{quote('Chess Club')}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"{email} is already registered for Chess Club"

    activities = client.get("/activities").json()
    assert activities["Chess Club"]["participants"].count(email) == 1


def test_remove_participant(client):
    email = "daniel@mergington.edu"
    response = client.delete(
        f"/activities/{quote('Chess Club')}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]
