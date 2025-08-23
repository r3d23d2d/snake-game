import requests
import sys
import json
from datetime import datetime
import tempfile
import zipfile
import os
from urllib.parse import unquote

class FilenameAndTitleTester:
    """Test filename and title fixes for contract documents as requested in review"""
    
    def __init__(self, base_url="https://contract-editor.preview.emergentagent.com"):
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

    def test_individual_contract_creation_and_filename(self):
        """Test creating contract for individual (Петров Петр Петрович) and verify filename"""
        print("\n" + "="*80)
        print("🧑 TESTING INDIVIDUAL CONTRACT - ПЕТРОВ ПЕТР ПЕТРОВИЧ")
        print("="*80)
        
        # Create contract for individual as specified in review request
        contract_data = {
            "name_or_organization": "Петров Петр Петрович",
            "other_details": "Индивидуальный предприниматель\nг. Казань, ул. Баумана, 15\nИНН: 1234567890\nТел: +7(843)123-45-67",
            "service_cost": 50000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Create Individual Contract (Петров Петр Петрович)",
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
        
        print(f"   ✅ Contract created with ID: {contract_id}")
        print(f"   ✅ Contract number: {contract_number}")
        
        # Test regular download and verify filename
        return self.test_download_and_verify_filename(
            contract_id, 
            "Петров Петр Петрович",
            "Петрова Петра Петровича",  # Expected genitive case
            contract_number,
            "Individual Regular Download"
        )

    def test_organization_contract_creation_and_filename(self):
        """Test creating contract for organization (ООО Тест Компания) and verify filename"""
        print("\n" + "="*80)
        print("🏢 TESTING ORGANIZATION CONTRACT - ООО ТЕСТ КОМПАНИЯ")
        print("="*80)
        
        # Create contract for organization as specified in review request
        contract_data = {
            "name_or_organization": "ООО Тест Компания",
            "other_details": "Директор: Иванов И.И.\nг. Москва, ул. Тверская, 1\nИНН: 9876543210\nТел: +7(495)987-65-43\nEmail: info@testcompany.ru",
            "service_cost": 75000,
            "duration_months": 12
        }
        
        success, response = self.run_test(
            "Create Organization Contract (ООО Тест Компания)",
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
        
        print(f"   ✅ Contract created with ID: {contract_id}")
        print(f"   ✅ Contract number: {contract_number}")
        
        # Test regular download and verify filename
        return self.test_download_and_verify_filename(
            contract_id, 
            "ООО Тест Компания",
            "ООО Тест Компания",  # Organizations should remain unchanged
            contract_number,
            "Organization Regular Download"
        )

    def test_download_and_verify_filename(self, contract_id, original_name, expected_genitive, contract_number, test_name):
        """Test download and verify filename format"""
        url = f"{self.api_url}/contracts/direct/{contract_id}/download"
        
        self.tests_run += 1
        print(f"\n🔍 Testing {test_name}...")
        print(f"   URL: {url}")
        
        try:
            download_response = requests.get(url)
            
            success = download_response.status_code == 200
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {download_response.status_code}")
                
                # Check Content-Disposition header for filename
                content_disposition = download_response.headers.get('Content-Disposition', '')
                print(f"   📄 Content-Disposition: {content_disposition}")
                
                if 'attachment' in content_disposition and 'filename*=UTF-8' in content_disposition:
                    print("   ✅ Correct Content-Disposition header with UTF-8 encoding")
                    
                    # Extract filename from UTF-8 encoded format
                    filename_part = content_disposition.split("filename*=UTF-8''")[1]
                    decoded_filename = unquote(filename_part)
                    print(f"   📄 Decoded filename: {decoded_filename}")
                    
                    # Expected filename format: "Договор для [имя в родительском падеже].docx"
                    expected_filename = f"Договор для {expected_genitive}.docx"
                    print(f"   📄 Expected filename: {expected_filename}")
                    
                    if decoded_filename == expected_filename:
                        print("   ✅ Filename format is CORRECT")
                        print(f"   ✅ Genitive case conversion: '{original_name}' → '{expected_genitive}'")
                    else:
                        print("   ❌ Filename format is INCORRECT")
                        print(f"   ❌ Expected: {expected_filename}")
                        print(f"   ❌ Got: {decoded_filename}")
                        return False
                        
                else:
                    print(f"   ❌ Wrong Content-Disposition format: {content_disposition}")
                    return False
                
                # Verify document title inside Word document
                return self.verify_document_title(download_response.content, contract_number, test_name)
                
            else:
                print(f"❌ Failed - Expected 200, got {download_response.status_code}")
                print(f"   Response: {download_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

    def verify_document_title(self, document_content, contract_number, test_name):
        """Verify that document title inside Word document is standard format"""
        print(f"\n🔍 Verifying Document Title for {test_name}...")
        
        try:
            # Save document to temporary file
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                temp_file.write(document_content)
                temp_file_path = temp_file.name
            
            # Extract and check document content
            with zipfile.ZipFile(temp_file_path, 'r') as docx_zip:
                # Read the main document XML
                document_xml = docx_zip.read('word/document.xml').decode('utf-8')
                
                # Expected title format: "Договор об оказании услуг № КР22.08.25"
                expected_title = f"Договор об оказании услуг № {contract_number}"
                print(f"   📄 Expected title: {expected_title}")
                
                if expected_title in document_xml:
                    print("   ✅ Document title is CORRECT (standard format)")
                    print("   ✅ Title has NOT been changed to include genitive case")
                    return True
                else:
                    print("   ❌ Document title is INCORRECT or missing")
                    print("   ❌ Standard title format not found in document")
                    
                    # Look for any title-like content for debugging
                    if 'Договор об оказании услуг' in document_xml:
                        print("   🔍 Found partial title in document")
                        # Extract surrounding text for debugging
                        start_idx = document_xml.find('Договор об оказании услуг')
                        if start_idx != -1:
                            title_section = document_xml[start_idx:start_idx+200]
                            print(f"   🔍 Title section: {title_section}")
                    else:
                        print("   ❌ No title found in document at all")
                    
                    return False
                    
        except Exception as e:
            print(f"   ❌ Error checking document title: {str(e)}")
            return False
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass

    def test_custom_download_with_edited_content(self):
        """Test custom download with edited content and verify filename includes (редактированный)"""
        print("\n" + "="*80)
        print("✏️ TESTING CUSTOM DOWNLOAD WITH EDITED CONTENT")
        print("="*80)
        
        # Create a contract for custom download testing
        contract_data = {
            "name_or_organization": "Сидоров Сидор Сидорович",
            "other_details": "Индивидуальный предприниматель\nг. Санкт-Петербург, Невский пр., 50",
            "service_cost": 40000,
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
        
        print(f"   ✅ Contract created with ID: {contract_id}")
        print(f"   ✅ Contract number: {contract_number}")
        
        # Update contract content with custom text
        custom_content = f"""**Договор об оказании услуг № {contract_number}**

РЕДАКТИРОВАННОЕ СОДЕРЖИМОЕ ДОГОВОРА

г. Казань «___» 2025 г.

Индивидуальный предприниматель Шамсутдинов Радис Раисович, именуемый в дальнейшем «Исполнитель» с одной стороны и Сидоров Сидор Сидорович, именуемый в дальнейшем «Заказчик», с другой стороны.

**1. ПРЕДМЕТ ДОГОВОРА**

1.1. Данный договор был отредактирован пользователем для тестирования функции кастомного скачивания.

1.2. Исполнитель обязуется оказать услуги по созданию рекламных кампаний.

**2. СТОИМОСТЬ УСЛУГ**

2.1. Стоимость услуг составляет 40000 (сорок тысяч) рублей.

**3. ЗАКЛЮЧИТЕЛЬНЫЕ ПОЛОЖЕНИЯ**

3.1. Настоящий договор составлен в двух экземплярах.

**ПОДПИСИ СТОРОН**

Исполнитель: ________________/Шамсутдинов Р.Р.

Заказчик: ________________/Сидоров Сидор Сидорович

КОНЕЦ РЕДАКТИРОВАННОГО СОДЕРЖИМОГО"""

        content_update_data = {
            "contract_content": custom_content
        }
        
        success, update_response = self.run_test(
            "Update Contract Content for Custom Download",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            200,
            data=content_update_data,
            return_response=True
        )
        
        if not success:
            return False
        
        print("   ✅ Contract content updated with custom text")
        
        # Test custom download
        url = f"{self.api_url}/contracts/direct/{contract_id}/download_custom"
        
        self.tests_run += 1
        print(f"\n🔍 Testing Custom Download with Edited Content...")
        print(f"   URL: {url}")
        
        try:
            download_response = requests.get(url)
            
            success = download_response.status_code == 200
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {download_response.status_code}")
                
                # Check Content-Disposition header for filename
                content_disposition = download_response.headers.get('Content-Disposition', '')
                print(f"   📄 Content-Disposition: {content_disposition}")
                
                if 'attachment' in content_disposition and 'filename*=UTF-8' in content_disposition:
                    print("   ✅ Correct Content-Disposition header with UTF-8 encoding")
                    
                    # Extract filename from UTF-8 encoded format
                    filename_part = content_disposition.split("filename*=UTF-8''")[1]
                    decoded_filename = unquote(filename_part)
                    print(f"   📄 Decoded filename: {decoded_filename}")
                    
                    # Expected filename format: "Договор для [имя в родительском падеже] (редактированный).docx"
                    expected_filename = "Договор для Сидорова Сидора Сидоровича (редактированный).docx"
                    print(f"   📄 Expected filename: {expected_filename}")
                    
                    if decoded_filename == expected_filename:
                        print("   ✅ Custom filename format is CORRECT")
                        print("   ✅ Filename includes '(редактированный)' suffix")
                        print("   ✅ Genitive case conversion: 'Сидоров Сидор Сидорович' → 'Сидорова Сидора Сидоровича'")
                    else:
                        print("   ❌ Custom filename format is INCORRECT")
                        print(f"   ❌ Expected: {expected_filename}")
                        print(f"   ❌ Got: {decoded_filename}")
                        return False
                        
                else:
                    print(f"   ❌ Wrong Content-Disposition format: {content_disposition}")
                    return False
                
                # Verify document contains custom content and standard title
                return self.verify_custom_document_content(download_response.content, contract_number, custom_content)
                
            else:
                print(f"❌ Failed - Expected 200, got {download_response.status_code}")
                print(f"   Response: {download_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

    def verify_custom_document_content(self, document_content, contract_number, expected_custom_content):
        """Verify that custom document contains edited content but standard title"""
        print(f"\n🔍 Verifying Custom Document Content...")
        
        try:
            # Save document to temporary file
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                temp_file.write(document_content)
                temp_file_path = temp_file.name
            
            # Extract and check document content
            with zipfile.ZipFile(temp_file_path, 'r') as docx_zip:
                # Read the main document XML
                document_xml = docx_zip.read('word/document.xml').decode('utf-8')
                
                # Check that title is still standard format
                expected_title = f"Договор об оказании услуг № {contract_number}"
                if expected_title in document_xml:
                    print("   ✅ Document title remains STANDARD format (not changed)")
                else:
                    print("   ❌ Document title is not in standard format")
                    return False
                
                # Check for custom content markers
                custom_checks = [
                    ('Custom header', 'РЕДАКТИРОВАННОЕ СОДЕРЖИМОЕ ДОГОВОРА' in document_xml),
                    ('Custom clause', 'отредактирован пользователем для тестирования' in document_xml),
                    ('Custom ending', 'КОНЕЦ РЕДАКТИРОВАННОГО СОДЕРЖИМОГО' in document_xml),
                    ('Client name', 'Сидоров Сидор Сидорович' in document_xml),
                    ('Contract number', contract_number in document_xml)
                ]
                
                all_custom_content_found = True
                for check_name, check_result in custom_checks:
                    if check_result:
                        print(f"   ✅ {check_name} found in custom document")
                    else:
                        print(f"   ❌ {check_name} NOT found in custom document")
                        all_custom_content_found = False
                
                # Check for header with Kazan and date
                if 'Казань' in document_xml:
                    print("   ✅ 'Казань' found in custom document header")
                else:
                    print("   ❌ 'Казань' NOT found in custom document header")
                    all_custom_content_found = False
                
                return all_custom_content_found
                    
        except Exception as e:
            print(f"   ❌ Error checking custom document content: {str(e)}")
            return False
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass

    def test_cyrillic_characters_in_filenames(self):
        """Test that Cyrillic characters are correctly displayed in filenames"""
        print("\n" + "="*80)
        print("🔤 TESTING CYRILLIC CHARACTERS IN FILENAMES")
        print("="*80)
        
        # Test with various Cyrillic names
        test_cases = [
            {
                "name": "Александров Александр Александрович",
                "expected_genitive": "Александрова Александра Александровича"
            },
            {
                "name": "Смирнова Мария Ивановна", 
                "expected_genitive": "Смирновы Марии Ивановны"
            },
            {
                "name": "ООО Русская Компания",
                "expected_genitive": "ООО Русская Компания"  # Organizations unchanged
            },
            {
                "name": "ИП Козлов Олег Петрович",
                "expected_genitive": "ИП Козлов Олег Петрович"  # Organizations unchanged
            }
        ]
        
        all_passed = True
        
        for i, test_case in enumerate(test_cases):
            print(f"\n--- Test Case {i+1}: {test_case['name']} ---")
            
            # Create contract
            contract_data = {
                "name_or_organization": test_case['name'],
                "other_details": f"Тестовые данные для {test_case['name']}",
                "service_cost": 30000 + (i * 5000),
                "duration_months": 6
            }
            
            success, response = self.run_test(
                f"Create Contract for Cyrillic Test {i+1}",
                "POST",
                "contracts/direct",
                200,
                data=contract_data,
                return_response=True
            )
            
            if not success or 'id' not in response:
                all_passed = False
                continue
                
            contract_id = response['id']
            self.created_contract_ids.append(contract_id)
            
            # Test download and filename
            url = f"{self.api_url}/contracts/direct/{contract_id}/download"
            
            try:
                download_response = requests.get(url)
                
                if download_response.status_code == 200:
                    content_disposition = download_response.headers.get('Content-Disposition', '')
                    
                    if 'filename*=UTF-8' in content_disposition:
                        filename_part = content_disposition.split("filename*=UTF-8''")[1]
                        decoded_filename = unquote(filename_part)
                        expected_filename = f"Договор для {test_case['expected_genitive']}.docx"
                        
                        print(f"   📄 Filename: {decoded_filename}")
                        print(f"   📄 Expected: {expected_filename}")
                        
                        if decoded_filename == expected_filename:
                            print(f"   ✅ Cyrillic filename correct for: {test_case['name']}")
                        else:
                            print(f"   ❌ Cyrillic filename incorrect for: {test_case['name']}")
                            all_passed = False
                    else:
                        print(f"   ❌ UTF-8 encoding not found in Content-Disposition")
                        all_passed = False
                else:
                    print(f"   ❌ Download failed with status: {download_response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                print(f"   ❌ Error testing Cyrillic filename: {str(e)}")
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
        """Run all filename and title tests as requested in review"""
        print("🚀 Starting Filename and Title Testing (Review Request)")
        print("="*80)
        print("Testing contract filename and title fixes:")
        print("1. Individual contracts (Петров Петр Петрович)")
        print("2. Organization contracts (ООО Тест Компания)")
        print("3. Document titles remain standard format")
        print("4. Filenames use correct genitive case")
        print("5. Custom downloads with (редактированный) suffix")
        print("6. Cyrillic character handling")
        print("="*80)
        
        try:
            # Test 1: Individual contract
            test1_passed = self.test_individual_contract_creation_and_filename()
            
            # Test 2: Organization contract
            test2_passed = self.test_organization_contract_creation_and_filename()
            
            # Test 3: Custom download with edited content
            test3_passed = self.test_custom_download_with_edited_content()
            
            # Test 4: Cyrillic characters in filenames
            test4_passed = self.test_cyrillic_characters_in_filenames()
            
            # Summary
            print("\n" + "="*80)
            print("📊 FILENAME AND TITLE TEST RESULTS")
            print("="*80)
            print(f"Total tests run: {self.tests_run}")
            print(f"Tests passed: {self.tests_passed}")
            print(f"Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
            print()
            print("Individual Test Results:")
            print(f"✅ Individual Contract (Петров): {'PASSED' if test1_passed else 'FAILED'}")
            print(f"✅ Organization Contract (ООО): {'PASSED' if test2_passed else 'FAILED'}")
            print(f"✅ Custom Download (редактированный): {'PASSED' if test3_passed else 'FAILED'}")
            print(f"✅ Cyrillic Characters: {'PASSED' if test4_passed else 'FAILED'}")
            print()
            
            all_tests_passed = test1_passed and test2_passed and test3_passed and test4_passed
            
            if all_tests_passed:
                print("🎉 ALL FILENAME AND TITLE TESTS PASSED!")
                print("✅ Document titles remain standard format")
                print("✅ Filenames use correct genitive case")
                print("✅ Cyrillic characters display correctly")
                print("✅ Custom downloads include (редактированный) suffix")
            else:
                print("❌ SOME TESTS FAILED - Review implementation needed")
            
            return all_tests_passed
            
        finally:
            # Always cleanup
            self.cleanup_contracts()

def main():
    """Main function to run filename and title tests"""
    tester = FilenameAndTitleTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎯 REVIEW REQUEST COMPLETED SUCCESSFULLY")
        print("All filename and title fixes are working correctly!")
        sys.exit(0)
    else:
        print("\n❌ REVIEW REQUEST FAILED")
        print("Some filename and title fixes need attention!")
        sys.exit(1)

if __name__ == "__main__":
    main()