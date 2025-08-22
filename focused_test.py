#!/usr/bin/env python3
import requests
import json

def test_number_to_words_fix():
    """Test the fixed number-to-words conversion for thousands and millions"""
    base_url = "https://contractify.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    test_cases = [
        (1000, "одна тысяча рублей"),
        (30000, "тридцать тысяч рублей"),
        (1000000, "один миллион рублей")
    ]
    
    created_ids = []
    
    print("🔍 Testing Fixed Number-to-Words Conversion...")
    
    for amount, expected in test_cases:
        contract_data = {
            "name_or_organization": f"Тест {amount}",
            "other_details": "Тестовые данные",
            "service_cost": amount,
            "duration_months": 6
        }
        
        response = requests.post(f"{api_url}/contracts/direct", json=contract_data)
        
        if response.status_code == 200:
            data = response.json()
            created_ids.append(data['id'])
            actual = data.get('service_cost_words', '')
            
            if actual == expected:
                print(f"   ✅ {amount}: '{actual}' (CORRECT)")
            else:
                print(f"   ❌ {amount}: '{actual}' (expected: '{expected}')")
        else:
            print(f"   ❌ {amount}: API call failed with {response.status_code}")
    
    # Cleanup
    for contract_id in created_ids:
        requests.delete(f"{api_url}/contracts/direct/{contract_id}")
    
    return True

def test_word_download_fix():
    """Test the fixed Word download with Cyrillic filename"""
    base_url = "https://contractify.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("\n🔍 Testing Fixed Word Download...")
    
    # Create contract with Cyrillic name
    contract_data = {
        "name_or_organization": "Компания для Скачивания",
        "other_details": "Тестовые данные",
        "service_cost": 35000,
        "duration_months": 6
    }
    
    response = requests.post(f"{api_url}/contracts/direct", json=contract_data)
    
    if response.status_code == 200:
        data = response.json()
        contract_id = data['id']
        contract_number = data.get('contract_number', '')
        
        # Test download
        download_response = requests.get(f"{api_url}/contracts/direct/{contract_id}/download")
        
        if download_response.status_code == 200:
            print("   ✅ Download successful")
            
            # Check headers
            content_type = download_response.headers.get('Content-Type', '')
            if 'wordprocessingml.document' in content_type:
                print("   ✅ Correct Content-Type")
            else:
                print(f"   ❌ Wrong Content-Type: {content_type}")
            
            content_disposition = download_response.headers.get('Content-Disposition', '')
            if 'attachment' in content_disposition and 'filename=' in content_disposition:
                print("   ✅ Correct Content-Disposition")
                filename = content_disposition.split('filename=')[1]
                print(f"   📄 Filename: {filename}")
                
                # Check if filename is ASCII-safe
                try:
                    filename.encode('ascii')
                    print("   ✅ Filename is ASCII-safe")
                except UnicodeEncodeError:
                    print("   ❌ Filename contains non-ASCII characters")
            else:
                print(f"   ❌ Wrong Content-Disposition: {content_disposition}")
            
            # Check file size
            if len(download_response.content) > 1000:
                print(f"   ✅ File size reasonable: {len(download_response.content)} bytes")
            else:
                print(f"   ❌ File size too small: {len(download_response.content)} bytes")
        else:
            print(f"   ❌ Download failed with {download_response.status_code}")
            print(f"   Response: {download_response.text}")
        
        # Cleanup
        requests.delete(f"{api_url}/contracts/direct/{contract_id}")
    else:
        print(f"   ❌ Contract creation failed with {response.status_code}")
    
    return True

def test_legacy_contract_creation():
    """Test the fixed legacy contract creation endpoint"""
    base_url = "https://contractify.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("\n🔍 Testing Fixed Legacy Contract Creation...")
    
    # First create a client
    client_data = {
        "name_or_organization": "Тестовый Клиент",
        "other_details": "Тестовые данные клиента"
    }
    
    client_response = requests.post(f"{api_url}/clients", json=client_data)
    
    if client_response.status_code == 200:
        client_data = client_response.json()
        client_id = client_data['id']
        
        # Create contract
        contract_data = {
            "client_id": client_id,
            "service_cost": "25000",
            "service_cost_words": "двадцать пять тысяч",
            "contract_end_date": "15",
            "contract_end_month": "декабря"
        }
        
        contract_response = requests.post(f"{api_url}/contracts", json=contract_data)
        
        if contract_response.status_code == 200:
            print("   ✅ Legacy contract creation successful")
            contract_data = contract_response.json()
            contract_id = contract_data['id']
            
            # Cleanup
            requests.delete(f"{api_url}/contracts/{contract_id}")
        else:
            print(f"   ❌ Contract creation failed with {contract_response.status_code}")
            print(f"   Response: {contract_response.text}")
        
        # Cleanup client
        requests.delete(f"{api_url}/clients/{client_id}")
    else:
        print(f"   ❌ Client creation failed with {client_response.status_code}")
    
    return True

if __name__ == "__main__":
    print("🚀 Running Focused Tests for Bug Fixes")
    print("=" * 50)
    
    test_number_to_words_fix()
    test_word_download_fix()
    test_legacy_contract_creation()
    
    print("\n✅ Focused tests completed!")