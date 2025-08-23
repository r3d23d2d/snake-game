import requests
import sys
import json
import tempfile
import zipfile
from datetime import datetime

class GenitiveCaseTester:
    """Test the genitive case functionality for contract titles"""
    
    def __init__(self, base_url="https://wordsmith-app-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.created_contract_ids = []

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
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
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

    def test_genitive_case_individuals(self):
        """Test genitive case conversion for individual names"""
        test_cases = [
            {
                "name": "Иванов Иван Иванович",
                "expected_genitive": "Иванова Ивана Ивановича",
                "description": "Standard Russian male name"
            },
            {
                "name": "Петрова Анна Сергеевна", 
                "expected_genitive": "Петровы Анны Сергеевны",
                "description": "Standard Russian female name"
            },
            {
                "name": "Сидоров Петр Александрович",
                "expected_genitive": "Сидорова Петра Александровича", 
                "description": "Another male name variant"
            },
            {
                "name": "Козлова Мария Владимировна",
                "expected_genitive": "Козловы Марии Владимировны",
                "description": "Female name with -ова ending"
            }
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            print(f"\n📝 Testing genitive case for: {test_case['name']} ({test_case['description']})")
            
            contract_data = {
                "name_or_organization": test_case["name"],
                "other_details": "Тестовые данные для проверки родительского падежа",
                "service_cost": 50000,
                "duration_months": 6
            }
            
            success, response = self.run_test(
                f"Create Contract for {test_case['name']}",
                "POST",
                "contracts/direct",
                200,
                data=contract_data,
                return_response=True
            )
            
            if success and 'id' in response:
                contract_id = response['id']
                self.created_contract_ids.append(contract_id)
                
                # Test Word document download to check title
                success = self.check_genitive_in_word_document(
                    contract_id, 
                    test_case["name"], 
                    test_case["expected_genitive"],
                    response.get('contract_number', '')
                )
                
                if not success:
                    all_passed = False
            else:
                all_passed = False
                
        return all_passed

    def test_genitive_case_organizations(self):
        """Test genitive case conversion for organizations"""
        test_cases = [
            {
                "name": "ООО Тест",
                "expected_genitive": "ООО Тест",  # Organizations don't change
                "description": "Limited Liability Company"
            },
            {
                "name": "ИП Иванов Иван Иванович",
                "expected_genitive": "ИП Иванов Иван Иванович",  # Organizations don't change
                "description": "Individual Entrepreneur"
            },
            {
                "name": "АО Рога и Копыта",
                "expected_genitive": "АО Рога и Копыта",  # Organizations don't change
                "description": "Joint Stock Company"
            },
            {
                "name": "ЗАО Тестовая Компания",
                "expected_genitive": "ЗАО Тестовая Компания",  # Organizations don't change
                "description": "Closed Joint Stock Company"
            }
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            print(f"\n🏢 Testing genitive case for organization: {test_case['name']} ({test_case['description']})")
            
            contract_data = {
                "name_or_organization": test_case["name"],
                "other_details": "Тестовые данные для проверки организаций",
                "service_cost": 75000,
                "duration_months": 12
            }
            
            success, response = self.run_test(
                f"Create Contract for {test_case['name']}",
                "POST",
                "contracts/direct",
                200,
                data=contract_data,
                return_response=True
            )
            
            if success and 'id' in response:
                contract_id = response['id']
                self.created_contract_ids.append(contract_id)
                
                # Test Word document download to check title
                success = self.check_genitive_in_word_document(
                    contract_id, 
                    test_case["name"], 
                    test_case["expected_genitive"],
                    response.get('contract_number', '')
                )
                
                if not success:
                    all_passed = False
            else:
                all_passed = False
                
        return all_passed

    def check_genitive_in_word_document(self, contract_id, original_name, expected_genitive, contract_number):
        """Check if the Word document contains the correct genitive case in title"""
        url = f"{self.api_url}/contracts/direct/{contract_id}/download"
        
        try:
            download_response = requests.get(url)
            
            if download_response.status_code != 200:
                print(f"   ❌ Failed to download Word document: {download_response.status_code}")
                return False
            
            # Save document temporarily and check content
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                temp_file.write(download_response.content)
                temp_file_path = temp_file.name
            
            try:
                # Extract and check document content
                with zipfile.ZipFile(temp_file_path, 'r') as docx_zip:
                    # Read the main document XML
                    document_xml = docx_zip.read('word/document.xml').decode('utf-8')
                    
                    # Check for the expected title format
                    expected_title = f"Договор об оказании услуг для {expected_genitive} № {contract_number}"
                    
                    if expected_title in document_xml:
                        print(f"   ✅ Correct genitive case title found: '{expected_title}'")
                        return True
                    else:
                        print(f"   ❌ Expected title not found: '{expected_title}'")
                        
                        # Try to find what title is actually there
                        import re
                        title_pattern = r'Договор об оказании услуг для ([^№]+) № ([^<]+)'
                        matches = re.findall(title_pattern, document_xml)
                        if matches:
                            actual_genitive = matches[0][0].strip()
                            actual_number = matches[0][1].strip()
                            print(f"   📄 Actual title found: 'Договор об оказании услуг для {actual_genitive} № {actual_number}'")
                            print(f"   📝 Original name: '{original_name}'")
                            print(f"   📝 Expected genitive: '{expected_genitive}'")
                            print(f"   📝 Actual genitive: '{actual_genitive}'")
                        else:
                            print(f"   ❌ No contract title found in document")
                        
                        return False
                        
            except Exception as e:
                print(f"   ❌ Error checking document content: {str(e)}")
                return False
            finally:
                # Clean up temporary file
                import os
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                    
        except Exception as e:
            print(f"   ❌ Error downloading document: {str(e)}")
            return False

    def test_custom_download_genitive_case(self):
        """Test genitive case in custom download functionality"""
        print(f"\n📋 Testing genitive case in custom download...")
        
        # Create a contract with individual name
        contract_data = {
            "name_or_organization": "Смирнов Алексей Викторович",
            "other_details": "Тестовые данные для кастомного скачивания",
            "service_cost": 60000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Create Contract for Custom Download Test",
            "POST",
            "contracts/direct",
            200,
            data=contract_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            return False
            
        contract_id = response['id']
        contract_number = response.get('contract_number', '')
        self.created_contract_ids.append(contract_id)
        
        # Update contract content with custom text
        custom_content = """**Договор об оказании услуг № {contract_number}**

КАСТОМНОЕ СОДЕРЖИМОЕ ДЛЯ ТЕСТИРОВАНИЯ РОДИТЕЛЬСКОГО ПАДЕЖА

г. Казань «___» 2025 г.

Индивидуальный предприниматель Шамсутдинов Радис Раисович, именуемый в дальнейшем «Исполнитель» с одной стороны и Смирнов Алексей Викторович, именуемый в дальнейшем «Заказчик», с другой стороны.

**1. ПРЕДМЕТ ДОГОВОРА**

1.1. Этот договор содержит кастомное содержимое для тестирования родительского падежа в заголовке.

**2. ПОДПИСИ СТОРОН**

Исполнитель: ________________/Шамсутдинов Р.Р.

Заказчик: ________________/Смирнов Алексей Викторович"""

        content_update_data = {
            "contract_content": custom_content
        }
        
        # Update content first
        success, update_response = self.run_test(
            "Update Content for Custom Download",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            200,
            data=content_update_data,
            return_response=True
        )
        
        if not success:
            return False
        
        # Test custom download
        url = f"{self.api_url}/contracts/direct/{contract_id}/download_custom"
        
        try:
            download_response = requests.get(url)
            
            if download_response.status_code != 200:
                print(f"   ❌ Failed to download custom Word document: {download_response.status_code}")
                return False
            
            # Save document temporarily and check content
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                temp_file.write(download_response.content)
                temp_file_path = temp_file.name
            
            try:
                # Extract and check document content
                with zipfile.ZipFile(temp_file_path, 'r') as docx_zip:
                    # Read the main document XML
                    document_xml = docx_zip.read('word/document.xml').decode('utf-8')
                    
                    # Check for the expected title format with genitive case
                    expected_genitive = "Смирнова Алексея Викторовича"
                    expected_title = f"Договор об оказании услуг для {expected_genitive} № {contract_number}"
                    
                    if expected_title in document_xml:
                        print(f"   ✅ Correct genitive case title found in custom document: '{expected_title}'")
                        
                        # Also check for custom content
                        if 'КАСТОМНОЕ СОДЕРЖИМОЕ ДЛЯ ТЕСТИРОВАНИЯ РОДИТЕЛЬСКОГО ПАДЕЖА' in document_xml:
                            print(f"   ✅ Custom content found in document")
                            return True
                        else:
                            print(f"   ❌ Custom content not found in document")
                            return False
                    else:
                        print(f"   ❌ Expected genitive case title not found in custom document: '{expected_title}'")
                        return False
                        
            except Exception as e:
                print(f"   ❌ Error checking custom document content: {str(e)}")
                return False
            finally:
                # Clean up temporary file
                import os
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                    
        except Exception as e:
            print(f"   ❌ Error downloading custom document: {str(e)}")
            return False

    def test_genitive_case_edge_cases(self):
        """Test genitive case conversion for edge cases"""
        test_cases = [
            {
                "name": "Иван",  # Single name
                "expected_genitive": "Ивана",
                "description": "Single first name"
            },
            {
                "name": "Петров",  # Single surname
                "expected_genitive": "Петрова",
                "description": "Single surname"
            },
            {
                "name": "Анна Петровна",  # First name + patronymic
                "expected_genitive": "Анны Петровны",
                "description": "First name and patronymic only"
            },
            {
                "name": "ООО \"Кавычки в названии\"",
                "expected_genitive": "ООО \"Кавычки в названии\"",  # Organizations don't change
                "description": "Organization with quotes"
            }
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            print(f"\n🔍 Testing edge case: {test_case['name']} ({test_case['description']})")
            
            contract_data = {
                "name_or_organization": test_case["name"],
                "other_details": "Тестовые данные для крайних случаев",
                "service_cost": 30000,
                "duration_months": 6
            }
            
            success, response = self.run_test(
                f"Create Contract for Edge Case: {test_case['name']}",
                "POST",
                "contracts/direct",
                200,
                data=contract_data,
                return_response=True
            )
            
            if success and 'id' in response:
                contract_id = response['id']
                self.created_contract_ids.append(contract_id)
                
                # Test Word document download to check title
                success = self.check_genitive_in_word_document(
                    contract_id, 
                    test_case["name"], 
                    test_case["expected_genitive"],
                    response.get('contract_number', '')
                )
                
                if not success:
                    all_passed = False
            else:
                all_passed = False
                
        return all_passed

    def cleanup_contracts(self):
        """Clean up all created contracts"""
        print(f"\n🧹 Cleaning up {len(self.created_contract_ids)} created contracts...")
        for contract_id in self.created_contract_ids:
            try:
                requests.delete(f"{self.api_url}/contracts/direct/{contract_id}")
            except:
                pass
        self.created_contract_ids = []

    def run_all_tests(self):
        """Run all genitive case tests"""
        print("🚀 Starting Genitive Case Testing for Contract Titles")
        print("=" * 60)
        
        tests = [
            ("Individual Names Genitive Case", self.test_genitive_case_individuals),
            ("Organization Names Genitive Case", self.test_genitive_case_organizations),
            ("Custom Download Genitive Case", self.test_custom_download_genitive_case),
            ("Edge Cases Genitive Case", self.test_genitive_case_edge_cases),
        ]
        
        for test_name, test_method in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                result = test_method()
                if result:
                    print(f"✅ {test_name}: PASSED")
                else:
                    print(f"❌ {test_name}: FAILED")
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {str(e)}")
        
        # Cleanup
        self.cleanup_contracts()
        
        # Final results
        print(f"\n{'='*60}")
        print(f"🏁 GENITIVE CASE TESTING COMPLETE")
        print(f"📊 Tests run: {self.tests_run}")
        print(f"✅ Tests passed: {self.tests_passed}")
        print(f"❌ Tests failed: {self.tests_run - self.tests_passed}")
        print(f"📈 Success rate: {(self.tests_passed/self.tests_run*100):.1f}%" if self.tests_run > 0 else "No tests run")
        
        return self.tests_passed == self.tests_run

if __name__ == "__main__":
    tester = GenitiveCaseTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)