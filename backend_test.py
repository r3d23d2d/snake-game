import requests
import sys
import json
from datetime import datetime

class DirectContractTester:
    """Test the new direct contract creation functionality"""
    
    def __init__(self, base_url="https://contract-forge.preview.emergentagent.com"):
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

    def test_number_to_words_conversion(self):
        """Test number-to-words conversion by creating contracts with various amounts"""
        test_amounts = [0, 1, 2, 5, 11, 23, 100, 1000, 1234, 30000, 1000000]
        expected_words = {
            0: "ноль рублей",
            1: "один рубль", 
            2: "два рубля",
            5: "пять рублей",
            11: "одиннадцать рублей",
            23: "двадцать три рубля",
            100: "сто рублей",
            1000: "одна тысяча рублей",
            1234: "одна тысяча двести тридцать четыре рубля",
            30000: "тридцать тысяч рублей",
            1000000: "один миллион рублей"
        }
        
        all_passed = True
        
        for amount in test_amounts:
            contract_data = {
                "name_or_organization": f"Тест Компания {amount}",
                "other_details": "Тестовые данные",
                "service_cost": amount,
                "duration_months": 6
            }
            
            success, response = self.run_test(
                f"Number to Words Test - {amount}",
                "POST",
                "contracts/direct",
                200,
                data=contract_data,
                return_response=True
            )
            
            if success and 'id' in response:
                self.created_contract_ids.append(response['id'])
                actual_words = response.get('service_cost_words', '')
                expected = expected_words.get(amount, '')
                
                if actual_words == expected:
                    print(f"   ✅ Correct conversion: {amount} → '{actual_words}'")
                else:
                    print(f"   ❌ Wrong conversion: {amount} → '{actual_words}' (expected: '{expected}')")
                    all_passed = False
            else:
                all_passed = False
                
        return all_passed

    def test_contract_number_generation(self):
        """Test contract number generation format КР + DD.MM.YY"""
        contract_data = {
            "name_or_organization": "Тест Номер Договора",
            "other_details": "Тестовые данные",
            "service_cost": 50000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Contract Number Generation",
            "POST",
            "contracts/direct",
            200,
            data=contract_data,
            return_response=True
        )
        
        if success and 'id' in response:
            self.created_contract_ids.append(response['id'])
            contract_number = response.get('contract_number', '')
            
            # Check format КР + DD.MM.YY
            import re
            pattern = r'^КР\d{2}\.\d{2}\.\d{2}$'
            if re.match(pattern, contract_number):
                print(f"   ✅ Correct format: {contract_number}")
                
                # Check if it's today's date
                from datetime import datetime
                today = datetime.now()
                expected_suffix = today.strftime('%d.%m.%y')
                if contract_number.endswith(expected_suffix):
                    print(f"   ✅ Correct date: {expected_suffix}")
                    return True
                else:
                    print(f"   ❌ Wrong date: expected {expected_suffix}")
            else:
                print(f"   ❌ Wrong format: {contract_number}")
                
        return False

    def test_contract_end_date_calculation(self):
        """Test contract end date calculation with 1, 6, and 12 months"""
        durations = [1, 6, 12]
        expected_months = {
            1: ["января", "февраля", "марта", "апреля", "мая", "июня", 
                "июля", "августа", "сентября", "октября", "ноября", "декабря"],
            6: ["января", "февраля", "марта", "апреля", "мая", "июня", 
                "июля", "августа", "сентября", "октября", "ноября", "декабря"],
            12: ["января", "февраля", "марта", "апреля", "мая", "июня", 
                "июля", "августа", "сентября", "октября", "ноября", "декабря"]
        }
        
        all_passed = True
        
        for duration in durations:
            contract_data = {
                "name_or_organization": f"Тест Длительность {duration}",
                "other_details": "Тестовые данные",
                "service_cost": 40000,
                "duration_months": duration
            }
            
            success, response = self.run_test(
                f"End Date Calculation - {duration} months",
                "POST",
                "contracts/direct",
                200,
                data=contract_data,
                return_response=True
            )
            
            if success and 'id' in response:
                self.created_contract_ids.append(response['id'])
                end_date = response.get('contract_end_date', '')
                end_month = response.get('contract_end_month', '')
                end_year = response.get('contract_end_year', '')
                
                # Check if end_date is a valid day (1-31)
                try:
                    day = int(end_date)
                    if 1 <= day <= 31:
                        print(f"   ✅ Valid end date: {end_date}")
                    else:
                        print(f"   ❌ Invalid end date: {end_date}")
                        all_passed = False
                except:
                    print(f"   ❌ Invalid end date format: {end_date}")
                    all_passed = False
                
                # Check if end_month is a valid Russian month
                if end_month in expected_months[duration]:
                    print(f"   ✅ Valid Russian month: {end_month}")
                else:
                    print(f"   ❌ Invalid month: {end_month}")
                    all_passed = False
                
                # CRITICAL: Check if end_year is present and valid
                if end_year:
                    try:
                        year = int(end_year)
                        current_year = datetime.now().year
                        if current_year <= year <= current_year + 2:  # Allow up to 2 years in future
                            print(f"   ✅ Valid end year: {end_year}")
                            
                            # SPECIFIC TEST: For 6 months duration, verify year calculation
                            if duration == 6:
                                current_month = datetime.now().month
                                expected_year = current_year
                                if current_month + 6 > 12:
                                    expected_year = current_year + 1
                                
                                if year == expected_year:
                                    print(f"   ✅ Correct year calculation for 6 months: {year}")
                                else:
                                    print(f"   ❌ Wrong year calculation for 6 months: got {year}, expected {expected_year}")
                                    all_passed = False
                        else:
                            print(f"   ❌ Invalid end year: {end_year}")
                            all_passed = False
                    except:
                        print(f"   ❌ Invalid end year format: {end_year}")
                        all_passed = False
                else:
                    print(f"   ❌ Missing contract_end_year field")
                    all_passed = False
            else:
                all_passed = False
                
        return all_passed

    def test_direct_contract_creation(self):
        """Test the new direct contract creation API with test data"""
        test_data = {
            "name_or_organization": "ООО Тест Компания",
            "other_details": "Адрес: г. Казань\nИНН: 1234567890",
            "service_cost": 30000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Direct Contract Creation",
            "POST",
            "contracts/direct",
            200,
            data=test_data,
            return_response=True
        )
        
        if success and 'id' in response:
            self.created_contract_ids.append(response['id'])
            
            # Verify all required fields are present and auto-generated
            checks = [
                ('contract_number', response.get('contract_number', '')),
                ('service_cost_words', response.get('service_cost_words', '')),
                ('contract_start_date', response.get('contract_start_date', '')),
                ('contract_end_date', response.get('contract_end_date', '')),
                ('contract_end_month', response.get('contract_end_month', '')),
                ('contract_content', response.get('contract_content', ''))
            ]
            
            all_fields_present = True
            for field_name, field_value in checks:
                if field_value:
                    print(f"   ✅ {field_name}: present")
                else:
                    print(f"   ❌ {field_name}: missing")
                    all_fields_present = False
            
            # Check contract content formatting
            contract_content = response.get('contract_content', '')
            content_checks = [
                ('Client name in content', 'ООО Тест Компания' in contract_content),
                ('Client details in content', 'г. Казань' in contract_content),
                ('INN in content', '1234567890' in contract_content),
                ('Service cost in content', '30000' in contract_content),
                ('Service cost words in content', 'тридцать тысяч' in contract_content)
            ]
            
            for check_name, check_result in content_checks:
                if check_result:
                    print(f"   ✅ {check_name}")
                else:
                    print(f"   ❌ {check_name}")
                    all_fields_present = False
            
            return all_fields_present
            
        return False

    def test_contract_retrieval(self):
        """Test contract retrieval endpoints"""
        # First create a contract to retrieve
        contract_data = {
            "name_or_organization": "Тест Получение Договора",
            "other_details": "Данные для получения",
            "service_cost": 25000,
            "duration_months": 12
        }
        
        success, response = self.run_test(
            "Create Contract for Retrieval Test",
            "POST",
            "contracts/direct",
            200,
            data=contract_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            return False
            
        contract_id = response['id']
        self.created_contract_ids.append(contract_id)
        
        # Test GET /api/contracts/direct (list all)
        success1, response1 = self.run_test(
            "Get All Direct Contracts",
            "GET",
            "contracts/direct",
            200,
            return_response=True
        )
        
        list_success = False
        if success1:
            contracts = response1 if isinstance(response1, list) else []
            print(f"   Found {len(contracts)} contracts")
            # Check if our contract is in the list
            for contract in contracts:
                if contract.get('id') == contract_id:
                    print(f"   ✅ Created contract found in list")
                    list_success = True
                    break
            if not list_success:
                print(f"   ❌ Created contract not found in list")
        
        # Test GET /api/contracts/direct/{id} (specific contract)
        success2, response2 = self.run_test(
            "Get Specific Direct Contract",
            "GET",
            f"contracts/direct/{contract_id}",
            200,
            return_response=True
        )
        
        specific_success = False
        if success2:
            if response2.get('id') == contract_id:
                print(f"   ✅ Retrieved correct contract by ID")
                print(f"   Client: {response2.get('client_name', 'N/A')}")
                print(f"   Cost: {response2.get('service_cost', 'N/A')}")
                specific_success = True
            else:
                print(f"   ❌ Retrieved wrong contract")
        
        return list_success and specific_success

    def test_contract_updates(self):
        """Test contract updates with PUT /api/contracts/direct/{id}"""
        # First create a contract to update
        original_data = {
            "name_or_organization": "Оригинальная Компания",
            "other_details": "Оригинальные данные",
            "service_cost": 20000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Create Contract for Update Test",
            "POST",
            "contracts/direct",
            200,
            data=original_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            return False
            
        contract_id = response['id']
        self.created_contract_ids.append(contract_id)
        original_contract_number = response.get('contract_number', '')
        
        # Update the contract
        updated_data = {
            "name_or_organization": "Обновленная Компания",
            "other_details": "Обновленные данные\nНовый адрес",
            "service_cost": 45000,
            "duration_months": 12
        }
        
        success, response = self.run_test(
            "Update Direct Contract",
            "PUT",
            f"contracts/direct/{contract_id}",
            200,
            data=updated_data,
            return_response=True
        )
        
        if success:
            # Verify updates
            checks = [
                ('Client name updated', response.get('client_name') == 'Обновленная Компания'),
                ('Client details updated', 'Обновленные данные' in response.get('client_details', '')),
                ('Service cost updated', response.get('service_cost') == 45000),
                ('Cost words updated', 'сорок пять тысяч' in response.get('service_cost_words', '')),
                ('Contract number preserved', response.get('contract_number') == original_contract_number)
            ]
            
            all_updated = True
            for check_name, check_result in checks:
                if check_result:
                    print(f"   ✅ {check_name}")
                else:
                    print(f"   ❌ {check_name}")
                    all_updated = False
            
            # Check contract content has new data
            contract_content = response.get('contract_content', '')
            content_checks = [
                ('Updated name in content', 'Обновленная Компания' in contract_content),
                ('Updated details in content', 'Обновленные данные' in contract_content),
                ('Updated cost in content', '45000' in contract_content),
                ('Updated cost words in content', 'сорок пять тысяч' in contract_content)
            ]
            
            for check_name, check_result in content_checks:
                if check_result:
                    print(f"   ✅ {check_name}")
                else:
                    print(f"   ❌ {check_name}")
                    all_updated = False
            
            return all_updated
            
        return False

    def test_word_document_improvements(self):
        """Test Word document generation with new header format and section 11 improvements"""
        # Create a contract for Word document testing
        contract_data = {
            "name_or_organization": "ООО Тест Документ",
            "other_details": "Тестовые данные для проверки документа\nАдрес: г. Казань, ул. Тестовая, 1",
            "service_cost": 50000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Create Contract for Word Document Test",
            "POST",
            "contracts/direct",
            200,
            data=contract_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            return False
            
        contract_id = response['id']
        self.created_contract_ids.append(contract_id)
        
        # Test Word document download
        url = f"{self.api_url}/contracts/direct/{contract_id}/download"
        
        self.tests_run += 1
        print(f"\n🔍 Testing Word Document Improvements...")
        print(f"   URL: {url}")
        
        try:
            download_response = requests.get(url)
            
            success = download_response.status_code == 200
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {download_response.status_code}")
                
                # Check Content-Type header
                content_type = download_response.headers.get('Content-Type', '')
                expected_content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                if expected_content_type in content_type:
                    print("   ✅ Correct Content-Type for Word document")
                else:
                    print(f"   ❌ Wrong Content-Type: {content_type}")
                    return False
                
                # Check file size (Word documents should have reasonable size)
                content_length = len(download_response.content)
                if content_length > 5000:  # At least 5KB for a Word document with improvements
                    print(f"   ✅ File size reasonable: {content_length} bytes")
                else:
                    print(f"   ❌ File size too small: {content_length} bytes")
                    return False
                
                # Check if it's actually a Word document by checking magic bytes
                if download_response.content.startswith(b'PK'):  # ZIP-based format (Word .docx)
                    print("   ✅ File appears to be a valid Word document (ZIP-based)")
                else:
                    print("   ❌ File does not appear to be a valid Word document")
                    return False
                
                # Save the document temporarily to check content
                import tempfile
                import zipfile
                import xml.etree.ElementTree as ET
                
                with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                    temp_file.write(download_response.content)
                    temp_file_path = temp_file.name
                
                try:
                    # Extract and check document content
                    with zipfile.ZipFile(temp_file_path, 'r') as docx_zip:
                        # Read the main document XML
                        document_xml = docx_zip.read('word/document.xml').decode('utf-8')
                        
                        # Check for "Казань" in the document
                        if 'Казань' in document_xml:
                            print("   ✅ 'Казань' found in document header")
                        else:
                            print("   ❌ 'Казань' NOT found in document header")
                            return False
                        
                        # Check for Russian month names (indicating date formatting)
                        russian_months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                                        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
                        month_found = any(month in document_xml for month in russian_months)
                        if month_found:
                            print("   ✅ Russian month names found in document (proper date formatting)")
                        else:
                            print("   ❌ Russian month names NOT found in document")
                            return False
                        
                        # Check for section 11 content
                        if '11. ЮРИДИЧЕСКИЕ АДРЕСА И БАНКОВСКИЕ РЕКВИЗИТЫ СТОРОН' in document_xml:
                            print("   ✅ Section 11 found in document")
                        else:
                            print("   ❌ Section 11 NOT found in document")
                            return False
                        
                        # Check for page break before section 11 (indicated by page break XML)
                        if 'w:br w:type="page"' in document_xml or '<w:br w:type="page"/>' in document_xml:
                            print("   ✅ Page break found in document (section 11 on new page)")
                        else:
                            print("   ❌ Page break NOT found in document")
                            return False
                        
                        # Check for compact executor details (should have fewer line breaks)
                        executor_section = document_xml[document_xml.find('«Исполнитель»:'):document_xml.find('«Заказчик»:')]
                        if executor_section:
                            # Count line breaks in executor section
                            line_breaks = executor_section.count('<w:br/>') + executor_section.count('<w:br ')
                            if line_breaks < 10:  # Should be more compact now
                                print(f"   ✅ Executor details are compact ({line_breaks} line breaks)")
                            else:
                                print(f"   ❌ Executor details not compact enough ({line_breaks} line breaks)")
                                return False
                        
                        # Check for contract end year in document content
                        end_year = response.get('contract_end_year', '')
                        if end_year and end_year in document_xml:
                            print(f"   ✅ Contract end year ({end_year}) found in document")
                        else:
                            print(f"   ❌ Contract end year ({end_year}) NOT found in document")
                            return False
                        
                        print("   ✅ All Word document improvements verified successfully")
                        return True
                        
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
                
            else:
                print(f"❌ Failed - Expected 200, got {download_response.status_code}")
                print(f"   Response: {download_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

    def test_word_download(self):
        """Test Word document download with GET /api/contracts/direct/{id}/download"""
        # Create a contract for download testing
        contract_data = {
            "name_or_organization": "Компания для Скачивания",
            "other_details": "Данные для скачивания документа",
            "service_cost": 35000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Create Contract for Download Test",
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
        
        # Test download
        url = f"{self.api_url}/contracts/direct/{contract_id}/download"
        
        self.tests_run += 1
        print(f"\n🔍 Testing Word Download for Direct Contract...")
        print(f"   URL: {url}")
        
        try:
            download_response = requests.get(url)
            
            success = download_response.status_code == 200
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {download_response.status_code}")
                
                # Check Content-Type header
                content_type = download_response.headers.get('Content-Type', '')
                expected_content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                if expected_content_type in content_type:
                    print("   ✅ Correct Content-Type for Word document")
                else:
                    print(f"   ❌ Wrong Content-Type: {content_type}")
                
                # Check Content-Disposition header for filename
                content_disposition = download_response.headers.get('Content-Disposition', '')
                if 'attachment' in content_disposition and 'filename=' in content_disposition:
                    print("   ✅ Correct Content-Disposition header with filename")
                    # Extract filename
                    filename_part = content_disposition.split('filename=')[1]
                    print(f"   📄 Filename: {filename_part}")
                    
                    # Check if filename contains contract number
                    contract_number_in_filename = contract_number.replace('.', '_')
                    if contract_number_in_filename in filename_part and '.docx' in filename_part:
                        print("   ✅ Filename contains contract number and .docx extension")
                    else:
                        print("   ❌ Filename format incorrect")
                else:
                    print(f"   ❌ Wrong Content-Disposition: {content_disposition}")
                
                # Check file size (Word documents should have reasonable size)
                content_length = len(download_response.content)
                if content_length > 1000:  # At least 1KB for a Word document
                    print(f"   ✅ File size reasonable: {content_length} bytes")
                else:
                    print(f"   ❌ File size too small: {content_length} bytes")
                
                # Check if it's actually a Word document by checking magic bytes
                if download_response.content.startswith(b'PK'):  # ZIP-based format (Word .docx)
                    print("   ✅ File appears to be a valid Word document (ZIP-based)")
                else:
                    print("   ❌ File does not appear to be a valid Word document")
                
                return True
            else:
                print(f"❌ Failed - Expected 200, got {download_response.status_code}")
                print(f"   Response: {download_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

    def test_contract_content_editing(self):
        """Test new contract content editing endpoints - PUT /api/contracts/direct/{id}/content"""
        # Create a contract for content editing testing
        contract_data = {
            "name_or_organization": "ООО Тест Редактирование",
            "other_details": "Данные для тестирования редактирования содержимого",
            "service_cost": 40000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Create Contract for Content Editing Test",
            "POST",
            "contracts/direct",
            200,
            data=contract_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            return False
            
        contract_id = response['id']
        original_content = response.get('contract_content', '')
        self.created_contract_ids.append(contract_id)
        
        print(f"   Original content length: {len(original_content)} characters")
        
        # Test updating contract content
        custom_content = """**Договор об оказании услуг № {contract_number}**

ИЗМЕНЕННОЕ СОДЕРЖИМОЕ ДОГОВОРА

г. Казань «___» 2025 г.

Индивидуальный предприниматель Шамсутдинов Радис Раисович, именуемый в дальнейшем «Исполнитель» с одной стороны и ООО Тест Редактирование, именуемый в дальнейшем «Заказчик», с другой стороны, далее совместно именуемые «Стороны» заключили настоящий Договор о нижеследующем:

**1. ПРЕДМЕТ ДОГОВОРА**

1.1. Данный договор был изменен через новый API endpoint для редактирования содержимого.

1.2. Исполнитель обязуется оказать услуги по созданию и ведению рекламных кампаний.

**2. СТОИМОСТЬ УСЛУГ**

2.1. Стоимость услуг составляет 40000 (сорок тысяч) рублей.

**3. ЗАКЛЮЧИТЕЛЬНЫЕ ПОЛОЖЕНИЯ**

3.1. Настоящий договор составлен в двух экземплярах.

**ПОДПИСИ СТОРОН**

Исполнитель: ________________/Шамсутдинов Р.Р.

Заказчик: ________________/ООО Тест Редактирование"""

        content_update_data = {
            "contract_content": custom_content
        }
        
        success, response = self.run_test(
            "Update Contract Content",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            200,
            data=content_update_data,
            return_response=True
        )
        
        if not success:
            return False
        
        # Verify content was updated
        updated_content = response.get('contract_content', '')
        if updated_content == custom_content:
            print("   ✅ Contract content updated successfully")
        else:
            print("   ❌ Contract content not updated correctly")
            return False
        
        # Verify other fields remain unchanged
        checks = [
            ('Contract ID preserved', response.get('id') == contract_id),
            ('Client name preserved', response.get('client_name') == 'ООО Тест Редактирование'),
            ('Service cost preserved', response.get('service_cost') == 40000),
            ('Contract number preserved', response.get('contract_number') is not None)
        ]
        
        all_preserved = True
        for check_name, check_result in checks:
            if check_result:
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name}")
                all_preserved = False
        
        # Verify content contains our custom text
        content_checks = [
            ('Custom header found', 'ИЗМЕНЕННОЕ СОДЕРЖИМОЕ ДОГОВОРА' in updated_content),
            ('Custom clause found', 'изменен через новый API endpoint' in updated_content),
            ('Original client name preserved', 'ООО Тест Редактирование' in updated_content),
            ('Original cost preserved', '40000' in updated_content and 'сорок тысяч' in updated_content)
        ]
        
        for check_name, check_result in content_checks:
            if check_result:
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name}")
                all_preserved = False
        
        # Test retrieving the contract to verify content persisted in database
        success, db_response = self.run_test(
            "Verify Content Persisted in Database",
            "GET",
            f"contracts/direct/{contract_id}",
            200,
            return_response=True
        )
        
        if success:
            db_content = db_response.get('contract_content', '')
            if db_content == custom_content:
                print("   ✅ Updated content persisted in database")
            else:
                print("   ❌ Updated content NOT persisted in database")
                all_preserved = False
        else:
            print("   ❌ Failed to retrieve contract from database")
            all_preserved = False
        
        return all_preserved

    def test_custom_contract_download(self):
        """Test custom contract download with GET /api/contracts/direct/{id}/download_custom"""
        # Create a contract for custom download testing
        contract_data = {
            "name_or_organization": "ООО Тест Кастомное Скачивание",
            "other_details": "Данные для тестирования кастомного скачивания",
            "service_cost": 60000,
            "duration_months": 12
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

КАСТОМНОЕ СОДЕРЖИМОЕ ДЛЯ СКАЧИВАНИЯ

г. Казань «___» 2025 г.

Индивидуальный предприниматель Шамсутдинов Радис Раисович, именуемый в дальнейшем «Исполнитель» с одной стороны и ООО Тест Кастомное Скачивание, именуемый в дальнейшем «Заказчик», с другой стороны.

**1. ПРЕДМЕТ ДОГОВОРА**

1.1. Этот договор содержит кастомное содержимое для тестирования функции скачивания измененного документа.

1.2. Исполнитель обязуется оказать услуги по созданию рекламных кампаний стоимостью 60000 рублей.

**2. ОСОБЫЕ УСЛОВИЯ**

2.1. Данный раздел добавлен для проверки кастомного содержимого.

2.2. Договор действует в течение 12 месяцев.

**3. ПОДПИСИ СТОРОН**

Исполнитель: ________________/Шамсутдинов Р.Р.

Заказчик: ________________/ООО Тест Кастомное Скачивание

КОНЕЦ КАСТОМНОГО СОДЕРЖИМОГО"""

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
        
        self.tests_run += 1
        print(f"\n🔍 Testing Custom Contract Download...")
        print(f"   URL: {url}")
        
        try:
            download_response = requests.get(url)
            
            success = download_response.status_code == 200
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {download_response.status_code}")
                
                # Check Content-Type header
                content_type = download_response.headers.get('Content-Type', '')
                expected_content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                if expected_content_type in content_type:
                    print("   ✅ Correct Content-Type for Word document")
                else:
                    print(f"   ❌ Wrong Content-Type: {content_type}")
                    return False
                
                # Check Content-Disposition header for filename
                content_disposition = download_response.headers.get('Content-Disposition', '')
                if 'attachment' in content_disposition and 'filename=' in content_disposition:
                    print("   ✅ Correct Content-Disposition header with filename")
                    # Extract filename
                    filename_part = content_disposition.split('filename=')[1]
                    print(f"   📄 Filename: {filename_part}")
                    
                    # Check if filename contains 'custom' and contract info
                    if 'custom' in filename_part.lower() and '.docx' in filename_part:
                        print("   ✅ Filename indicates custom document and has .docx extension")
                    else:
                        print("   ❌ Filename format incorrect for custom document")
                        return False
                else:
                    print(f"   ❌ Wrong Content-Disposition: {content_disposition}")
                    return False
                
                # Check file size (Word documents should have reasonable size)
                content_length = len(download_response.content)
                if content_length > 1000:  # At least 1KB for a Word document
                    print(f"   ✅ File size reasonable: {content_length} bytes")
                else:
                    print(f"   ❌ File size too small: {content_length} bytes")
                    return False
                
                # Check if it's actually a Word document by checking magic bytes
                if download_response.content.startswith(b'PK'):  # ZIP-based format (Word .docx)
                    print("   ✅ File appears to be a valid Word document (ZIP-based)")
                else:
                    print("   ❌ File does not appear to be a valid Word document")
                    return False
                
                # Verify document contains custom content
                import tempfile
                import zipfile
                
                with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                    temp_file.write(download_response.content)
                    temp_file_path = temp_file.name
                
                try:
                    # Extract and check document content
                    with zipfile.ZipFile(temp_file_path, 'r') as docx_zip:
                        # Read the main document XML
                        document_xml = docx_zip.read('word/document.xml').decode('utf-8')
                        
                        # Check for custom content markers
                        custom_checks = [
                            ('Custom header', 'КАСТОМНОЕ СОДЕРЖИМОЕ ДЛЯ СКАЧИВАНИЯ' in document_xml),
                            ('Custom clause', 'кастомное содержимое для тестирования' in document_xml),
                            ('Special section', 'ОСОБЫЕ УСЛОВИЯ' in document_xml),
                            ('Custom ending', 'КОНЕЦ КАСТОМНОГО СОДЕРЖИМОГО' in document_xml),
                            ('Client name', 'ООО Тест Кастомное Скачивание' in document_xml),
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
                    import os
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass
                
            else:
                print(f"❌ Failed - Expected 200, got {download_response.status_code}")
                print(f"   Response: {download_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False

    def test_contract_content_validation(self):
        """Test ContractContentUpdate model validation"""
        # Create a contract for validation testing
        contract_data = {
            "name_or_organization": "ООО Тест Валидация",
            "other_details": "Данные для тестирования валидации",
            "service_cost": 25000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Create Contract for Validation Test",
            "POST",
            "contracts/direct",
            200,
            data=contract_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            return False
            
        contract_id = response['id']
        self.created_contract_ids.append(contract_id)
        
        # Test 1: Valid content update
        valid_content = "Валидное содержимое договора для тестирования модели ContractContentUpdate"
        valid_data = {"contract_content": valid_content}
        
        success, response = self.run_test(
            "Valid Content Update",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            200,
            data=valid_data,
            return_response=True
        )
        
        if not success:
            return False
        
        if response.get('contract_content') == valid_content:
            print("   ✅ Valid content update successful")
        else:
            print("   ❌ Valid content update failed")
            return False
        
        # Test 2: Empty content (should be rejected)
        empty_data = {"contract_content": ""}
        
        success, response = self.run_test(
            "Empty Content Update (Should Fail)",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            422,  # Validation error expected
            data=empty_data,
            return_response=True
        )
        
        if success:  # Success means we got the expected 422 status
            print("   ✅ Empty content properly rejected with validation error")
        else:
            print("   ❌ Empty content was not properly rejected")
            return False
        
        # Test 3: Missing contract_content field
        missing_field_data = {"wrong_field": "some content"}
        
        success, response = self.run_test(
            "Missing Field Update (Should Fail)",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            422,  # Validation error expected
            data=missing_field_data,
            return_response=True
        )
        
        if success:  # Success means we got the expected 422 status
            print("   ✅ Missing field properly rejected with validation error")
        else:
            print("   ❌ Missing field was not properly rejected")
            return False
        
        # Test 4: Very long content (should be accepted)
        long_content = "Очень длинное содержимое договора. " * 100  # 3700+ characters
        long_data = {"contract_content": long_content}
        
        success, response = self.run_test(
            "Long Content Update",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            200,
            data=long_data,
            return_response=True
        )
        
        if success and response.get('contract_content') == long_content:
            print(f"   ✅ Long content ({len(long_content)} chars) accepted successfully")
        else:
            print("   ❌ Long content update failed")
            return False
        
        # Test 5: Content with special characters and formatting
        special_content = """Договор с **жирным текстом**, _курсивом_ и специальными символами:
        
№ 123-456/789
Стоимость: 25,000.00 ₽
Email: test@example.com
Телефон: +7 (123) 456-78-90
Адрес: г. Москва, ул. Тестовая, д. 1, кв. 2

"Кавычки", 'апострофы', и другие символы: @#$%^&*()[]{}|\\:";'<>?,./

Многострочный
текст
с переносами"""
        
        special_data = {"contract_content": special_content}
        
        success, response = self.run_test(
            "Special Characters Content Update",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            200,
            data=special_data,
            return_response=True
        )
        
        if success and response.get('contract_content') == special_content:
            print("   ✅ Content with special characters accepted successfully")
        else:
            print("   ❌ Content with special characters update failed")
            return False
        
        print("   ✅ All ContractContentUpdate model validation tests passed")
        return True

    def test_contract_content_editing_workflow(self):
        """
        COMPREHENSIVE TEST FOR CONTRACT CONTENT EDITING AND DOWNLOAD FUNCTIONALITY
        
        This test specifically addresses the user-reported issue:
        "When editing contract content and clicking download, the edits are not reflected in the downloaded Word document"
        
        Test workflow:
        1. Create contract → Edit content → Save changes → Download document → Verify that downloaded Word document contains the edited content
        2. Test regular download endpoint still works for non-edited contracts
        3. Test edge cases like empty content, special characters, and long text
        """
        print("\n🔍 COMPREHENSIVE CONTRACT CONTENT EDITING WORKFLOW TEST")
        print("=" * 70)
        
        # Step 1: Create a contract
        print("\n📝 Step 1: Creating initial contract...")
        contract_data = {
            "name_or_organization": "ООО Тест Редактирование Контента",
            "other_details": "Адрес: г. Казань, ул. Тестовая, 123\nИНН: 1234567890\nТел: +7(843)123-45-67",
            "service_cost": 50000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Create Contract for Workflow Test",
            "POST",
            "contracts/direct",
            200,
            data=contract_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            print("❌ Failed to create contract for workflow test")
            return False
        
        contract_id = response['id']
        original_content = response['contract_content']
        contract_number = response['contract_number']
        self.created_contract_ids.append(contract_id)
        
        print(f"✅ Contract created successfully: {contract_id}")
        print(f"   Original content length: {len(original_content)} characters")
        
        # Step 2: Test regular download (before editing)
        print("\n📥 Step 2: Testing regular download before editing...")
        url = f"{self.api_url}/contracts/direct/{contract_id}/download"
        
        self.tests_run += 1
        try:
            download_response = requests.get(url)
            if download_response.status_code == 200:
                self.tests_passed += 1
                print("✅ Regular download works before editing")
                print(f"   File size: {len(download_response.content)} bytes")
            else:
                print(f"❌ Regular download failed: {download_response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error with regular download: {str(e)}")
            return False
        
        # Step 3: Edit contract content
        print("\n✏️  Step 3: Editing contract content...")
        edited_content = f"""**Договор об оказании услуг № {contract_number}**

ОТРЕДАКТИРОВАННОЕ СОДЕРЖИМОЕ ДОГОВОРА - ТЕСТ ФУНКЦИОНАЛЬНОСТИ

г. Казань «___» 2025 г.

Индивидуальный предприниматель Шамсутдинов Радис Раисович, именуемый в дальнейшем «Исполнитель» с одной стороны и ООО Тест Редактирование Контента, именуемый в дальнейшем «Заказчик», с другой стороны, далее совместно именуемые «Стороны» заключили настоящий Договор о нижеследующем:

**1. ПРЕДМЕТ ДОГОВОРА**

1.1. ЭТОТ ТЕКСТ БЫЛ ДОБАВЛЕН ЧЕРЕЗ API РЕДАКТИРОВАНИЯ СОДЕРЖИМОГО.

1.2. Исполнитель принимает на себя обязательства оказать комплекс услуг в соответствии с заявками Заказчика.

1.3. СПЕЦИАЛЬНАЯ ПРОВЕРКА: Стоимость услуг составляет 50000 (пятьдесят тысяч) рублей.

**2. СРОК ДЕЙСТВИЯ ДОГОВОРА**

2.1. Настоящий Договор вступает в силу с даты его подписания Сторонами.

2.2. ОТРЕДАКТИРОВАННЫЙ РАЗДЕЛ: Договор действует в течение 6 месяцев.

**3. ПРАВА И ОБЯЗАННОСТИ СТОРОН**

3.1. Исполнитель обязан:
- Приступить к оказанию Услуг в течение трех дней
- Консультировать Заказчика по всем вопросам
- НОВОЕ ОБЯЗАТЕЛЬСТВО: Уведомлять о всех изменениях в договоре

3.2. Заказчик обязан:
- Предоставлять необходимую информацию
- Оплатить Услуги в установленные сроки
- НОВОЕ ОБЯЗАТЕЛЬСТВО: Подтверждать получение отредактированного договора

**4. ЗАКЛЮЧИТЕЛЬНЫЕ ПОЛОЖЕНИЯ**

4.1. Настоящий Договор составлен в двух экземплярах.

4.2. ПРОВЕРКА РЕДАКТИРОВАНИЯ: Данный текст должен появиться в скачанном документе.

**ПОДПИСИ СТОРОН**

Исполнитель: ________________/Шамсутдинов Р.Р.

Заказчик: ________________/ООО Тест Редактирование Контента

КОНЕЦ ОТРЕДАКТИРОВАННОГО СОДЕРЖИМОГО - МАРКЕР ДЛЯ ПРОВЕРКИ"""

        content_update = {"contract_content": edited_content}
        
        success, edit_response = self.run_test(
            "Edit Contract Content",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            200,
            data=content_update,
            return_response=True
        )
        
        if not success:
            print("❌ Failed to edit contract content")
            return False
        
        # Verify content was actually updated
        if edit_response['contract_content'] == edited_content:
            print("✅ Content update verified in API response")
        else:
            print("❌ Content update not reflected in API response")
            return False
        
        # Step 4: Verify content persisted in database
        print("\n🗄️  Step 4: Verifying content persisted in database...")
        success, db_response = self.run_test(
            "Verify Content Persisted",
            "GET",
            f"contracts/direct/{contract_id}",
            200,
            return_response=True
        )
        
        if success and db_response['contract_content'] == edited_content:
            print("✅ Edited content persisted in database")
        else:
            print("❌ Edited content NOT persisted in database")
            return False
        
        # Step 5: Test custom download with edited content
        print("\n📥 Step 5: Testing custom download with edited content...")
        url = f"{self.api_url}/contracts/direct/{contract_id}/download_custom"
        
        self.tests_run += 1
        try:
            custom_download_response = requests.get(url)
            if custom_download_response.status_code != 200:
                print(f"❌ Custom download failed: {custom_download_response.status_code}")
                return False
            
            self.tests_passed += 1
            print("✅ Custom download successful")
            print(f"   File size: {len(custom_download_response.content)} bytes")
            
            # Check Content-Type
            content_type = custom_download_response.headers.get('Content-Type', '')
            if 'wordprocessingml.document' in content_type:
                print("✅ Correct Word document Content-Type")
            else:
                print(f"❌ Wrong Content-Type: {content_type}")
                return False
            
            # Check filename
            content_disposition = custom_download_response.headers.get('Content-Disposition', '')
            if 'редактированный' in content_disposition or 'custom' in content_disposition.lower():
                print("✅ Filename indicates edited/custom document")
            else:
                print(f"❌ Filename doesn't indicate custom document: {content_disposition}")
                return False
            
        except Exception as e:
            print(f"❌ Error with custom download: {str(e)}")
            return False
        
        # Step 6: Verify Word document contains edited content
        print("\n🔍 Step 6: Verifying Word document contains edited content...")
        try:
            import tempfile
            import zipfile
            
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                temp_file.write(custom_download_response.content)
                temp_file_path = temp_file.name
            
            # Extract and check document content
            with zipfile.ZipFile(temp_file_path, 'r') as docx_zip:
                document_xml = docx_zip.read('word/document.xml').decode('utf-8')
                
                # Check for specific edited content markers
                content_checks = [
                    ('Edited header', 'ОТРЕДАКТИРОВАННОЕ СОДЕРЖИМОЕ ДОГОВОРА' in document_xml),
                    ('API edit marker', 'ЧЕРЕЗ API РЕДАКТИРОВАНИЯ СОДЕРЖИМОГО' in document_xml),
                    ('New obligation', 'НОВОЕ ОБЯЗАТЕЛЬСТВО' in document_xml),
                    ('Edit verification', 'ПРОВЕРКА РЕДАКТИРОВАНИЯ' in document_xml),
                    ('End marker', 'КОНЕЦ ОТРЕДАКТИРОВАННОГО СОДЕРЖИМОГО' in document_xml),
                    ('Client name', 'ООО Тест Редактирование Контента' in document_xml),
                    ('Contract number', contract_number in document_xml),
                    ('Kazan header', 'Казань' in document_xml)
                ]
                
                all_content_found = True
                for check_name, check_result in content_checks:
                    if check_result:
                        print(f"   ✅ {check_name} found in Word document")
                    else:
                        print(f"   ❌ {check_name} NOT found in Word document")
                        all_content_found = False
                
                if not all_content_found:
                    print("❌ Some edited content missing from Word document")
                    return False
                
                print("✅ All edited content verified in Word document")
            
            # Clean up temp file
            import os
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
        except Exception as e:
            print(f"❌ Error verifying Word document content: {str(e)}")
            return False
        
        # Step 7: Test regular download still works (should use template)
        print("\n📥 Step 7: Testing regular download still works after editing...")
        self.tests_run += 1
        try:
            regular_download_response = requests.get(f"{self.api_url}/contracts/direct/{contract_id}/download")
            if regular_download_response.status_code == 200:
                self.tests_passed += 1
                print("✅ Regular download still works after editing")
                print(f"   File size: {len(regular_download_response.content)} bytes")
                
                # Regular download should use template, not custom content
                with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                    temp_file.write(regular_download_response.content)
                    temp_file_path = temp_file.name
                
                with zipfile.ZipFile(temp_file_path, 'r') as docx_zip:
                    regular_xml = docx_zip.read('word/document.xml').decode('utf-8')
                    
                    # Regular download should use template formatting, not custom content
                    if 'ОТРЕДАКТИРОВАННОЕ СОДЕРЖИМОЕ ДОГОВОРА' not in regular_xml:
                        print("✅ Regular download uses template (not custom content)")
                    else:
                        print("❌ Regular download incorrectly uses custom content")
                        return False
                    
                    # But should still have basic contract info
                    if contract_number in regular_xml and 'ООО Тест Редактирование Контента' in regular_xml:
                        print("✅ Regular download contains correct contract data")
                    else:
                        print("❌ Regular download missing contract data")
                        return False
                
                # Clean up temp file
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                    
            else:
                print(f"❌ Regular download failed after editing: {regular_download_response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error with regular download after editing: {str(e)}")
            return False
        
        print("\n🎉 CONTRACT CONTENT EDITING WORKFLOW TEST COMPLETED SUCCESSFULLY!")
        print("✅ All critical functionality verified:")
        print("   • Contract content can be edited via PUT /api/contracts/direct/{id}/content")
        print("   • Edited content persists in database")
        print("   • Custom download generates Word documents with edited content")
        print("   • Regular download still works with template formatting")
        
        return True

    def cleanup_contracts(self):
        """Clean up all created contracts"""
        print(f"\n🧹 Cleaning up {len(self.created_contract_ids)} created contracts...")
        for contract_id in self.created_contract_ids:
            try:
                requests.delete(f"{self.api_url}/contracts/direct/{contract_id}")
            except:
                pass
        self.created_contract_ids = []

class ContractSystemTester:
    def __init__(self, base_url="https://contract-forge.preview.emergentagent.com"):
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
    print("=" * 80)
    
    # Test new direct contract functionality first
    print("\n" + "=" * 80)
    print("🆕 TESTING NEW DIRECT CONTRACT FUNCTIONALITY")
    print("=" * 80)
    
    direct_tester = DirectContractTester()
    
    # Direct contract test sequence
    direct_test_sequence = [
        ("Number to Words Conversion", direct_tester.test_number_to_words_conversion),
        ("Contract Number Generation", direct_tester.test_contract_number_generation),
        ("Contract End Date Calculation", direct_tester.test_contract_end_date_calculation),
        ("Direct Contract Creation", direct_tester.test_direct_contract_creation),
        ("Contract Retrieval", direct_tester.test_contract_retrieval),
        ("Contract Updates", direct_tester.test_contract_updates),
        ("Word Document Improvements", direct_tester.test_word_document_improvements),
        ("Word Download", direct_tester.test_word_download),
        ("Contract Content Editing", direct_tester.test_contract_content_editing),
        ("Custom Contract Download", direct_tester.test_custom_contract_download),
        ("Contract Content Validation", direct_tester.test_contract_content_validation),
    ]
    
    # Run direct contract tests
    for test_name, test_func in direct_test_sequence:
        try:
            test_func()
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {str(e)}")
    
    # Cleanup direct contracts
    direct_tester.cleanup_contracts()
    
    # Print direct contract test results
    print("\n" + "=" * 80)
    print(f"📊 Direct Contract Test Results:")
    print(f"   Tests run: {direct_tester.tests_run}")
    print(f"   Tests passed: {direct_tester.tests_passed}")
    print(f"   Success rate: {(direct_tester.tests_passed/direct_tester.tests_run*100):.1f}%")
    
    # Test legacy functionality
    print("\n" + "=" * 80)
    print("🔄 TESTING LEGACY CONTRACT FUNCTIONALITY")
    print("=" * 80)
    
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
        ("Download Contract Word", tester.test_download_contract_word),
        ("Kozlov Client & Contract Test", tester.test_create_petrov_client_and_contract),
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
    
    # Print legacy test results
    print("\n" + "=" * 80)
    print(f"📊 Legacy Contract Test Results:")
    print(f"   Tests run: {tester.tests_run}")
    print(f"   Tests passed: {tester.tests_passed}")
    print(f"   Success rate: {(tester.tests_passed/tester.tests_run*100):.1f}%")
    
    # Combined results
    total_tests = direct_tester.tests_run + tester.tests_run
    total_passed = direct_tester.tests_passed + tester.tests_passed
    
    print("\n" + "=" * 80)
    print(f"📊 OVERALL TEST RESULTS:")
    print(f"   Total tests run: {total_tests}")
    print(f"   Total tests passed: {total_passed}")
    print(f"   Overall success rate: {(total_passed/total_tests*100):.1f}%")
    
    if total_passed == total_tests:
        print("🎉 All backend tests passed!")
        return 0
    else:
        print("⚠️  Some backend tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())