import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from fetch_otp import get_latest_otp

# Get configuration from environment variables (for cloud deployment)
# Fall back to hardcoded values for local development
SYSTEM_ID = os.getenv('SYSTEM_ID', "2023497222")
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', "7688760570:AAFxql5tfEBIkBvwche2Zj_74zRUuVlS7rY")
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', "6244107851")

def send_telegram_message(message):
    """Send a message via Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

# Set up Selenium WebDriver for cloud deployment
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run in headless mode for cloud
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')

# Try to use Chrome, fall back to Chromium
try:
    driver = webdriver.Chrome(options=chrome_options)
except:
    try:
        # For systems with chromium-browser
        chrome_options.binary_location = '/usr/bin/chromium-browser'
        driver = webdriver.Chrome(options=chrome_options)
    except:
        # Last resort - try without options
        driver = webdriver.Chrome()

try:
    driver.get("https://student.sharda.ac.in/admin")
    print("🔗 Opened Sharda E-Zone login page.")

    # Enter System ID
    system_id_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "system_id"))
    )
    system_id_field.send_keys(SYSTEM_ID)
    print("✅ Entered System ID.")

    # Click OTP Request Button
    otp_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "send_stu_otp_email"))
    )
    otp_button.click()
    print("✅ Clicked OTP request button.")

    # Fetch OTP
    print("⏳ Waiting for OTP...")
    time.sleep(5)  # Allow time for OTP to arrive
    otp = get_latest_otp()

    if not otp:
        print("❌ Failed to retrieve OTP.")
        driver.quit()
        exit()

    # Enter OTP
    otp_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "otp"))
    )
    otp_field.send_keys(otp)
    print(f"🔢 Entered OTP: {otp}")

    # Click Login Button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "stu-login"))
    )
    login_button.click()
    print("✅ Logged in successfully.")

    # Navigate to Attendance Page
    driver.get("https://student.sharda.ac.in/admin/courses")
    print("🔄 Navigating to attendance page...")
    
    # Wait for the page to load completely
    time.sleep(5)
    
    # Take a screenshot for debugging
    driver.save_screenshot('attendance_page.png')
    print("📸 Took a screenshot of the attendance page for debugging")
    
    # Save page source for inspection
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("💾 Saved page source to 'page_source.html'")
    
    # Debug: Print all tables on the page
    print("\n🔍 Looking for tables on the page...")
    tables = driver.find_elements(By.TAG_NAME, 'table')
    print(f"Found {len(tables)} table(s) on the page")
    
    # Print all elements with class names containing 'table'
    print("\n🔍 Elements with 'table' in class name:")
    table_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='table']")
    for i, elem in enumerate(table_elements, 1):
        print(f"  {i}. Tag: {elem.tag_name}, ID: {elem.get_attribute('id')}, Classes: {elem.get_attribute('class')}")
    
    # Print all div elements that might contain the attendance data
    print("\n🔍 Looking for potential containers with attendance data...")
    potential_containers = driver.find_elements(By.CSS_SELECTOR, "div.card, div.panel, div.tab-content, div.content-wrapper")
    for i, container in enumerate(potential_containers, 1):
        print(f"\n  Container {i}:")
        print(f"  - ID: {container.get_attribute('id')}")
        print(f"  - Classes: {container.get_attribute('class')}")
        print(f"  - Text preview: {container.text[:100]}...")
    
    # Try to find the attendance table - the ID might have changed
    try:
        # First try with common table selectors
        table_selectors = [
            (By.CSS_SELECTOR, "table.table"),
            (By.CSS_SELECTOR, "table#table1"),
            (By.CSS_SELECTOR, "table[class*='attendance']"),
            (By.CSS_SELECTOR, "table.dataTable"),
            (By.CSS_SELECTOR, "table.datatable"),
            (By.TAG_NAME, "table")
        ]
        
        attendance_table = None
        for selector in table_selectors:
            try:
                attendance_table = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(selector)
                )
                print(f"\n✅ Found table using selector: {selector}")
                print(f"   - Table ID: {attendance_table.get_attribute('id')}")
                print(f"   - Table classes: {attendance_table.get_attribute('class')}")
                print(f"   - Rows found: {len(attendance_table.find_elements(By.TAG_NAME, 'tr'))}")
                break
            except Exception as e:
                print(f"  ❌ Table not found with selector {selector}")
                continue
                
        if not attendance_table:
            # Try to find any element that might contain attendance data
            print("\n🔍 Trying to find attendance data in other elements...")
            potential_elements = driver.find_elements(By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'attendance')]")
            if potential_elements:
                print(f"Found {len(potential_elements)} elements containing 'attendance' in text")
                for i, elem in enumerate(potential_elements[:5], 1):  # Show first 5
                    print(f"  {i}. Tag: {elem.tag_name}, ID: {elem.get_attribute('id')}, Text: {elem.text[:100]}...")
            
            raise Exception("Could not find attendance table on the page. Check the saved page_source.html for more details.")
            
        # Get all rows in the table body
        rows = attendance_table.find_elements(By.CSS_SELECTOR, "tbody tr")
        if not rows:
            # If no rows in tbody, try getting all rows directly
            rows = attendance_table.find_elements(By.TAG_NAME, "tr")
            
        print(f"📊 Found {len(rows)} rows in attendance table")
        
        attendance_data = []
        for row in rows:
            try:
                # Get all cells in the row
                cols = row.find_elements(By.TAG_NAME, "td")
                if not cols:
                    continue
                    
                # Print column data for debugging
                col_texts = [col.text.strip() for col in cols]
                print("📋 Row data:", col_texts)
                
                # Try to extract course info and percentage
                # The exact indices might need adjustment based on the actual structure
                if len(cols) >= 3:  # At least 3 columns expected: course code, name, percentage
                    # Try to find percentage (look for a cell containing '%')
                    percentage = "N/A"
                    course_code = cols[0].text.strip() if len(cols) > 0 else "Unknown"
                    course_name = cols[1].text.strip() if len(cols) > 1 else "Unknown"
                    
                    # Find the column with percentage
                    for i, col in enumerate(cols):
                        if '%' in col.text:
                            percentage = col.text.strip()
                            break
                    
                    attendance_data.append(f"{course_name} ({course_code}): {percentage}")
                    
            except Exception as e:
                print(f"⚠️ Error processing row: {str(e)}")
                continue
                
        if not attendance_data:
            raise Exception("No attendance data found in the table")
            
    except Exception as e:
        error_msg = f"❌ Error extracting attendance data: {str(e)}"
        print(error_msg)
        # Send the error message via Telegram
        send_telegram_message(error_msg)
        # Re-raise the exception to be caught by the outer try-except
        raise

    # Format the message
    attendance_message = "📊 *Attendance Report*\n\n" + "\n".join(attendance_data)

    # Send via Telegram
    send_telegram_message(attendance_message)
    print("📩 Sent attendance report to Telegram!")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    driver.quit()
    print("🚪 Browser closed.")
