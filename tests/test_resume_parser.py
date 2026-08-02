import unittest

from services.parser import ResumeParser


class ResumeParserTestCase(unittest.TestCase):
    def test_parse_resume_text_extracts_sections(self):
        sample = """
        John Doe
        john.doe@example.com
        +1 555-123-4567
        Skills: Python, Flask, SQL, MySQL, Git
        Education: B.Tech in Computer Science
        Experience: Senior Software Engineer at Acme
        Projects: AI Resume Analyzer
        Certifications: AWS Cloud Practitioner
        """

        result = ResumeParser().parse_resume_text(sample)

        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["email"], "john.doe@example.com")
        self.assertEqual(result["phone"], "+1 555-123-4567")
        self.assertIn("python", result["skills"].lower())
        self.assertIn("flask", result["skills"].lower())
        self.assertIn("B.Tech", result["education"])
        self.assertIn("Senior Software Engineer", result["experience"])
        self.assertIn("AI Resume Analyzer", result["projects"])
        self.assertIn("AWS Cloud Practitioner", result["certifications"])


if __name__ == "__main__":
    unittest.main()
