import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app

client = TestClient(app)

@patch('main.YoutubeDL')
def test_process_video_age_restricted(mock_youtube_dl):
    # Configure the mock to simulate an age-restricted video
    mock_ydl_instance = MagicMock()
    mock_ydl_instance.extract_info.return_value = {
        'age_limit': 18,
        'title': 'Test Video',
        'thumbnail': 'http://example.com/thumbnail.jpg',
        'duration_string': '1:00',
        'formats': []
    }
    mock_youtube_dl.return_value.__enter__.return_value = mock_ydl_instance

    # Make the request to the endpoint
    response = client.post("/api/process-video", params={"url": "http://example.com/video"})

    # Assert that the response is a 400 error with the correct message
    assert response.status_code == 400
    assert response.json() == {'detail': 'Age-restricted content'}
