import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_scorer_agent():
    print("🔢 Testing Scorer Agent...")
    print("=" * 60)
    
    # Mock Analysis result (normally this would come from the Analyzer Agent)
    mock_analysis = """
    **Eligibility Analysis for Pacific Salmon Foundation Grant**
    - Geographic Focus: MEETS (PNW based)
    - Nonprofit Status: MEETS (501c3)
    - Focus Area: MEETS (Salmon conservation)
    - Project Requirements: MEETS (Community engagement present)
    - Funding Capacity: MEETS (Budget matches range)
    Overall Assessment: Perfect match.
    """
    
    print("🧠 Asking Scorer to calculate match score...")
    payload = {
        "message": f"Please score this analysis: {mock_analysis}",
        "session_id": "test_scorer_session"
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/api/agent/chat", json=payload, timeout=60)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Agent Responded in {duration:.2f}s")
            print(f"\n🤖 Score Report:\n{data['message']}")
            print(f"\n📊 Active Agent: {data['active_agent']}")
            
            agent_data = data.get("data", {})
            if "match_score" in agent_data:
                print(f"🎯 Stored Numeric Score: {agent_data['match_score']}")
        else:
            print(f"  ❌ Error: {response.status_code}")
            print(f"  {response.text}")
            
    except Exception as e:
        print(f"  ❌ Request failed: {e}")

if __name__ == "__main__":
    print("Ensuring server is running at http://localhost:8000...")
    print()
    test_scorer_agent()
