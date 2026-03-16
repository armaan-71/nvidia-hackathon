import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_drafter_agent():
    print("📝 Testing Drafting Agent...")
    print("=" * 60)
    
    # 1. Ensure context exists (ingest bio if not already done)
    # We assume ingestion was done in previous tests, but for a fresh test:
    print("📄 Step 1: Ingesting nonprofit bio for RAG context...")
    try:
        with open("test_nonprofit_bio.md", "rb") as f:
            ingest_response = requests.post(
                f"{BASE_URL}/ingest",
                files={"file": ("test_nonprofit_bio.md", f)}
            )
        print(f"  ✅ {ingest_response.json().get('message', 'Ingested')}")
    except Exception as e:
        print(f"  ⚠️ Ingest failed (maybe file missing?), proceeding: {e}")

    print()

    # 2. Ask Drafter to generate a proposal
    print("✍️ Step 2: Asking Drafter to generate a proposal outline...")
    grant_details = "The Pacific Salmon Foundation is accepting proposals for salmon habitat restoration projects in British Columbia and the Pacific Northwest. Grant amounts: $25k-$100k. Deadline: June 2026."
    payload = {
        "message": f"Draft a proposal outline for this grant: {grant_details}",
        "session_id": "test_drafter_session"
    }

    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/api/agent/chat", json=payload, timeout=60)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Agent Responded in {duration:.2f}s")
            print(f"\n🤖 Draft Message:\n{data['message']}")
            print(f"\n📊 Active Agent: {data['active_agent']}")
            print(f"🔗 Suggested Actions: {data['suggested_actions']}")
        else:
            print(f"  ❌ Error: {response.status_code}")
            print(f"  {response.text}")
            
    except Exception as e:
        print(f"  ❌ Request failed: {e}")

if __name__ == "__main__":
    print("Ensuring server is running at http://localhost:8000...")
    print()
    test_drafter_agent()
