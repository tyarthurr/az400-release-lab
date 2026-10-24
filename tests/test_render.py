import json
import unittest
from pathlib import Path

from src.render import render_page


class RenderTests(unittest.TestCase):
    def test_supported_statuses(self):
        for status in ("operational", "degraded", "outage"):
            with self.subTest(status=status):
                page = render_page({"service": "Demo API", "status": status})
                self.assertIn(f"Status: {status}", page)

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            render_page({"service": "Demo API", "status": "unknown"})

    def test_service_name_is_html_escaped(self):
        page = render_page({
            "service": "<script>alert(1)</script>",
            "status": "operational",
        })
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_repository_data_builds(self):
        data = json.loads(
            Path("data/status.json").read_text(encoding="utf-8")
        )
        self.assertIn("</html>", render_page(data))


if __name__ == "__main__":
    unittest.main()