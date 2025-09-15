import subprocess
import pytest
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import signal
import time
import socket

# Find the supervisord process and kill it
def kill_supervisord():
    result = subprocess.run(['pgrep', 'supervisord'], capture_output=True, text=True)
    if result.stdout.strip():
        pid = int(result.stdout.strip())
        os.kill(pid, signal.SIGTERM)  # Send SIGTERM to terminate supervisord
        print(f"Sent SIGTERM to supervisord (PID {pid}). Waiting for it to stop...")

        # Wait for the process to terminate
        while True:
            result = subprocess.run(['pgrep', 'supervisord'], capture_output=True, text=True)
            if not result.stdout.strip():  # If no PID is found, the process has stopped
                print("Supervisord has stopped.")
                break
            time.sleep(0.5)  # Wait for 500ms before checking again
    else:
        print("Supervisord is not running.")

def wait_for_port(port, host="127.0.0.1", timeout=5):
    """Wait until the specified port is available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex((host, port)) != 0:  # Port is not in use
                return True
        time.sleep(0.5)
    return False

def start_supervisord():
    # Wait for port 8080 to become available
    if not wait_for_port(8080):
        print("Port 8080 is still in use. Cannot start supervisord.")
        return

    # Start supervisord as a background process
    subprocess.Popen(
        ['supervisord', '-c', '.devcontainer/llama.conf'],
        stdout=subprocess.DEVNULL,  # Suppress output
        stderr=subprocess.DEVNULL,  # Suppress error output
        preexec_fn=os.setpgrp  # Start the process in a new process group
    )
    print("Starting supervisord...")

    # Wait for supervisord to start
    for _ in range(10):  # Retry for up to 5 seconds (10 * 0.5s)
        result = subprocess.run(['pgrep', 'supervisord'], capture_output=True, text=True)
        if result.stdout.strip():  # If a PID is found, supervisord is running
            print("Supervisord is running.")
            return
        time.sleep(0.5)  # Wait for 500ms before checking again

    print("Failed to start supervisord within the timeout.")

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

    kill_supervisord()

    # Start the mock server in a separate thread
    server = HTTPServer(("127.0.0.1", 8080), MockServerRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()
    start_supervisord()
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


if __name__ == '__main__':
    start_supervisord()