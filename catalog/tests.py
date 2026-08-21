import json
from django.test import TestCase, Client
from catalog.models import Course, Lesson


class CourseAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            code="TST01",
            title="Test Course",
            description="For testing",
            is_active=True,
        )

    # ========== TEST 1: Happy-path GET ==========
    def test_get_course_list(self):
        response = self.client.get("/api/courses/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)  # karena pakai pagination
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["code"], "TST01")

    # ========== TEST 2: Happy-path POST ==========
    def test_create_course_success(self):
        payload = {
            "code": "TST02",
            "title": "New Course",
            "description": "Created via test",
            "is_active": True,
        }
        response = self.client.post(
            "/api/courses/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["code"], "TST02")

    # ========== TEST 3: Invalid Input ==========
    def test_create_course_duplicate_code(self):
        # TST01 sudah ada di setUp
        payload = {
            "code": "TST01",  # duplikat!
            "title": "Duplicate",
            "description": "Should fail",
            "is_active": True,
        }
        response = self.client.post(
            "/api/courses/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    # ========== TEST 4: Resource Not Found ==========
    def test_get_nonexistent_course(self):
        response = self.client.get("/api/courses/99999/")
        self.assertEqual(response.status_code, 404)