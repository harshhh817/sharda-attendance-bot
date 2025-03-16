from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from fetch_otp import get_latest_otp

# Constants
SYSTEM_ID = "2023497222"
TELEGRAM_BOT_TOKEN = "7688760570:AAFxql5tfEBIkBvwche2Zj_74zRUuVlS7rY"  # Replace with your Telegram Bot Token
TELEGRAM_CHAT_ID = "6244107851"  # Replace with your Telegram Chat ID

def send_telegram_message(message):
    """Send a message via Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

# Set up Selenium WebDriver
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
    time.sleep(7)  # Allow page to load

    # Extract Attendance Data
    attendance_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "table1"))
    )
    rows = attendance_table.find_elements(By.TAG_NAME, "tr")

    attendance_data = []
    for row in rows[1:]:  # Skip the header row
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 9:  # Ensure there's a 9th column for percentage
            course_name = cols[0].text.strip()
            course_code = cols[1].text.strip()
            percentage = cols[8].text.strip()  # Get percentage from the 9th column

            if not percentage:
                percentage = "N/A"

            attendance_data.append(f"{course_name} ({course_code}): {percentage}%")

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
