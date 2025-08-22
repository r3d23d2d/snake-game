import requests
import sys
import json
from datetime import datetime

class DirectContractTester:
    """Test the new direct contract creation functionality"""
    
    def __init__(self, base_url="https://docuforge-4.preview.emergentagent.com"):
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
    def __init__(self, base_url="https://docuforge-4.preview.emergentagent.com"):
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
        ("Word Download", direct_tester.test_word_download),
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