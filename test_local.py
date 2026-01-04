#!/usr/bin/env python3
"""
Quick local test script for Fraud Detection API
Tests health, metrics, and prediction endpoints
"""

import requests
import json
import time

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing /health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Health check passed: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        print(f"   Make sure the API is running: uvicorn api.main:app --reload")
        return False

def test_metrics():
    """Test metrics endpoint"""
    print("\n🔍 Testing /metrics endpoint...")
    try:
        response = requests.get(f"{API_URL}/metrics", timeout=5)
        if response.status_code == 200:
            print("✅ Metrics endpoint accessible")
            # Check for Prometheus metrics
            if "predictions_total" in response.text:
                print("✅ Prometheus metrics found")
            return True
        else:
            print(f"❌ Metrics check failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Metrics check failed: {e}")
        return False

def test_docs():
    """Test API docs"""
    print("\n🔍 Testing API docs...")
    try:
        response = requests.get(f"{API_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API docs accessible at http://localhost:8000/docs")
            return True
        else:
            print(f"❌ Docs check failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Docs check failed: {e}")
        return False

def test_prediction():
    """Test prediction endpoint with sample data"""
    print("\n🔍 Testing /predict endpoint...")
    
    # Minimal sample data (adjust based on your model)
    sample_data = {
        "data": {
            "TransactionAmt": 100.0,
            "ProductCD": "W",
            "card1": 12345,
            "card2": 123.0,
            "card3": 150.0,
            "card4": "visa",
            "card5": 226.0,
            "card6": "credit",
            "addr1": 315.0,
            "addr2": 87.0,
            "dist1": 19.0,
            "P_emaildomain": 0.0,
            "R_emaildomain": 0.0,
            "C1": 1.0,
            "C2": 1.0,
            "C3": 0.0,
            "C4": 0.0,
            "C5": 0.0,
            "C6": 1.0,
            "C7": 0.0,
            "C8": 0.0,
            "C9": 1.0,
            "C10": 0.0,
            "C11": 2.0,
            "C12": 0.0,
            "C13": 1.0,
            "C14": 1.0,
            "D1": 14.0,
            "D2": 0.0,
            "D3": 13.0,
            "D4": 0.0,
            "D5": 0.0,
            "D6": 0.0,
            "D8": 0.0,
            "D9": 0.0,
            "D10": 13.0,
            "D11": 13.0,
            "D12": 0.0,
            "D13": 0.0,
            "D14": 0.0,
            "D15": 0.0,
            "M1": "T",
            "M2": "T",
            "M3": "T",
            "M4": "M2",
            "M5": "F",
            "M6": "T",
            "M7": 0.0,
            "M8": 0.0,
            "M9": 0.0,
        }
    }
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=sample_data,
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction successful!")
            print(f"   Fraud probability: {result.get('fraud_probability', 'N/A')}")
            return True
        else:
            print(f"❌ Prediction failed: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 Fraud Detection API - Local Test")
    print("=" * 60)
    print(f"Testing API at: {API_URL}")
    print("\nMake sure the API is running:")
    print("  uvicorn api.main:app --reload")
    print("=" * 60)
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Metrics Endpoint", test_metrics()))
    results.append(("API Docs", test_docs()))
    results.append(("Prediction", test_prediction()))
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    print("=" * 60)
    if all_passed:
        print("🎉 All tests passed! Ready to push to GitHub.")
    else:
        print("⚠️  Some tests failed. Fix issues before pushing.")
    print("=" * 60)

if __name__ == "__main__":
    main()

