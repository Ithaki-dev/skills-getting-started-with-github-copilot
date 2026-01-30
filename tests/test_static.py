"""
Tests for static file serving and frontend functionality
"""
import pytest
from fastapi.testclient import TestClient


def test_static_files_served(client):
    """Test that static files are properly served"""
    # Test main HTML file
    response = client.get("/static/index.html")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Mergington High School" in response.text
    
    # Test CSS file
    response = client.get("/static/styles.css")
    assert response.status_code == 200
    assert "text/css" in response.headers.get("content-type", "")
    
    # Test JavaScript file
    response = client.get("/static/app.js")
    assert response.status_code == 200
    assert "javascript" in response.headers.get("content-type", "").lower()


def test_root_redirects_to_static_index(client):
    """Test that the root URL serves the static index page"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"


def test_nonexistent_static_file_404(client):
    """Test that requesting a nonexistent static file returns 404"""
    response = client.get("/static/nonexistent.html")
    assert response.status_code == 404


def test_html_contains_expected_elements(client):
    """Test that the HTML file contains expected form elements and structure"""
    response = client.get("/static/index.html")
    html_content = response.text
    
    # Check for essential form elements
    assert 'id="signup-form"' in html_content
    assert 'id="email"' in html_content
    assert 'id="activity"' in html_content
    assert 'type="email"' in html_content
    
    # Check for activity display elements
    assert 'id="activities-list"' in html_content
    assert 'id="activity-card-template"' in html_content
    
    # Check for script inclusion
    assert 'src="app.js"' in html_content


def test_javascript_contains_expected_functions(client):
    """Test that the JavaScript file contains expected functionality"""
    response = client.get("/static/app.js")
    js_content = response.text
    
    # Check for key functions and endpoints
    assert "fetchActivities" in js_content
    assert "removeParticipant" in js_content
    assert "/activities" in js_content
    assert "signup" in js_content
    assert "unregister" in js_content
    
    # Check for DOM manipulation
    assert "getElementById" in js_content
    assert "addEventListener" in js_content


def test_css_contains_expected_styles(client):
    """Test that the CSS file contains expected styling"""
    response = client.get("/static/styles.css")
    css_content = response.text
    
    # Check for key styling classes
    assert ".participants-list" in css_content
    assert ".delete-participant" in css_content
    assert ".activity-card" in css_content
    assert ".form-group" in css_content
    
    # Check for responsive design elements
    assert "flex" in css_content
    assert "hover" in css_content