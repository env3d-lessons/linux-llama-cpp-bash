import subprocess
import pytest
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

# Define a mock HTTP server
class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Respond with a mocked JSON stream
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = (
            'data: {"choices":[{"delta":{"content":"Data"}}]}\n'
            'data: {"choices":[{"delta":{"content":" formats"}}]}\n'
        )
        self.wfile.write(response.encode("utf-8"))

@pytest.fixture(scope="module")
def start_mock_server():
    # Check if port 8080 is already in use
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if sock.connect_ex(("127.0.0.1", 8080)) == 0:
            yield
        else:
            # Start the mock server in a separate thread
            server = HTTPServer(("127.0.0.1", 8080), MockServerRequestHandler)
            thread = threading.Thread(target=server.serve_forever)
            thread.daemon = True
            thread.start()
            yield
            server.shutdown()
            thread.join()

def test_query_with_mock_server(start_mock_server):
    # Run the query.sh script
    result = subprocess.run(["bash", "./query.sh"], capture_output=True, text=True)    
    assert result.stdout.strip() == "Data formats"