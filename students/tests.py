from django.test import TestCase

# Create your tests here.
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from students.models import Student

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_student():
    def _create_student(name="John Doe", email="john@example.com", age=20):
        return Student.objects.create(name=name, email=email, age=age)
    return _create_student

@pytest.mark.django_db
class TestStudentAPI:

    def test_create_student(self, api_client):
        url = reverse('student-list')
        data = {"name": "Alice", "email": "alice@example.com", "age": 22}
        response = api_client.post(url, data, format='json')
        assert response.status_code == 201
        assert response.data['name'] == "Alice"

    def test_list_students(self, api_client, create_student):
        create_student()
        url = reverse('student-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_retrieve_student(self, api_client, create_student):
        student = create_student()
        url = reverse('student-detail', args=[student.id])
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['name'] == student.name

    def test_update_student(self, api_client, create_student):
        student = create_student()
        url = reverse('student-detail', args=[student.id])
        data = {"name": "Updated", "email": student.email, "age": 25}
        response = api_client.put(url, data, format='json')
        assert response.status_code == 200
        assert response.data['name'] == "Updated"

    def test_delete_student(self, api_client, create_student):
        student = create_student()
        url = reverse('student-detail', args=[student.id])
        response = api_client.delete(url)
        assert response.status_code == 204
        assert Student.objects.count() == 0
