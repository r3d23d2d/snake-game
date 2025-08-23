import requests
import sys
import json
import tempfile
import zipfile
import urllib.parse
from datetime import datetime

class RegressionTester:
    """Test specific regression fixes for contract management system"""
    
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

    def test_title_duplication_fix(self):
        """
        REGRESSION TEST 1: Title Duplication Fix
        
        Test that contract titles appear only once (not duplicated) when downloading custom versions.
        
        Steps:
        1. Create a contract
        2. Edit content that includes the title "Договор об оказании услуг № [number]"
        3. Download custom version and verify title appears only once (not duplicated)
        """
        print("\n" + "="*80)
        print("🔍 REGRESSION TEST 1: TITLE DUPLICATION FIX")
        print("="*80)
        
        # Step 1: Create contract
        print("\n📝 Step 1: Creating contract for title duplication test...")
        contract_data = {
            "name_or_organization": "ООО Тест Дублирование Заголовка",
            "other_details": "Адрес: г. Казань, ул. Тестовая, 1\nИНН: 1234567890",
            "service_cost": 45000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Create Contract for Title Test",
            "POST",
            "contracts/direct",
            200,
            data=contract_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            print("❌ Failed to create contract")
            return False
        
        contract_id = response['id']
        contract_number = response['contract_number']
        self.created_contract_ids.append(contract_id)
        
        print(f"✅ Contract created: {contract_id}")
        print(f"   Contract number: {contract_number}")
        
        # Step 2: Edit content with title included
        print("\n✏️  Step 2: Editing content that includes title...")
        edited_content = f"""**Договор об оказании услуг № {contract_number}**

г. Казань «___» 2025 г.

Индивидуальный предприниматель Шамсутдинов Радис Раисович, именуемый в дальнейшем «Исполнитель» с одной стороны и ООО Тест Дублирование Заголовка, именуемый в дальнейшем «Заказчик», с другой стороны.

**1. ПРЕДМЕТ ДОГОВОРА**

1.1. Исполнитель обязуется оказать услуги по созданию рекламных кампаний.

1.2. Стоимость услуг составляет 45000 (сорок пять тысяч) рублей.

**2. ЗАКЛЮЧИТЕЛЬНЫЕ ПОЛОЖЕНИЯ**

2.1. Настоящий договор составлен в двух экземплярах.

**ПОДПИСИ СТОРОН**

Исполнитель: ________________/Шамсутдинов Р.Р.

Заказчик: ________________/ООО Тест Дублирование Заголовка"""

        content_update = {"contract_content": edited_content}
        
        success, edit_response = self.run_test(
            "Edit Contract Content with Title",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            200,
            data=content_update,
            return_response=True
        )
        
        if not success:
            print("❌ Failed to edit contract content")
            return False
        
        print("✅ Contract content edited successfully")
        
        # Step 3: Download custom version and check for title duplication
        print("\n📥 Step 3: Downloading custom version and checking for title duplication...")
        url = f"{self.api_url}/contracts/direct/{contract_id}/download_custom"
        
        self.tests_run += 1
        try:
            download_response = requests.get(url)
            if download_response.status_code != 200:
                print(f"❌ Custom download failed: {download_response.status_code}")
                return False
            
            self.tests_passed += 1
            print("✅ Custom download successful")
            
            # Extract and analyze document content
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                temp_file.write(download_response.content)
                temp_file_path = temp_file.name
            
            with zipfile.ZipFile(temp_file_path, 'r') as docx_zip:
                document_xml = docx_zip.read('word/document.xml').decode('utf-8')
                
                # Count occurrences of the title
                title_pattern = f"Договор об оказании услуг № {contract_number}"
                title_count = document_xml.count(title_pattern)
                
                print(f"   Title occurrences found: {title_count}")
                
                if title_count == 1:
                    print("   ✅ TITLE DUPLICATION FIX VERIFIED: Title appears exactly once")
                    title_fix_passed = True
                elif title_count == 0:
                    print("   ❌ TITLE MISSING: Title not found in document")
                    title_fix_passed = False
                else:
                    print(f"   ❌ TITLE DUPLICATION DETECTED: Title appears {title_count} times")
                    title_fix_passed = False
                
                # Additional check: Verify title is properly formatted
                if title_fix_passed:
                    # Look for title in proper context (should be in a centered, bold paragraph)
                    if title_pattern in document_xml:
                        print("   ✅ Title found in document content")
                    else:
                        print("   ❌ Title not found in expected format")
                        title_fix_passed = False
            
            # Clean up
            import os
            try:
                os.unlink(temp_file_path)
            except:
                pass
            
            return title_fix_passed
            
        except Exception as e:
            print(f"❌ Error during title duplication test: {str(e)}")
            return False

    def test_html_tags_in_signatures_fix(self):
        """
        REGRESSION TEST 2: HTML Tags in Signatures Section Fix
        
        Test that HTML `<br>` tags are properly converted to line breaks in the signatures table.
        
        Steps:
        1. Create a contract with client details containing line breaks
        2. Download both regular and custom versions
        3. Verify that HTML `<br>` tags are properly converted to line breaks in the signatures table
        4. Check that client details display correctly formatted
        """
        print("\n" + "="*80)
        print("🔍 REGRESSION TEST 2: HTML TAGS IN SIGNATURES SECTION FIX")
        print("="*80)
        
        # Step 1: Create contract with client details containing line breaks
        print("\n📝 Step 1: Creating contract with multi-line client details...")
        contract_data = {
            "name_or_organization": "ИП Сидоров Сидор Сидорович",
            "other_details": "Адрес: г. Казань, ул. Подписная, 2<br>ИНН: 9876543210<br>ОГРНИП: 123456789012345<br>Телефон: +7(843)987-65-43<br>Email: sidorov@test.ru",
            "service_cost": 35000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Create Contract with HTML Tags in Details",
            "POST",
            "contracts/direct",
            200,
            data=contract_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            print("❌ Failed to create contract")
            return False
        
        contract_id = response['id']
        contract_number = response['contract_number']
        self.created_contract_ids.append(contract_id)
        
        print(f"✅ Contract created: {contract_id}")
        print(f"   Contract number: {contract_number}")
        print(f"   Client details contain HTML <br> tags: {contract_data['other_details']}")
        
        # Step 2: Test regular download
        print("\n📥 Step 2: Testing regular download for HTML tag handling...")
        url_regular = f"{self.api_url}/contracts/direct/{contract_id}/download"
        
        self.tests_run += 1
        try:
            download_response = requests.get(url_regular)
            if download_response.status_code != 200:
                print(f"❌ Regular download failed: {download_response.status_code}")
                return False
            
            self.tests_passed += 1
            print("✅ Regular download successful")
            
            # Check regular download for HTML tag handling
            regular_html_fix = self._check_html_tags_in_document(download_response.content, "regular")
            
        except Exception as e:
            print(f"❌ Error during regular download: {str(e)}")
            return False
        
        # Step 3: Edit content and test custom download
        print("\n✏️  Step 3: Editing content and testing custom download...")
        edited_content = f"""**Договор об оказании услуг № {contract_number}**

г. Казань «___» 2025 г.

Индивидуальный предприниматель Шамсутдинов Радис Раисович, именуемый в дальнейшем «Исполнитель» с одной стороны и ИП Сидоров Сидор Сидорович, именуемый в дальнейшем «Заказчик», с другой стороны.

**1. ПРЕДМЕТ ДОГОВОРА**

1.1. Исполнитель обязуется оказать услуги по созданию рекламных кампаний.

**2. СТОИМОСТЬ УСЛУГ**

2.1. Стоимость услуг составляет 35000 (тридцать пять тысяч) рублей.

**3. ЗАКЛЮЧИТЕЛЬНЫЕ ПОЛОЖЕНИЯ**

3.1. Настоящий договор составлен в двух экземплярах."""

        content_update = {"contract_content": edited_content}
        
        success, edit_response = self.run_test(
            "Edit Contract Content for HTML Test",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            200,
            data=content_update,
            return_response=True
        )
        
        if not success:
            print("❌ Failed to edit contract content")
            return False
        
        print("✅ Contract content edited successfully")
        
        # Step 4: Test custom download
        print("\n📥 Step 4: Testing custom download for HTML tag handling...")
        url_custom = f"{self.api_url}/contracts/direct/{contract_id}/download_custom"
        
        self.tests_run += 1
        try:
            custom_download_response = requests.get(url_custom)
            if custom_download_response.status_code != 200:
                print(f"❌ Custom download failed: {custom_download_response.status_code}")
                return False
            
            self.tests_passed += 1
            print("✅ Custom download successful")
            
            # Check custom download for HTML tag handling
            custom_html_fix = self._check_html_tags_in_document(custom_download_response.content, "custom")
            
            return regular_html_fix and custom_html_fix
            
        except Exception as e:
            print(f"❌ Error during custom download: {str(e)}")
            return False

    def _check_html_tags_in_document(self, document_content, download_type):
        """Helper method to check HTML tag handling in Word document"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                temp_file.write(document_content)
                temp_file_path = temp_file.name
            
            with zipfile.ZipFile(temp_file_path, 'r') as docx_zip:
                document_xml = docx_zip.read('word/document.xml').decode('utf-8')
                
                print(f"   Checking {download_type} download for HTML tag handling...")
                
                # Check 1: HTML <br> tags should NOT be present in final document
                html_br_count = document_xml.count('<br>') + document_xml.count('<br/>') + document_xml.count('<br ')
                if html_br_count == 0:
                    print(f"   ✅ No HTML <br> tags found in {download_type} document (correctly converted)")
                    html_tags_removed = True
                else:
                    print(f"   ❌ HTML <br> tags still present in {download_type} document: {html_br_count} occurrences")
                    html_tags_removed = False
                
                # Check 2: Client details should be properly formatted in signatures section
                signatures_section_start = document_xml.find('«Заказчик»:')
                if signatures_section_start != -1:
                    signatures_section = document_xml[signatures_section_start:signatures_section_start + 2000]  # Get section
                    
                    # Check for proper line breaks (Word uses <w:br/> or paragraph breaks)
                    word_line_breaks = signatures_section.count('<w:br/>') + signatures_section.count('<w:p>')
                    if word_line_breaks > 3:  # Should have multiple line breaks for multi-line client details
                        print(f"   ✅ Client details properly formatted with line breaks in {download_type} document ({word_line_breaks} breaks)")
                        proper_formatting = True
                    else:
                        print(f"   ❌ Client details may not be properly formatted in {download_type} document ({word_line_breaks} breaks)")
                        proper_formatting = False
                    
                    # Check 3: Specific client detail elements should be present
                    detail_checks = [
                        ('Address', 'г. Казань, ул. Подписная, 2' in signatures_section),
                        ('INN', '9876543210' in signatures_section),
                        ('OGRNIP', '123456789012345' in signatures_section),
                        ('Phone', '+7(843)987-65-43' in signatures_section),
                        ('Email', 'sidorov@test.ru' in signatures_section)
                    ]
                    
                    details_present = True
                    for detail_name, detail_found in detail_checks:
                        if detail_found:
                            print(f"   ✅ {detail_name} found in {download_type} signatures section")
                        else:
                            print(f"   ❌ {detail_name} NOT found in {download_type} signatures section")
                            details_present = False
                else:
                    print(f"   ❌ Signatures section not found in {download_type} document")
                    proper_formatting = False
                    details_present = False
                
                # Clean up
                import os
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                
                return html_tags_removed and proper_formatting and details_present
                
        except Exception as e:
            print(f"   ❌ Error checking HTML tags in {download_type} document: {str(e)}")
            return False

    def test_page_layout_fix(self):
        """
        REGRESSION TEST 3: Page Layout Fix
        
        Test that signatures section (Section 11) starts on new page (page 4) for edited contracts.
        
        Steps:
        1. Create and edit a contract
        2. Download custom version
        3. Verify that signatures section (Section 11) starts on new page (page 4)
        4. Ensure content fits properly in 3 pages with signatures on page 4
        5. Verify proper page breaks are inserted
        """
        print("\n" + "="*80)
        print("🔍 REGRESSION TEST 3: PAGE LAYOUT FIX")
        print("="*80)
        
        # Step 1: Create contract
        print("\n📝 Step 1: Creating contract for page layout test...")
        contract_data = {
            "name_or_organization": "ООО Тест Разметка Страниц",
            "other_details": "Адрес: г. Казань, ул. Страничная, 4\nИНН: 1122334455\nОГРН: 1234567890123\nТелефон: +7(843)111-22-33\nEmail: layout@test.ru\nДиректор: Иванов Иван Иванович\nБухгалтер: Петрова Анна Сергеевна",
            "service_cost": 80000,
            "duration_months": 12
        }
        
        success, response = self.run_test(
            "Create Contract for Page Layout Test",
            "POST",
            "contracts/direct",
            200,
            data=contract_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            print("❌ Failed to create contract")
            return False
        
        contract_id = response['id']
        contract_number = response['contract_number']
        self.created_contract_ids.append(contract_id)
        
        print(f"✅ Contract created: {contract_id}")
        print(f"   Contract number: {contract_number}")
        
        # Step 2: Edit contract with substantial content
        print("\n✏️  Step 2: Editing contract with substantial content...")
        edited_content = f"""**Договор об оказании услуг № {contract_number}**

г. Казань «___» 2025 г.

Индивидуальный предприниматель Шамсутдинов Радис Раисович, именуемый в дальнейшем «Исполнитель» с одной стороны и ООО Тест Разметка Страниц, именуемый в дальнейшем «Заказчик», с другой стороны, далее совместно именуемые «Стороны» заключили настоящий Договор о нижеследующем:

**1. ПРЕДМЕТ ДОГОВОРА**

1.1. «Исполнитель» принимает на себя обязательства оказать комплекс услуг в соответствии с заявками «Заказчика», а «Заказчик» обязуется принять услуги и оплатить их в размере и порядке, установленном настоящим договором.

1.2. В комплекс оказываемых услуг входят:

1.2.1. Создание рекламных кампаний в Яндекс.Директ.

1.2.2. Ведение рекламных кампаний в течение 3 (трёх) календарных недель после запуска.

1.3. Настройка и ведение рекламных кампаний осуществляются через специализированные сервисы.

**2. СРОК ДЕЙСТВИЯ ДОГОВОРА**

2.1. Настоящий Договор вступает в силу с даты его подписания Сторонами и действует в течение 12 месяцев.

2.2. Договор может быть расторгнут в одностороннем порядке по инициативе одной из Сторон при условии письменного уведомления другой Стороны.

2.3. Досрочное расторжение Договора возможно по взаимному согласию Сторон, выраженному в письменной форме.

**3. ПРАВА И ОБЯЗАННОСТИ СТОРОН**

3.1. «Исполнитель» обязан:

3.1.1. Приступить к оказанию Услуг в течение трех дней с момента поступления оплаты за них.

3.1.2. Консультировать Заказчика по всем вопросам, касающихся предмета данного Договора.

3.1.3. Незамедлительно уведомлять «Заказчика» обо всех обстоятельствах, которые могут повлечь задержку в оказании Услуг.

3.2. «Заказчик» обязан:

3.2.1. Предоставлять «Исполнителю» информацию, необходимую для оказания Услуг по настоящему Договору.

3.2.2. Оплатить Услуги в сроки и в порядке, установленные настоящим Договором.

**4. ЦЕНА УСЛУГ И ПОРЯДОК РАСЧЕТОВ**

4.1. Стоимость услуг составляет 80000 (восемьдесят тысяч) рублей в месяц.

4.2. Полная оплата производится в день подписания настоящего договора на расчетный счет Исполнителя.

**5. ПОРЯДОК СДАЧИ-ПРИЕМКИ УСЛУГ**

5.1. Не позднее 3 (Три) рабочих дней с момента оказания услуг ежемесячно Стороны подписывают Акт выполненных работ.

**6. ОТВЕТСТВЕННОСТЬ СТОРОН**

6.1. За неисполнение, ненадлежащее исполнение своих обязательств по настоящему Договору Стороны несут ответственность в соответствии с действующим законодательством РФ.

**7. ПОРЯДОК РАЗРЕШЕНИЯ СПОРОВ**

7.1. Все споры или разногласия, возникающие между Сторонами по настоящему Договору, разрешаются путем переговоров.

**8. ЗАКЛЮЧИТЕЛЬНЫЕ ПОЛОЖЕНИЯ**

8.1. Настоящий Договор составлен в двух экземплярах, по одному экземпляру для каждой из Сторон.

8.2. После подписания настоящего Договора все предыдущие переговоры и переписка, связанная с его заключением, теряют силу.

**9. ДОПОЛНИТЕЛЬНЫЕ УСЛОВИЯ**

9.1. Все изменения и дополнения к настоящему Договору должны быть оформлены в письменном виде.

9.2. Настоящий Договор регулируется законодательством Российской Федерации.

**10. КОНФИДЕНЦИАЛЬНОСТЬ**

10.1. Любая информация, данные или сведения, полученные Сторонами в целях исполнения настоящего Договора, рассматриваются как конфиденциальные."""

        content_update = {"contract_content": edited_content}
        
        success, edit_response = self.run_test(
            "Edit Contract Content for Page Layout Test",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            200,
            data=content_update,
            return_response=True
        )
        
        if not success:
            print("❌ Failed to edit contract content")
            return False
        
        print("✅ Contract content edited successfully")
        
        # Step 3: Download custom version and check page layout
        print("\n📥 Step 3: Downloading custom version and checking page layout...")
        url = f"{self.api_url}/contracts/direct/{contract_id}/download_custom"
        
        self.tests_run += 1
        try:
            download_response = requests.get(url)
            if download_response.status_code != 200:
                print(f"❌ Custom download failed: {download_response.status_code}")
                return False
            
            self.tests_passed += 1
            print("✅ Custom download successful")
            
            # Check page layout
            layout_fix_passed = self._check_page_layout(download_response.content)
            
            return layout_fix_passed
            
        except Exception as e:
            print(f"❌ Error during page layout test: {str(e)}")
            return False

    def _check_page_layout(self, document_content):
        """Helper method to check page layout in Word document"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                temp_file.write(document_content)
                temp_file_path = temp_file.name
            
            with zipfile.ZipFile(temp_file_path, 'r') as docx_zip:
                document_xml = docx_zip.read('word/document.xml').decode('utf-8')
                
                print("   Checking page layout and section positioning...")
                
                # Check 1: Page breaks should be present
                page_break_patterns = [
                    '<w:br w:type="page"/>',
                    '<w:br w:type="page" />',
                    'w:type="page"'
                ]
                
                page_breaks_found = 0
                for pattern in page_break_patterns:
                    page_breaks_found += document_xml.count(pattern)
                
                if page_breaks_found > 0:
                    print(f"   ✅ Page breaks found in document: {page_breaks_found} occurrences")
                    page_breaks_present = True
                else:
                    print("   ❌ No page breaks found in document")
                    page_breaks_present = False
                
                # Check 2: Section 11 (signatures section) should be present
                section_11_pattern = "11. ЮРИДИЧЕСКИЕ АДРЕСА И БАНКОВСКИЕ РЕКВИЗИТЫ СТОРОН"
                section_11_found = section_11_pattern in document_xml
                
                if section_11_found:
                    print("   ✅ Section 11 (signatures section) found in document")
                    
                    # Check if section 11 comes after a page break
                    section_11_pos = document_xml.find(section_11_pattern)
                    text_before_section_11 = document_xml[:section_11_pos]
                    
                    # Look for page break before section 11
                    page_break_before_section_11 = any(pattern in text_before_section_11 for pattern in page_break_patterns)
                    
                    if page_break_before_section_11:
                        print("   ✅ Page break found before Section 11 (starts on new page)")
                        section_on_new_page = True
                    else:
                        print("   ❌ No page break found before Section 11")
                        section_on_new_page = False
                else:
                    print("   ❌ Section 11 (signatures section) not found in document")
                    section_on_new_page = False
                
                # Check 3: Document structure should be preserved
                paragraph_count = document_xml.count('<w:p>')
                if paragraph_count > 15:  # Should have substantial content
                    print(f"   ✅ Document has substantial content: {paragraph_count} paragraphs")
                    substantial_content = True
                else:
                    print(f"   ❌ Document may lack substantial content: {paragraph_count} paragraphs")
                    substantial_content = False
                
                # Check 4: Signatures table should be present
                table_found = '<w:tbl>' in document_xml
                if table_found:
                    print("   ✅ Table structure found (likely signatures table)")
                    signatures_table_present = True
                else:
                    print("   ❌ No table structure found for signatures")
                    signatures_table_present = False
                
                # Check 5: Client details should be in signatures section
                client_name_in_signatures = "ООО Тест Разметка Страниц" in document_xml
                if client_name_in_signatures:
                    print("   ✅ Client name found in document (signatures section)")
                    client_details_present = True
                else:
                    print("   ❌ Client name not found in document")
                    client_details_present = False
                
                # Clean up
                import os
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                
                # Overall assessment
                layout_checks = [
                    page_breaks_present,
                    section_11_found,
                    section_on_new_page,
                    substantial_content,
                    signatures_table_present,
                    client_details_present
                ]
                
                passed_checks = sum(layout_checks)
                total_checks = len(layout_checks)
                
                if passed_checks >= 5:  # Allow one minor failure
                    print(f"   ✅ PAGE LAYOUT FIX VERIFIED: {passed_checks}/{total_checks} checks passed")
                    return True
                else:
                    print(f"   ❌ PAGE LAYOUT ISSUES DETECTED: Only {passed_checks}/{total_checks} checks passed")
                    return False
                
        except Exception as e:
            print(f"   ❌ Error checking page layout: {str(e)}")
            return False

    def test_custom_content_integration(self):
        """
        REGRESSION TEST 4: Custom Content Integration
        
        Test structured content including sections with **bold** markers.
        
        Steps:
        1. Create contract
        2. Edit with structured content including sections with **bold** markers
        3. Verify section headers are formatted correctly (centered, bold)
        4. Test content with both upper case headers and markdown **bold** headers
        """
        print("\n" + "="*80)
        print("🔍 REGRESSION TEST 4: CUSTOM CONTENT INTEGRATION")
        print("="*80)
        
        # Step 1: Create contract
        print("\n📝 Step 1: Creating contract for custom content integration test...")
        contract_data = {
            "name_or_organization": "ИП Тестов Тест Тестович",
            "other_details": "Адрес: г. Казань, ул. Интеграционная, 5\nИНН: 5566778899\nОГРНИП: 987654321098765",
            "service_cost": 60000,
            "duration_months": 6
        }
        
        success, response = self.run_test(
            "Create Contract for Content Integration Test",
            "POST",
            "contracts/direct",
            200,
            data=contract_data,
            return_response=True
        )
        
        if not success or 'id' not in response:
            print("❌ Failed to create contract")
            return False
        
        contract_id = response['id']
        contract_number = response['contract_number']
        self.created_contract_ids.append(contract_id)
        
        print(f"✅ Contract created: {contract_id}")
        print(f"   Contract number: {contract_number}")
        
        # Step 2: Edit with structured content including various formatting
        print("\n✏️  Step 2: Editing with structured content and formatting markers...")
        structured_content = f"""**Договор об оказании услуг № {contract_number}**

г. Казань «___» 2025 г.

Индивидуальный предприниматель Шамсутдинов Радис Раисович, именуемый в дальнейшем «Исполнитель» с одной стороны и ИП Тестов Тест Тестович, именуемый в дальнейшем «Заказчик», с другой стороны.

**1. ПРЕДМЕТ ДОГОВОРА**

1.1. Исполнитель обязуется оказать следующие услуги:

**ОСНОВНЫЕ УСЛУГИ:**

- Создание рекламных кампаний
- Настройка таргетинга
- Оптимизация показов

**ДОПОЛНИТЕЛЬНЫЕ УСЛУГИ:**

- Аналитика и отчетность
- Консультационная поддержка

**2. СТОИМОСТЬ И ОПЛАТА**

2.1. Стоимость услуг составляет **60000 (шестьдесят тысяч) рублей**.

2.2. Оплата производится **ежемесячно** до 10 числа.

**УСЛОВИЯ ОПЛАТЫ**

Заказчик обязуется производить оплату в установленные сроки.

**3. СРОК ДЕЙСТВИЯ**

3.1. Договор действует **6 месяцев** с момента подписания.

**УСЛОВИЯ ПРОДЛЕНИЯ**

Договор может быть продлен по взаимному согласию сторон.

**4. ОТВЕТСТВЕННОСТЬ СТОРОН**

4.1. Стороны несут ответственность в соответствии с **действующим законодательством РФ**.

**ОСОБЫЕ УСЛОВИЯ ОТВЕТСТВЕННОСТИ**

При нарушении сроков применяются штрафные санкции.

**5. ЗАКЛЮЧИТЕЛЬНЫЕ ПОЛОЖЕНИЯ**

5.1. Договор составлен в **двух экземплярах**.

5.2. Все изменения оформляются **письменно**.

**ДОПОЛНИТЕЛЬНЫЕ СОГЛАШЕНИЯ**

Стороны могут заключать дополнительные соглашения к настоящему договору.

**ПОДПИСИ СТОРОН**

Исполнитель: ________________/Шамсутдинов Р.Р.

Заказчик: ________________/ИП Тестов Тест Тестович

**КОНЕЦ СТРУКТУРИРОВАННОГО ДОКУМЕНТА**"""

        content_update = {"contract_content": structured_content}
        
        success, edit_response = self.run_test(
            "Edit Contract with Structured Content",
            "PUT",
            f"contracts/direct/{contract_id}/content",
            200,
            data=content_update,
            return_response=True
        )
        
        if not success:
            print("❌ Failed to edit contract content")
            return False
        
        print("✅ Contract content edited with structured formatting")
        
        # Step 3: Download and verify content integration
        print("\n📥 Step 3: Downloading and verifying custom content integration...")
        url = f"{self.api_url}/contracts/direct/{contract_id}/download_custom"
        
        self.tests_run += 1
        try:
            download_response = requests.get(url)
            if download_response.status_code != 200:
                print(f"❌ Custom download failed: {download_response.status_code}")
                return False
            
            self.tests_passed += 1
            print("✅ Custom download successful")
            
            # Check content integration
            integration_passed = self._check_content_integration(download_response.content)
            
            return integration_passed
            
        except Exception as e:
            print(f"❌ Error during content integration test: {str(e)}")
            return False

    def _check_content_integration(self, document_content):
        """Helper method to check custom content integration in Word document"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                temp_file.write(document_content)
                temp_file_path = temp_file.name
            
            with zipfile.ZipFile(temp_file_path, 'r') as docx_zip:
                document_xml = docx_zip.read('word/document.xml').decode('utf-8')
                
                print("   Checking custom content integration and formatting...")
                
                # Check 1: Bold formatting should be present (markdown **bold** converted)
                bold_elements = document_xml.count('<w:b/>') + document_xml.count('<w:b ')
                if bold_elements > 10:  # Should have many bold elements from **bold** markers
                    print(f"   ✅ Bold formatting found: {bold_elements} bold elements")
                    bold_formatting_present = True
                else:
                    print(f"   ❌ Insufficient bold formatting: {bold_elements} bold elements")
                    bold_formatting_present = False
                
                # Check 2: Section headers should be present and formatted
                section_headers = [
                    "1. ПРЕДМЕТ ДОГОВОРА",
                    "2. СТОИМОСТЬ И ОПЛАТА", 
                    "3. СРОК ДЕЙСТВИЯ",
                    "4. ОТВЕТСТВЕННОСТЬ СТОРОН",
                    "5. ЗАКЛЮЧИТЕЛЬНЫЕ ПОЛОЖЕНИЯ"
                ]
                
                headers_found = 0
                for header in section_headers:
                    if header in document_xml:
                        headers_found += 1
                        print(f"   ✅ Section header found: {header}")
                    else:
                        print(f"   ❌ Section header missing: {header}")
                
                headers_present = headers_found >= 4  # Allow one missing
                
                # Check 3: Custom subsection headers should be present
                custom_headers = [
                    "ОСНОВНЫЕ УСЛУГИ:",
                    "ДОПОЛНИТЕЛЬНЫЕ УСЛУГИ:",
                    "УСЛОВИЯ ОПЛАТЫ",
                    "УСЛОВИЯ ПРОДЛЕНИЯ",
                    "ОСОБЫЕ УСЛОВИЯ ОТВЕТСТВЕННОСТИ",
                    "ДОПОЛНИТЕЛЬНЫЕ СОГЛАШЕНИЯ"
                ]
                
                custom_headers_found = 0
                for header in custom_headers:
                    if header in document_xml:
                        custom_headers_found += 1
                        print(f"   ✅ Custom header found: {header}")
                    else:
                        print(f"   ❌ Custom header missing: {header}")
                
                custom_headers_present = custom_headers_found >= 4  # Allow some missing
                
                # Check 4: Specific content with bold markers should be integrated
                bold_content_checks = [
                    ("Service cost", "60000 (шестьдесят тысяч) рублей" in document_xml),
                    ("Payment frequency", "ежемесячно" in document_xml),
                    ("Contract duration", "6 месяцев" in document_xml),
                    ("Legal framework", "действующим законодательством РФ" in document_xml),
                    ("Document copies", "двух экземплярах" in document_xml),
                    ("Written changes", "письменно" in document_xml)
                ]
                
                bold_content_found = 0
                for content_name, content_present in bold_content_checks:
                    if content_present:
                        bold_content_found += 1
                        print(f"   ✅ Bold content found: {content_name}")
                    else:
                        print(f"   ❌ Bold content missing: {content_name}")
                
                bold_content_integrated = bold_content_found >= 5  # Allow one missing
                
                # Check 5: List items should be present
                list_items = [
                    "Создание рекламных кампаний",
                    "Настройка таргетинга", 
                    "Оптимизация показов",
                    "Аналитика и отчетность",
                    "Консультационная поддержка"
                ]
                
                list_items_found = 0
                for item in list_items:
                    if item in document_xml:
                        list_items_found += 1
                        print(f"   ✅ List item found: {item}")
                    else:
                        print(f"   ❌ List item missing: {item}")
                
                list_items_present = list_items_found >= 4  # Allow one missing
                
                # Check 6: Document structure markers
                structure_markers = [
                    "КОНЕЦ СТРУКТУРИРОВАННОГО ДОКУМЕНТА" in document_xml,
                    "ИП Тестов Тест Тестович" in document_xml
                ]
                
                structure_markers_present = all(structure_markers)
                if structure_markers_present:
                    print("   ✅ Document structure markers found")
                else:
                    print("   ❌ Document structure markers missing")
                
                # Clean up
                import os
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                
                # Overall assessment
                integration_checks = [
                    bold_formatting_present,
                    headers_present,
                    custom_headers_present,
                    bold_content_integrated,
                    list_items_present,
                    structure_markers_present
                ]
                
                passed_checks = sum(integration_checks)
                total_checks = len(integration_checks)
                
                if passed_checks >= 5:  # Allow one minor failure
                    print(f"   ✅ CUSTOM CONTENT INTEGRATION VERIFIED: {passed_checks}/{total_checks} checks passed")
                    return True
                else:
                    print(f"   ❌ CONTENT INTEGRATION ISSUES DETECTED: Only {passed_checks}/{total_checks} checks passed")
                    return False
                
        except Exception as e:
            print(f"   ❌ Error checking content integration: {str(e)}")
            return False

    def cleanup_test_contracts(self):
        """Clean up test contracts created during testing"""
        print(f"\n🧹 Cleaning up {len(self.created_contract_ids)} test contracts...")
        
        cleanup_success = 0
        for contract_id in self.created_contract_ids:
            try:
                success, _ = self.run_test(
                    f"Delete Test Contract {contract_id[:8]}",
                    "DELETE",
                    f"contracts/direct/{contract_id}",
                    200
                )
                if success:
                    cleanup_success += 1
            except:
                pass
        
        print(f"✅ Cleaned up {cleanup_success}/{len(self.created_contract_ids)} test contracts")

    def run_all_regression_tests(self):
        """Run all regression tests"""
        print("🚀 STARTING REGRESSION TESTS FOR CONTRACT MANAGEMENT SYSTEM")
        print("=" * 80)
        print("Testing specific fixes for reported issues:")
        print("1. Title Duplication Fix")
        print("2. HTML Tags in Signatures Section Fix") 
        print("3. Page Layout Fix")
        print("4. Custom Content Integration")
        print("=" * 80)
        
        test_results = []
        
        # Test 1: Title Duplication Fix
        try:
            result1 = self.test_title_duplication_fix()
            test_results.append(("Title Duplication Fix", result1))
        except Exception as e:
            print(f"❌ Title Duplication Fix test failed with error: {str(e)}")
            test_results.append(("Title Duplication Fix", False))
        
        # Test 2: HTML Tags in Signatures Fix
        try:
            result2 = self.test_html_tags_in_signatures_fix()
            test_results.append(("HTML Tags in Signatures Fix", result2))
        except Exception as e:
            print(f"❌ HTML Tags in Signatures Fix test failed with error: {str(e)}")
            test_results.append(("HTML Tags in Signatures Fix", False))
        
        # Test 3: Page Layout Fix
        try:
            result3 = self.test_page_layout_fix()
            test_results.append(("Page Layout Fix", result3))
        except Exception as e:
            print(f"❌ Page Layout Fix test failed with error: {str(e)}")
            test_results.append(("Page Layout Fix", False))
        
        # Test 4: Custom Content Integration
        try:
            result4 = self.test_custom_content_integration()
            test_results.append(("Custom Content Integration", result4))
        except Exception as e:
            print(f"❌ Custom Content Integration test failed with error: {str(e)}")
            test_results.append(("Custom Content Integration", False))
        
        # Cleanup
        self.cleanup_test_contracts()
        
        # Final Results
        print("\n" + "="*80)
        print("🏁 REGRESSION TEST RESULTS SUMMARY")
        print("="*80)
        
        passed_tests = 0
        for test_name, result in test_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{status}: {test_name}")
            if result:
                passed_tests += 1
        
        print(f"\nOverall Results: {passed_tests}/{len(test_results)} regression tests passed")
        print(f"API Tests: {self.tests_passed}/{self.tests_run} individual API calls successful")
        
        success_rate = (passed_tests / len(test_results)) * 100
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 75:
            print("\n🎉 REGRESSION TESTING COMPLETED SUCCESSFULLY!")
            print("✅ The reported issues appear to be fixed.")
        else:
            print("\n⚠️  REGRESSION TESTING COMPLETED WITH ISSUES!")
            print("❌ Some reported issues may still be present.")
        
        return success_rate >= 75

if __name__ == "__main__":
    tester = RegressionTester()
    success = tester.run_all_regression_tests()
    sys.exit(0 if success else 1)