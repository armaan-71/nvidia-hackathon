import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_analyzer_agent():
    print("🔬 Testing Analyzer Agent...")
    print("=" * 60)
    
    # The Analyzer needs context from uploaded docs, so we first ingest
    print("📄 Step 1: Ingesting nonprofit bio for RAG context...")
    with open("test_nonprofit_bio.md", "rb") as f:
        ingest_response = requests.post(
            f"{BASE_URL}/ingest",
            files={"file": ("test_nonprofit_bio.md", f)}
        )
    if ingest_response.status_code == 200:
        print(f"  ✅ {ingest_response.json().get('message', 'Ingested')}")
    else:
        print(f"  ⚠️ Ingest returned {ingest_response.status_code}: {ingest_response.text}")
    
    print()
    
    # Now test the Analyzer with a grant description
    print("🧠 Step 2: Asking Analyzer to evaluate eligibility...")
    payload = {
        "message": "Analyze our eligibility for this grant: The Pacific Salmon Foundation is accepting proposals for salmon habitat restoration projects in British Columbia and the Pacific Northwest. Eligible applicants must be registered nonprofits focused on freshwater ecosystem conservation. Projects should demonstrate community engagement and measurable environmental impact. Grant amounts range from $25,000 to $100,000. Deadline: June 30, 2026.",
        "session_id": "test_analyzer_session"
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/api/agent/chat", json=payload, timeout=120)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Agent Responded in {duration:.2f}s")
            print(f"\n🤖 Analysis:\n{data['message']}")
            print(f"\n📊 Active Agent: {data['active_agent']}")
            print(f"🔗 Suggested Actions: {data['suggested_actions']}")
            
            agent_data = data.get("data", {})
            if agent_data.get("topics_searched"):
                print(f"🔍 Topics Searched: {agent_data['topics_searched']}")
        else:
            print(f"  ❌ Error: {response.status_code}")
            print(f"  {response.text}")
            
    except Exception as e:
        print(f"  ❌ Request failed: {e}")

if __name__ == "__main__":
    print("Ensuring server is running at http://localhost:8000...")
    print()
    test_analyzer_agent()
