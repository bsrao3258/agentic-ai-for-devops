import sys
import unittest
from pathlib import Path

# Add the parent project directory to the import path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from log_analyzer import classify_error, get_recommendation


class TestLogAnalyzer(unittest.TestCase):
    def test_timeout(self):
        self.assertEqual(classify_error("Connection timeout"), "TIMEOUT")

    def test_null_pointer(self):
        self.assertEqual(
            classify_error("Null pointer exception"),
            "NULL_POINTER",
        )

    def test_unknown_error(self):
        self.assertEqual(classify_error("Disk quota exceeded"), "UNKNOWN")

    def test_timeout_recommendation(self):
        self.assertIn("network", get_recommendation("TIMEOUT").lower())


if __name__ == "__main__":
    unittest.main()
