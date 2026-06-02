from fastapi import status


def test_get_activities_returns_activity_data(client):
    # Arrange
    # No additional setup needed, using default client fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "description" in payload["Chess Club"]
    assert "schedule" in payload["Chess Club"]
    assert "participants" in payload["Chess Club"]


def test_signup_adds_participant(client):
    # Arrange
    email = "newstudent@example.com"

    # Act
    response = client.post("/activities/Chess%20Club/signup?email={}".format(email))

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_returns_bad_request(client):
    # Arrange
    email = "duplicate@example.com"
    signup = client.post("/activities/Programming%20Class/signup?email={}".format(email))
    assert signup.status_code == status.HTTP_200_OK

    # Act
    duplicate = client.post("/activities/Programming%20Class/signup?email={}".format(email))

    # Assert
    assert duplicate.status_code == status.HTTP_400_BAD_REQUEST
    assert duplicate.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_participant(client):
    # Arrange
    email = "removeme@example.com"
    signup = client.post("/activities/Gym%20Class/signup?email={}".format(email))
    assert signup.status_code == status.HTTP_200_OK

    # Act
    remove = client.delete("/activities/Gym%20Class/participants?email={}".format(email))

    # Assert
    assert remove.status_code == status.HTTP_200_OK
    assert remove.json()["message"] == f"Unregistered {email} from Gym Class"

    activities = client.get("/activities").json()
    assert email not in activities["Gym Class"]["participants"]
