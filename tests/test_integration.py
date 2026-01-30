"""
Integration tests for the complete application workflow
"""
import pytest
from fastapi.testclient import TestClient


def test_complete_signup_and_unregister_workflow(client, reset_activities, sample_emails):
    """Test the complete workflow of signing up and then unregistering"""
    activity_name = "Basketball Club"
    email = sample_emails[0]
    
    # 1. Check initial state - no participants
    activities_response = client.get("/activities")
    initial_data = activities_response.json()
    assert email not in initial_data[activity_name]["participants"]
    initial_count = len(initial_data[activity_name]["participants"])
    
    # 2. Sign up for the activity
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200
    
    # 3. Verify signup worked
    activities_response = client.get("/activities")
    after_signup_data = activities_response.json()
    assert email in after_signup_data[activity_name]["participants"]
    assert len(after_signup_data[activity_name]["participants"]) == initial_count + 1
    
    # 4. Unregister from the activity
    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_response.status_code == 200
    
    # 5. Verify unregistration worked
    activities_response = client.get("/activities")
    final_data = activities_response.json()
    assert email not in final_data[activity_name]["participants"]
    assert len(final_data[activity_name]["participants"]) == initial_count


def test_multiple_students_same_activity(client, reset_activities, sample_emails):
    """Test multiple students signing up for the same activity"""
    activity_name = "Science Club"
    emails = sample_emails[:3]  # Use first 3 emails
    
    # Sign up all students
    for email in emails:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200
    
    # Verify all are registered
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    
    for email in emails:
        assert email in activities_data[activity_name]["participants"]
    
    # Remove one student
    response = client.delete(f"/activities/{activity_name}/unregister?email={emails[0]}")
    assert response.status_code == 200
    
    # Verify only that student was removed
    activities_response = client.get("/activities")
    final_data = activities_response.json()
    
    assert emails[0] not in final_data[activity_name]["participants"]
    assert emails[1] in final_data[activity_name]["participants"]
    assert emails[2] in final_data[activity_name]["participants"]


def test_student_multiple_activities(client, reset_activities, sample_emails):
    """Test one student signing up for multiple activities"""
    email = sample_emails[0]
    activities = ["Drama Club", "Art Workshop", "Math Olympiad"]
    
    # Sign up for multiple activities
    for activity in activities:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
    
    # Verify student is in all activities
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    
    for activity in activities:
        assert email in activities_data[activity]["participants"]
    
    # Unregister from one activity
    response = client.delete(f"/activities/{activities[0]}/unregister?email={email}")
    assert response.status_code == 200
    
    # Verify student is removed only from that activity
    activities_response = client.get("/activities")
    final_data = activities_response.json()
    
    assert email not in final_data[activities[0]]["participants"]
    assert email in final_data[activities[1]]["participants"] 
    assert email in final_data[activities[2]]["participants"]


def test_activity_data_integrity(client, reset_activities):
    """Test that activity data structure remains intact after operations"""
    activity_name = "Programming Class"
    email = "new_student@mergington.edu"
    
    # Get initial activity data
    response = client.get("/activities")
    initial_data = response.json()[activity_name]
    
    # Perform signup
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Check data integrity
    response = client.get("/activities")
    after_signup_data = response.json()[activity_name]
    
    # All fields should still be present and unchanged except participants
    assert after_signup_data["description"] == initial_data["description"]
    assert after_signup_data["schedule"] == initial_data["schedule"] 
    assert after_signup_data["max_participants"] == initial_data["max_participants"]
    
    # Participants should have the new email added
    expected_participants = initial_data["participants"] + [email]
    assert set(after_signup_data["participants"]) == set(expected_participants)


def test_error_handling_edge_cases(client, reset_activities):
    """Test various edge cases and error conditions"""
    # Test with URL-encoded activity names containing spaces
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    
    # Test with empty email (this should ideally be validated)
    response = client.post("/activities/Chess Club/signup?email=")
    # The behavior depends on how the API handles empty emails
    # For now, we just check it doesn't crash
    assert response.status_code in [200, 400, 422]
    
    # Test unregistering from activity with special characters in name
    response = client.delete("/activities/Chess%20Club/unregister?email=test@mergington.edu")
    assert response.status_code == 200