import os
import unittest
from viztracer.report_builder import ReportBuilder


class TestReportBuilder(unittest.TestCase):
    def test_file(self):
        json_path = os.path.join(os.path.dirname(__file__), "data", "multithread.json")
        with open(json_path) as f:
            rb = ReportBuilder(f, verbose=0)
        rb.combine_json()
        result1 = rb.generate_json()
        rb.combine_json()
        result2 = rb.generate_json()
        self.assertEqual(result1, result2)

    def test_invalid(self):
        with self.assertRaises(TypeError):
            _ = ReportBuilder(123123)

    def test_too_many_entry(self):
        json_path = os.path.join(os.path.dirname(__file__), "data", "multithread.json")
        with open(json_path) as f:
            rb = ReportBuilder(f, verbose=1)
        rb.entry_number_threshold = 20
        # Coverage only
        rb.generate_json()

    def test_invalid_json(self):
        invalid_json_path = os.path.join(os.path.dirname(__file__), "data", "fib.py")
        with open(invalid_json_path) as f:
            with self.assertRaises(Exception):
                ReportBuilder(f, verbose=1)
