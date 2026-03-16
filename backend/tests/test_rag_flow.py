import requests
import time

BASE_URL = "http://localhost:8000"
TEST_FILE = "test_nonprofit_bio.md"

def test_health():
    print("Checking API health...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.json()}\n")

def test_ingest():
    print(f"Uploading {TEST_FILE} to /ingest...")
    with open(TEST_FILE, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/ingest", files=files)
    print(f"Server Response: {response.json()}\n")

def test_search(query):
    print(f"Searching for: '{query}'...")
    response = requests.get(f"{BASE_URL}/search", params={"q": query})
    results = response.json().get("results", [])
    print(f"Found {len(results)} relevant chunks:")
    for i, res in enumerate(results):
        print(f"--- Result {i+1} (Distance: {res['distance']:.4f}) ---")
        print(f"{res['text'][:200]}...\n")

if __name__ == "__main__":
    try:
        test_health()
        test_ingest()
        time.sleep(2) # Brief wait for ChromaDB to settle
        test_search("What does EcoStream do for salmon?")
        test_search("Who is the director of the organization?")
    except Exception as e:
        print(f"Testing failed: {e}")
        print("Tip: Make sure the FastAPI server is running with 'python backend/main.py'")
