import requests
import sys
import json
from datetime import datetime

class ContractSystemTester:
    def __init__(self, base_url="https://client-data-hub-4.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.created_client_id = None
        self.created_contract_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, return_response=False):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                if return_response:
                    try:
                        return success, response.json()
                    except:
                        return success, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text}")

            return success, response.json() if success and response.text else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_api_root(self):
        """Test API root endpoint"""
        return self.run_test("API Root", "GET", "", 200)

    def test_create_client(self):
        """Test creating a client with simplified structure (2 fields)"""
        client_data = {
            "name_or_organization": "ООО Новая Компания",
            "other_details": "Директор: Сидоров С.С.\nМосква, ул. Тверская, 15\nИНН 1122334455\nТел: +7(495)123-45-67\nEmail: info@newcompany.ru"
        }
        
        success, response = self.run_test(
            "Create Client (Simplified Structure)",
            "POST",
            "clients",
            200,
            data=client_data,
            return_response=True
        )
        
        if success and 'id' in response:
            self.created_client_id = response['id']
            print(f"   Created client ID: {self.created_client_id}")
            return True
        return False

    def test_get_clients(self):
        """Test getting all clients"""
        success, response = self.run_test(
            "Get All Clients",
            "GET",
            "clients",
            200,
            return_response=True
        )
        
        if success:
            print(f"   Found {len(response)} clients")
            return True
        return False

    def test_get_client_by_id(self):
        """Test getting a specific client by ID"""
        if not self.created_client_id:
            print("❌ No client ID available for testing")
            return False
            
        success, response = self.run_test(
            "Get Client by ID",
            "GET",
            f"clients/{self.created_client_id}",
            200,
            return_response=True
        )
        
        if success:
            print(f"   Client name/organization: {response.get('name_or_organization', 'N/A')}")
            print(f"   Other details: {response.get('other_details', 'N/A')}")
            return True
        return False

    def test_create_contract(self):
        """Test creating a contract"""
        if not self.created_client_id:
            print("❌ No client ID available for contract creation")
            return False
            
        contract_data = {
            "client_id": self.created_client_id,
            "service_cost": "30000",
            "service_cost_words": "тридцать тысяч",
            "contract_end_date": "31",
            "contract_end_month": "декабря"
        }
        
        success, response = self.run_test(
            "Create Contract",
            "POST",
            "contracts",
            200,
            data=contract_data,
            return_response=True
        )
        
        if success and 'id' in response:
            self.created_contract_id = response['id']
            print(f"   Created contract ID: {self.created_contract_id}")
            print(f"   Client name in contract: {response.get('client_name', 'N/A')}")
            
            # Check if contract content contains client data
            contract_content = response.get('contract_content', '')
            if 'ООО Новая Компания' in contract_content:
                print("   ✅ Client name found in contract content")
            else:
                print("   ❌ Client name NOT found in contract content")
                
            if 'Директор: Сидоров С.С.' in contract_content:
                print("   ✅ Client details found in contract content")
            else:
                print("   ❌ Client details NOT found in contract content")
                
            if '30000' in contract_content and 'тридцать тысяч' in contract_content:
                print("   ✅ Service cost found in contract content")
            else:
                print("   ❌ Service cost NOT found in contract content")
                
            return True
        return False

    def test_get_contracts(self):
        """Test getting all contracts"""
        success, response = self.run_test(
            "Get All Contracts",
            "GET",
            "contracts",
            200,
            return_response=True
        )
        
        if success:
            print(f"   Found {len(response)} contracts")
            return True
        return False

    def test_get_contract_by_id(self):
        """Test getting a specific contract by ID"""
        if not self.created_contract_id:
            print("❌ No contract ID available for testing")
            return False
            
        success, response = self.run_test(
            "Get Contract by ID",
            "GET",
            f"contracts/{self.created_contract_id}",
            200,
            return_response=True
        )
        
        if success:
            print(f"   Contract client: {response.get('client_name', 'N/A')}")
            print(f"   Service cost: {response.get('service_cost', 'N/A')}")
            return True
        return False

    def test_download_contract_word(self):
        """Test downloading contract in Word format - NEW FUNCTIONALITY"""
        if not self.created_contract_id:
            print("❌ No contract ID available for download testing")
            return False
            
        url = f"{self.api_url}/contracts/{self.created_contract_id}/download"
        
        self.tests_run += 1
        print(f"\n🔍 Testing Download Contract Word...")
        print(f"   URL: {url}")
        
        try:
            response = requests.get(url)
            
            success = response.status_code == 200
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                
                # Check Content-Type header
                content_type = response.headers.get('Content-Type', '')
                expected_content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                if expected_content_type in content_type:
                    print("   ✅ Correct Content-Type for Word document")
                else:
                    print(f"   ❌ Wrong Content-Type: {content_type}")
                
                # Check Content-Disposition header for filename
                content_disposition = response.headers.get('Content-Disposition', '')
                if 'attachment' in content_disposition and 'filename=' in content_disposition:
                    print("   ✅ Correct Content-Disposition header with filename")
                    # Extract filename
                    filename_part = content_disposition.split('filename=')[1]
                    print(f"   📄 Filename: {filename_part}")
                    
                    # Check if filename contains client name and .docx extension
                    if 'OOO_Novaya_Kompaniya' in filename_part and '.docx' in filename_part:
                        print("   ✅ Filename contains transliterated client name and .docx extension")
                    else:
                        print("   ❌ Filename format incorrect")
                else:
                    print(f"   ❌ Wrong Content-Disposition: {content_disposition}")
                
                # Check file size (Word documents should have reasonable size)
                content_length = len(response.content)
                if content_length > 1000:  # At least 1KB for a Word document
                    print(f"   ✅ File size reasonable: {content_length} bytes")
                else:
                    print(f"   ❌ File size too small: {content_length} bytes")
                
                # Check if it's actually a Word document by checking magic bytes
                if response.content.startswith(b'PK'):  # ZIP-based format (Word .docx)
                    print("   ✅ File appears to be a valid Word document (ZIP-based)")
                else:
                    print("   ❌ File does not appear to be a valid Word document")
                
                return True
            else:
                print(f"❌ Failed - Expected 200, got {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

    def test_delete_contract(self):
        """Test deleting a contract"""
        if not self.created_contract_id:
            print("❌ No contract ID available for deletion")
            return False
            
        success, response = self.run_test(
            "Delete Contract",
            "DELETE",
            f"contracts/{self.created_contract_id}",
            200
        )
        
        if success:
            self.created_contract_id = None
            return True
        return False

    def test_delete_client(self):
        """Test deleting a client"""
        if not self.created_client_id:
            print("❌ No client ID available for deletion")
            return False
            
        success, response = self.run_test(
            "Delete Client",
            "DELETE",
            f"clients/{self.created_client_id}",
            200
        )
        
        if success:
            self.created_client_id = None
            return True
        return False

    def test_create_petrov_client_and_contract(self):
        """Test creating the specific client and contract from the review request with simplified structure"""
        # Create Kozlov client as specified in the review request (simplified structure)
        kozlov_data = {
            "name_or_organization": "Козлов Олег Петрович",
            "other_details": "ИП\nСПб, пр. Невский, 100\nТел: +7(812)987-65-43"
        }
        
        success, response = self.run_test(
            "Create Kozlov Client (Review Request - Simplified)",
            "POST",
            "clients",
            200,
            data=kozlov_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            return False
            
        kozlov_client_id = response['id']
        print(f"   Created Kozlov client ID: {kozlov_client_id}")
        
        # Create contract for Kozlov as specified
        kozlov_contract_data = {
            "client_id": kozlov_client_id,
            "service_cost": "75000",
            "service_cost_words": "семьдесят пять тысяч",
            "contract_end_date": "15",
            "contract_end_month": "сентября"
        }
        
        success, response = self.run_test(
            "Create Kozlov Contract (Review Request)",
            "POST",
            "contracts",
            200,
            data=kozlov_contract_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            # Clean up client
            requests.delete(f"{self.api_url}/clients/{kozlov_client_id}")
            return False
            
        kozlov_contract_id = response['id']
        print(f"   Created Kozlov contract ID: {kozlov_contract_id}")
        
        # Test download for Kozlov contract
        url = f"{self.api_url}/contracts/{kozlov_contract_id}/download"
        
        self.tests_run += 1
        print(f"\n🔍 Testing Download Kozlov Contract Word...")
        print(f"   URL: {url}")
        
        try:
            download_response = requests.get(url)
            
            success = download_response.status_code == 200
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {download_response.status_code}")
                
                # Check filename contains Kozlov
                content_disposition = download_response.headers.get('Content-Disposition', '')
                if 'Kozlov' in content_disposition:
                    print("   ✅ Filename contains Kozlov client name")
                else:
                    print(f"   ❌ Filename doesn't contain Kozlov: {content_disposition}")
                
                # Verify contract content has all Kozlov data
                contract_content = response.get('contract_content', '')
                checks = [
                    ('Client name', 'Козлов Олег Петрович' in contract_content),
                    ('Other details', 'ИП' in contract_content),
                    ('Address', 'СПб, пр. Невский, 100' in contract_content),
                    ('Phone', '+7(812)987-65-43' in contract_content),
                    ('Cost', '75000' in contract_content),
                    ('Cost words', 'семьдесят пять тысяч' in contract_content),
                    ('End date', '15' in contract_content and 'сентября' in contract_content)
                ]
                
                for check_name, check_result in checks:
                    if check_result:
                        print(f"   ✅ {check_name} found in contract")
                    else:
                        print(f"   ❌ {check_name} NOT found in contract")
                
            else:
                print(f"❌ Download failed - Expected 200, got {download_response.status_code}")
                
        except Exception as e:
            print(f"❌ Download failed - Error: {str(e)}")
            success = False
        
        # Clean up
        requests.delete(f"{self.api_url}/contracts/{kozlov_contract_id}")
        requests.delete(f"{self.api_url}/clients/{kozlov_client_id}")
        
        return success

    def test_create_minimal_client(self):
        """Test creating a client with minimal data (only name_or_organization)"""
        client_data = {
            "name_or_organization": "Тестовый Клиент Минимальный"
        }
        
        success, response = self.run_test(
            "Create Minimal Client (Simplified Structure)",
            "POST",
            "clients",
            200,
            data=client_data,
            return_response=True
        )
        
        if success and 'id' in response:
            # Clean up immediately
            requests.delete(f"{self.api_url}/clients/{response['id']}")
            return True
        return False

def main():
    print("🚀 Starting Contract Management System Backend Tests")
    print("=" * 60)
    
    tester = ContractSystemTester()
    
    # Test sequence
    test_sequence = [
        ("API Root", tester.test_api_root),
        ("Create Client", tester.test_create_client),
        ("Get All Clients", tester.test_get_clients),
        ("Get Client by ID", tester.test_get_client_by_id),
        ("Create Contract", tester.test_create_contract),
        ("Get All Contracts", tester.test_get_contracts),
        ("Get Contract by ID", tester.test_get_contract_by_id),
        ("Download Contract Word", tester.test_download_contract_word),  # NEW TEST
        ("Petrov Client & Contract Test", tester.test_create_petrov_client_and_contract),  # REVIEW REQUEST TEST
        ("Create Minimal Client", tester.test_create_minimal_client),
        ("Delete Contract", tester.test_delete_contract),
        ("Delete Client", tester.test_delete_client),
    ]
    
    # Run all tests
    for test_name, test_func in test_sequence:
        try:
            test_func()
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Backend Test Results:")
    print(f"   Tests run: {tester.tests_run}")
    print(f"   Tests passed: {tester.tests_passed}")
    print(f"   Success rate: {(tester.tests_passed/tester.tests_run*100):.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All backend tests passed!")
        return 0
    else:
        print("⚠️  Some backend tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())