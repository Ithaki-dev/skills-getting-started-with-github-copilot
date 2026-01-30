"""
Tests for the main API endpoints
"""
import pytest
from fastapi.testclient import TestClient


def test_root_redirect(client):
    """Test that root endpoint redirects to static index.html"""
    response = client.get("/")
    assert response.status_code == 200  # After redirect
    # Note: In test client, redirects are followed automatically


def test_get_activities(client, reset_activities):
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    
    # Check that expected activities are present
    expected_activities = ["Chess Club", "Programming Class", "Gym Class", "Soccer Team", 
                          "Basketball Club", "Drama Club", "Art Workshop", "Math Olympiad", 
                          "Science Club"]
    
    for activity in expected_activities:
        assert activity in data
        
    # Check structure of an activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_for_activity_success(client, reset_activities, sample_emails):
    """Test successful signup for an activity"""
    activity_name = "Chess Club"
    email = sample_emails[0]
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]
    
    # Verify the student was actually added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity_name]["participants"]


def test_signup_for_nonexistent_activity(client, sample_emails):
    """Test signup for an activity that doesn't exist"""
    email = sample_emails[0]
    
    response = client.post(f"/activities/Nonexistent Activity/signup?email={email}")
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_registration(client, reset_activities):
    """Test that duplicate registration returns an error"""
    activity_name = "Chess Club"
    # Use an email that's already registered (from initial data)
    email = "michael@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_unregister_from_activity_success(client, reset_activities, sample_emails):
    """Test successful unregistration from an activity"""
    activity_name = "Chess Club"
    email = sample_emails[0]
    
    # First, sign up the student
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200
    
    # Then unregister
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]
    
    # Verify the student was actually removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_from_nonexistent_activity(client, sample_emails):
    """Test unregistration from an activity that doesn't exist"""
    email = sample_emails[0]
    
    response = client.delete(f"/activities/Nonexistent Activity/unregister?email={email}")
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_not_registered_student(client, reset_activities, sample_emails):
    """Test unregistering a student who isn't registered for the activity"""
    activity_name = "Soccer Team"  # This activity has no participants initially
    email = sample_emails[0]
    
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 400
    
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"].lower()


def test_unregister_existing_participant(client, reset_activities):
    """Test unregistering an existing participant"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # This email is in the initial data
    
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    
    # Verify the student was removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data[activity_name]["participants"]