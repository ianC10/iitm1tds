import json
import os
from http.server import BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Resolve the absolute path of students.json
            current_dir = os.path.dirname(__file__)
            json_path = os.path.join(current_dir, "students.json")

            # Load student data from the JSON file
            with open(json_path, "r") as file:
                students = json.load(file)

            # Parse the query parameters
            query = self.path.split("?")
            if len(query) > 1 and query[0] == "/api":
                params = query[1].split("&")
                names = [param.split("=")[1] for param in params if param.startswith("name=")]

                # Fetch marks for the given names
                marks = [student["marks"] for student in students if student["name"] in names]
                marks.reverse()  # Reverse the marks array

                result = {"marks": marks}

                # Return the response
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")  # Enable CORS
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))
            else:
                # Return a 404 response for invalid paths
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            # Handle exceptions and return a 500 response
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"Internal Server Error: {str(e)}".encode("utf-8"))

    def do_OPTIONS(self):
        # Handle preflight CORS requests
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.end_headers()
