import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Load the student data from a JSON file
with open("students.json", "r") as file:
    students = json.load(file)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL and query parameters
        url = urlparse(self.path)
        if url.path == "/api":
            query = parse_qs(url.query)
            names = query.get("name", [])

            # Find marks for the given names
            result = {"marks": [student["marks"] for student in students if student["name"] in names]}

            # Respond with a JSON object
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")  # Enable CORS
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
        else:
            # Respond with a 404 for unsupported paths
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Handle preflight CORS requests
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()
