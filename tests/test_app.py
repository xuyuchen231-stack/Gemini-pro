import unittest
from fastapi.testclient import TestClient
from app import app, ORIGIN

class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_official_pages(self):
        data = self.client.get("/api/state").json()
        self.assertEqual(set(data["official"]), {"google_one", "google_play", "google_account"})
        self.assertTrue(all(value.startswith("https://") for value in data["official"].values()))

    def test_reject_post_without_auth(self):
        response = self.client.post("/api/note", json={"label": "test"}, headers={"origin": ORIGIN})
        self.assertEqual(response.status_code, 403)

    def test_reject_wrong_origin(self):
        response = self.client.post("/api/note", json={"label": "test"}, headers={"origin": "https://evil.example","x-session-token": "incorrect"})
        self.assertEqual(response.status_code, 403)

if __name__ == "__main__":
    unittest.main()
