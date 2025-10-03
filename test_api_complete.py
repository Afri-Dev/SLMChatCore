"""
Quick test script for the FAQ API
Run this to verify the API is working before integrating with Flutter
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n🏥 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_stats():
    """Test stats endpoint"""
    print("\n📊 Testing /stats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=5)
        print(f"✅ Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_faq_query(question, top_k=3, min_score=0.0):
    """Test FAQ query endpoint"""
    print(f"\n❓ Testing /faq with question: '{question}'")
    try:
        payload = {
            "question": question,
            "top_k": top_k,
            "min_score": min_score
        }
        response = requests.post(
            f"{BASE_URL}/faq",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=15
        )
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📋 Query: {data['query']}")
            print(f"📊 Total Results: {data['total_results']}")
            if data.get('message'):
                print(f"⚠️  Message: {data['message']}")
            
            print("\n🔍 Results:")
            for i, result in enumerate(data['results'], 1):
                print(f"\n  {i}. [{result['category']}] Score: {result['score']:.2%}")
                print(f"     Q: {result['question']}")
                print(f"     A: {result['answer']}")
        else:
            print(f"❌ Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 FAQ API Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health()))
    
    # Test 2: Stats
    results.append(("Stats", test_stats()))
    
    # Test 3: FAQ queries
    test_questions = [
        "What is anxiety?",
        "How do I manage stress?",
        "What causes depression?",
        "How can I improve my mental health?",
    ]
    
    for question in test_questions:
        results.append((f"Query: {question[:30]}...", test_faq_query(question)))
    
    # Summary
    print("\n" + "=" * 60)
    print("📝 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is ready for Flutter integration.")
    else:
        print("⚠️  Some tests failed. Check the API server.")

if __name__ == "__main__":
    main()
