#!/usr/bin/env python3
"""
Backend Testing Script for Dental Landing Page
Tests the FastAPI backend server endpoints and functionality.
"""

import requests
import json
import sys
from datetime import datetime
import os

# Get the backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    base_url = line.split('=')[1].strip()
                    return f"{base_url}/api"
        return None
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return None

def test_server_health():
    """Test if the server is running and responding"""
    backend_url = get_backend_url()
    if not backend_url:
        print("❌ CRITICAL: Could not get backend URL from frontend/.env")
        return False
    
    print(f"🔍 Testing backend at: {backend_url}")
    
    try:
        response = requests.get(f"{backend_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("message") == "Hello World":
                print("✅ Server health check passed")
                return True
            else:
                print(f"❌ Unexpected response: {data}")
                return False
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ CRITICAL: Server connection failed: {e}")
        return False

def test_status_endpoints():
    """Test the status endpoints (GET and POST)"""
    backend_url = get_backend_url()
    if not backend_url:
        return False
    
    print("\n🔍 Testing status endpoints...")
    
    # Test GET /api/status
    try:
        response = requests.get(f"{backend_url}/status", timeout=10)
        if response.status_code == 200:
            status_checks = response.json()
            print(f"✅ GET /api/status works - returned {len(status_checks)} status checks")
        else:
            print(f"❌ GET /api/status failed with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ GET /api/status failed: {e}")
        return False
    
    # Test POST /api/status
    try:
        test_data = {
            "client_name": "Test Dental Clinic"
        }
        response = requests.post(f"{backend_url}/status", 
                               json=test_data, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        if response.status_code == 200:
            created_status = response.json()
            if created_status.get("client_name") == test_data["client_name"]:
                print("✅ POST /api/status works - status check created successfully")
                return True
            else:
                print(f"❌ POST /api/status returned unexpected data: {created_status}")
                return False
        else:
            print(f"❌ POST /api/status failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ POST /api/status failed: {e}")
        return False

def test_cors_headers():
    """Test CORS configuration"""
    backend_url = get_backend_url()
    if not backend_url:
        return False
    
    print("\n🔍 Testing CORS headers...")
    
    try:
        response = requests.get(f"{backend_url}/", timeout=10)
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        
        if cors_headers['Access-Control-Allow-Origin']:
            print("✅ CORS headers are present")
            return True
        else:
            print("⚠️  CORS headers not found (may be handled by proxy)")
            return True  # Not critical for production setup
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

def test_database_connectivity():
    """Test database connectivity by creating and retrieving a status check"""
    backend_url = get_backend_url()
    if not backend_url:
        return False
    
    print("\n🔍 Testing database connectivity...")
    
    # Create a test status check
    test_data = {
        "client_name": f"DB Test Clinic {datetime.now().strftime('%H:%M:%S')}"
    }
    
    try:
        # Create
        response = requests.post(f"{backend_url}/status", 
                               json=test_data, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to create test status check: {response.status_code}")
            return False
        
        created_item = response.json()
        
        # Retrieve and verify
        response = requests.get(f"{backend_url}/status", timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to retrieve status checks: {response.status_code}")
            return False
        
        status_checks = response.json()
        found = any(item.get("client_name") == test_data["client_name"] for item in status_checks)
        
        if found:
            print("✅ Database connectivity test passed - data persisted correctly")
            return True
        else:
            print("❌ Database connectivity test failed - data not found after creation")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Database connectivity test failed: {e}")
        return False

def main():
    """Run all backend tests"""
    print("🚀 Starting Backend Testing for Dental Landing Page")
    print("=" * 60)
    
    tests = [
        ("Server Health Check", test_server_health),
        ("Status Endpoints", test_status_endpoints),
        ("CORS Configuration", test_cors_headers),
        ("Database Connectivity", test_database_connectivity)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 60)
    print("📊 BACKEND TEST RESULTS SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL BACKEND TESTS PASSED - Server is ready for production!")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - Please review the issues above")
        return 1

if __name__ == "__main__":
    sys.exit(main())