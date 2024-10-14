import unittest
from flask import Flask, json
from app import app, crawl_webpage  # Import your app and function

class WebCrawlerTestCase(unittest.TestCase):
    # Set up the Flask app for testing
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test the successful API response
    def test_crawl_success(self):
        # Mock request data
        request_data = {
            "url": "https://example.com",
            "depth": 1
        }

        # Make POST request to /crawl endpoint
        response = self.app.post('/crawl', data=json.dumps(request_data),
                                 content_type='application/json')

        # Assert the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains 'crawled_links' field
        data = json.loads(response.data)
        self.assertIn("crawled_links", data)

    # Test for invalid input: missing URL or depth
    def test_invalid_input(self):
        # Request missing the 'url'
        request_data = {
            "depth": 2
        }
        response = self.app.post('/crawl', data=json.dumps(request_data),
                                 content_type='application/json')

        # Assert that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, 400)

        # Assert that the response contains an error message
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Please provide both 'url' and 'depth'.")

    # Test for invalid depth value
    def test_invalid_depth(self):
        request_data = {
            "url": "https://example.com",
            "depth": "invalid_depth"  # Invalid depth
        }
        response = self.app.post('/crawl', data=json.dumps(request_data),
                                 content_type='application/json')

        # Assert that the response status code is 500 Internal Server Error
        self.assertEqual(response.status_code, 500)

        # Assert the error message
        data = json.loads(response.data)
        self.assertIn("error", data)

    # Test crawling functionality (basic function test without Flask)
    def test_crawler_function(self):
        # Test a shallow crawl (depth 1) on a mock URL
        url = "https://example.com"
        crawled_links = crawl_webpage(url, 1)
        self.assertIsInstance(crawled_links, set)  # Ensure it returns a set
        self.assertIn(url, crawled_links)          # Ensure the root URL is included

if __name__ == '__main__':
    unittest.main()

