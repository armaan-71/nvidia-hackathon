import requests
import time

BASE_URL = "http://localhost:8000"
TEST_FILE = "test_nonprofit_bio.md"

def test_health():
    print("Checking API health...")
    response = requests.get(f"{BASE_URL}/")
    response.raise_for_status()
    data = response.json()
    assert data["status"] == "Scout API is live", f"Unexpected status: {data['status']}"
    print(f"Status: {data}\n")

def test_ingest():
    print(f"Uploading {TEST_FILE} to /ingest...")
    with open(TEST_FILE, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/ingest", files=files)
    
    if response.status_code != 200:
        print(f"Server Error: {response.text}")
    
    response.raise_for_status()
    data = response.json()
    assert "message" in data, f"Ingestion failed: {data}"
    print(f"Server Response: {data}\n")

def test_search(query):
    print(f"Searching for: '{query}'...")
    response = requests.get(f"{BASE_URL}/search", params={"q": query})
    response.raise_for_status()
    data = response.json()
    results = data.get("results", [])
    
    assert len(results) > 0, f"No results found for query: {query}"
    print(f"Found {len(results)} relevant chunks:")
    for i, res in enumerate(results):
        print(f"--- Result {i+1} (Distance: {res['distance']:.4f}) ---")
        print(f"{res['text'][:200]}...\n")

if __name__ == "__main__":
    try:
        test_health()
        test_ingest()
        
        # Verify indexing with a small retry loop instead of a hard sleep
        print("Verifying indexing...")
        indexed = False
        for _ in range(5):
            response = requests.get(f"{BASE_URL}/search", params={"q": "EcoStream"})
            if response.status_code == 200 and len(response.json().get("results", [])) > 0:
                indexed = True
                break
            print("Indexing in progress, waiting...")
            time.sleep(1)
            
        if not indexed:
            print("Failed to verify indexing after 5 seconds.")
        
        test_search("What does EcoStream do for salmon?")
        test_search("Who is the director of the organization?")
        print("✅ All RAG tests passed!")
    except Exception as e:
        print(f"❌ Testing failed: {e}")
        print("Tip: Make sure the FastAPI server is running with 'python backend/main.py'")
