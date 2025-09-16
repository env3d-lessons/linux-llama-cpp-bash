import subprocess
import pytest
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

@pytest.fixture(scope="module")
def start_mock_server():    

    # change to mock_curl
        
    subprocess.run(["sed", "-i", "s/curl/tests\\/mock_curl/g", "query.sh"], check=True)

    yield

    # curl
    subprocess.run(["sed", "-i", "s/tests\\/mock_curl/curl/g", "query.sh"], check=True)


def test_data_in_response(start_mock_server):
    # Run the query.sh script
    result = subprocess.run(["bash", "./query.sh", "test"], capture_output=True, text=True)    
    assert 'test' in result.stdout.strip()

def test_format_in_response(start_mock_server):
    # Run the query.sh script
    result = subprocess.run(["bash", "./query.sh", "test data"], capture_output=True, text=True)    
    assert 'test data' == result.stdout.strip()

def test_num_words(start_mock_server):
    # Run the query.sh script
    result = subprocess.run(["bash", "./query.sh", "test data"], capture_output=True, text=True)  
    r = result.stdout.split()
    print(r)
    assert len(r) == 2

def test_num_lines(start_mock_server):
    # Run the query.sh script
    result = subprocess.run(["bash", "./query.sh", "test \\\\n data"], capture_output=True, text=True)  
    r = result.stdout.splitlines()
    print(r)
    assert len(r) == 2

def test_no_argument(start_mock_server):
    # Run the query.sh script
    result = subprocess.run(["bash", "./query.sh"], capture_output=True, text=True)  
    r = result.stdout.strip().lower()
    assert 'error' in r
