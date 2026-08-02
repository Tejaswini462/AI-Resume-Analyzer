import unittest

from services.ats_score import ATSScoreService


class ATSScoreServiceTestCase(unittest.TestCase):
    def test_score_reduces_when_resume_is_incomplete(self):
        parsed_resume = {
            "name": "John Doe",
            "email": "",
            "phone": "",
            "skills": "",
            "education": "",
            "experience": "",
            "projects": "",
            "certifications": "",
        }

        result = ATSScoreService().calculate_score(parsed_resume)

        self.assertLess(result["overall_score"], 100)
        self.assertIn("contact_information", result["section_scores"])
        self.assertIn("Missing contact details.", result["weaknesses"])
        self.assertIn("Missing technical skill keywords.", result["weaknesses"])


if __name__ == "__main__":
    unittest.main()
