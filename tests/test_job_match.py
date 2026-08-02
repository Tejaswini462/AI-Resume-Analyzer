import unittest

from services.job_match import JobMatchService


class JobMatchServiceTestCase(unittest.TestCase):
    def test_match_returns_usable_recommendations(self):
        resume_text = """
        Senior Java Developer with strong Java programming skills and knowledge of Spring Boot, REST APIs, and microservices.
        """
        job_description = """
        We are hiring a Java Developer with strong Spring Boot, Java, REST APIs, and good knowledge of microservices.
        """

        result = JobMatchService().match_resume_to_job(resume_text, job_description)

        self.assertIn("match_percentage", result)
        self.assertIn("matching_skills", result)
        self.assertIn("missing_skills", result)
        self.assertIn("recommendations", result)
        self.assertGreaterEqual(result["match_percentage"], 0)
        self.assertTrue(result["recommendations"])
        self.assertIn("java", result["matching_skills"])
        self.assertIn("rest apis", result["matching_skills"])
        self.assertNotIn("and", result["matching_skills"])
        self.assertNotIn("skills", result["matching_skills"])
        self.assertNotIn("strong", result["matching_skills"])


if __name__ == "__main__":
    unittest.main()
