import subprocess
import pytest
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import signal
import time
import socket

# Define a mock HTTP server
class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Respond with a mocked JSON stream
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = (
            'data: {"choices":[{"finish_reason":null,"index":0,"delta":{"content":"Data"}}],"created":1757973060,"id":"chatcmpl-Q9FZ3pGOdFQLtbXzymVYAVh2UvV0yBU5","model":"qwen2.5-0.5b-instruct","system_fingerprint":"b6479-b907255f","object":"chat.completion.chunk"}\n'
            'data: {"choices":[{"finish_reason":null,"index":0,"delta":{"content":" \\n "}}],"created":1757973060,"id":"chatcmpl-Q9FZ3pGOdFQLtbXzymVYAVh2UvV0yBU5","model":"qwen2.5-0.5b-instruct","system_fingerprint":"b6479-b907255f","object":"chat.completion.chunk"}\n'
            'data: {"choices":[{"finish_reason":null,"index":0,"delta":{"content":" formats"}}],"created":1757973060,"id":"chatcmpl-Q9FZ3pGOdFQLtbXzymVYAVh2UvV0yBU5","model":"qwen2.5-0.5b-instruct","system_fingerprint":"b6479-b907255f","object":"chat.completion.chunk"}\n'
        )
        self.wfile.write(response.encode("utf-8"))

@pytest.fixture(scope="module")
def start_mock_server():    

    # Start the mock server in a separate thread
    
    # Change port 8080 to 8081 in query.sh
    subprocess.run(["sed", "-i", "s/:8080/:8081/g", "query.sh"], check=True)

    # Start the mock server in a separate thread on 8081
    server = HTTPServer(("127.0.0.1", 8081), MockServerRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()

    # Restore query.sh to use 8080
    subprocess.run(["sed", "-i", "s/:8081/:8080/g", "query.sh"], check=True)

    thread.join()        
    

def test_Data_in_response(start_mock_server):
    # Run the query.sh script
    result = subprocess.run(["bash", "./query.sh", "test"], capture_output=True, text=True)    
    assert 'Data' in result.stdout.strip()

def test_Format_in_response(start_mock_server):
    # Run the query.sh script
    result = subprocess.run(["bash", "./query.sh", "test"], capture_output=True, text=True)    
    assert 'format' in result.stdout.strip()    

def test_num_words(start_mock_server):
    # Run the query.sh script
    result = subprocess.run(["bash", "./query.sh", "test"], capture_output=True, text=True)  
    r = result.stdout.split()
    print(r)
    assert len(r) == 2

def test_num_lines(start_mock_server):
    # Run the query.sh script
    result = subprocess.run(["bash", "./query.sh", "test"], capture_output=True, text=True)  
    r = result.stdout.splitlines()
    print(r)
    assert len(r) == 2

def test_no_argument(start_mock_server):
    # Run the query.sh script
    result = subprocess.run(["bash", "./query.sh"], capture_output=True, text=True)  
    r = result.stdout.strip().lower()
    assert 'error' in r
