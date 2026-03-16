import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_discovery_agent():
    print("🚀 Testing Discovery Agent...")
    payload = {
        "message": "I am looking for environmental grants in the Pacific Northwest related to salmon conservation.",
        "session_id": "test_session_123"
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/api/agent/chat", json=payload, timeout=30)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent Responded in {duration:.2f}s")
            print(f"\n🤖 Agent Message:\n{data['message']}")
            print(f"\n📊 Active Agent: {data['active_agent']}")
            print(f"🔗 Suggested Actions: {data['suggested_actions']}")
            
            # Check if we got grant data
            grants = data.get("data", {}).get("grants", [])
            if grants:
                print(f"📦 Found {len(grants)} potential results.")
            else:
                print("⚠️ No structured grant data found in response.")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("Ensuring server is running at http://localhost:8000...")
    test_discovery_agent()
