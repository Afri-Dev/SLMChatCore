import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_api():
    """Test the FAQ API endpoints"""
    print("Testing Mental Health FAQ API...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print("Make sure the API server is running!")
        return
    
    # Test 2: Root endpoint
    print("2. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    
    # Test 3: Stats endpoint
    print("3. Testing stats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    
    # Test 4: FAQ query
    print("4. Testing FAQ query...")
    test_questions = [
        "What is anxiety?",
        "How can I deal with depression?",
        "What are panic attacks?",
        "How to manage stress?",
        "I feel overwhelmed"
    ]
    
    for question in test_questions:
        print(f"\nQuestion: '{question}'")
        try:
            payload = {
                "question": question,
                "top_k": 3,
                "min_score": 0.1
            }
            
            response = requests.post(
                f"{BASE_URL}/faq", 
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result['success']}")
                if result.get('message'):
                    print(f"Message: {result['message']}")
                
                print(f"Found {len(result['results'])} results:")
                for i, res in enumerate(result['results'], 1):
                    print(f"  {i}. Score: {res['score']:.3f}")
                    print(f"     Q: {res['question'][:60]}...")
                    print(f"     A: {res['answer'][:100]}...")
                    print()
            else:
                print(f"Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        
        print("-" * 40)
    
    # Test 5: Error handling
    print("\n5. Testing error handling...")
    
    # Empty question
    try:
        response = requests.post(
            f"{BASE_URL}/faq", 
            json={"question": ""},
            headers={"Content-Type": "application/json"}
        )
        print(f"Empty question - Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def benchmark_api():
    """Simple benchmark test"""
    print("\nBenchmarking API response times...")
    print("=" * 50)
    
    questions = [
        "What is depression?",
        "How to handle anxiety?",
        "What are the symptoms of PTSD?",
        "How to improve mental health?",
        "What is therapy?"
    ]
    
    total_time = 0
    successful_requests = 0
    
    for i, question in enumerate(questions, 1):
        try:
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/faq",
                json={"question": question, "top_k": 3},
                headers={"Content-Type": "application/json"}
            )
            end_time = time.time()
            
            response_time = end_time - start_time
            total_time += response_time
            
            if response.status_code == 200:
                successful_requests += 1
                result = response.json()
                top_score = result['results'][0]['score'] if result['results'] else 0
                print(f"Request {i}: {response_time:.3f}s (top score: {top_score:.3f})")
            else:
                print(f"Request {i}: FAILED - {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Request {i}: ERROR - {e}")
    
    if successful_requests > 0:
        avg_time = total_time / successful_requests
        print(f"\nAverage response time: {avg_time:.3f}s")
        print(f"Successful requests: {successful_requests}/{len(questions)}")

if __name__ == "__main__":
    print("FAQ API Test Client")
    print("Make sure to start the API server first with: python faq_api.py")
    print("Or: uvicorn faq_api:app --reload")
    print()
    
    # Wait a moment for user to read
    input("Press Enter to start testing...")
    
    test_api()
    
    # Ask if user wants to run benchmark
    run_benchmark = input("\nRun benchmark test? (y/n): ").lower().strip()
    if run_benchmark == 'y':
        benchmark_api()
    
    print("\nTesting complete!")