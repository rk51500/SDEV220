from django.test import TestCase


class RegistrationViewTests(TestCase):
    def test_form_page_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student Registration Form")

    def test_blank_name_and_id_show_errors(self):
        response = self.client.post("/", data={"student_name": "", "student_id": ""})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student Name is required.")
        self.assertContains(response, "Student ID is required.")

    def test_valid_submission_shows_results(self):
        response = self.client.post(
            "/",
            data={
                "student_name": "Ada Lovelace",
                "student_id": "S12345",
                "major": "Computer Science",
                "class_standing": "Sophomore",
                "programming_languages": ["Python", "JavaScript"],
                "graduation_year": "2028",
                "comments": "Excited to learn Django.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student Registration Summary")
        self.assertContains(response, "Ada Lovelace")
        self.assertContains(response, "Python, JavaScript")
