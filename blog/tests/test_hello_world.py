import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_hello_world(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert b'Hello, World!' in response.content