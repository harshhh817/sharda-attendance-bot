from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from datetime import date
from fetch_otp import get_latest_otp

# Constants (kept consistent with autologin.py)
SYSTEM_ID = "2023497222"
TELEGRAM_BOT_TOKEN = "7688760570:AAFxql5tfEBIkBvwche2Zj_74zRUuVlS7rY"
TELEGRAM_CHAT_ID = "6244107851"


def send_telegram_message(message: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)


def send_telegram_photo(photo_path, caption=None) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    data = {"chat_id": TELEGRAM_CHAT_ID}
    if caption:
        data["caption"] = caption
    with open(photo_path, "rb") as f:
        files = {"photo": f}
        requests.post(url, data=data, files=files)


driver = webdriver.Chrome()
driver.set_window_size(1600, 2400)

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
    time.sleep(5)
    otp = get_latest_otp()

    if not otp:
        print("❌ Failed to retrieve OTP.")
        driver.quit()
        raise SystemExit(1)

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

    # Navigate to Home Page
    driver.get("https://student.sharda.ac.in/admin/home")
    print("🔄 Navigating to home page...")
    time.sleep(3)

    # Dismiss any modals that might block the view
    try:
        driver.execute_script(
            "document.querySelectorAll('.modal, .modal-backdrop').forEach(e => e.remove());"
        )
        print("✅ Dismissed blocking modals.")
    except Exception:
        pass

    # Wait for the "Today's Class" section to load
    try:
        today_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.todayclass"))
        )
        print("✅ Found Today's Class section.")
    except Exception:
        # Try alternative selectors
        try:
            today_section = driver.find_element(By.XPATH, "//h4[contains(text(), 'Today')]/following-sibling::ul")
            print("✅ Found Today's Class section via XPath.")
        except Exception:
            raise Exception("Could not find Today's Class section on the home page.")

    # Wait a bit more for AJAX content to load
    time.sleep(2)

    # Take screenshot of the Today's Class section
    try:
        today_section.screenshot('today_classes.png')
        send_telegram_photo('today_classes.png', caption="📅 Today's Classes")
        print("📸 Sent screenshot of Today's Class section.")
    except Exception as e:
        print(f"⚠️ Could not take section screenshot: {e}")
        try:
            driver.save_screenshot('home_page.png')
            send_telegram_photo('home_page.png', caption="📅 Home Page (Today's Classes)")
            print("📸 Sent full page screenshot as fallback.")
        except Exception:
            pass

    # Extract class information
    class_items = today_section.find_elements(By.TAG_NAME, "li")
    print(f"📊 Found {len(class_items)} class items")

    events = []
    for item in class_items:
        try:
            # Extract time
            time_element = item.find_element(By.TAG_NAME, "h4")
            time_text = time_element.text.strip()
            
            # Extract course name
            course_element = item.find_element(By.TAG_NAME, "p")
            course_text = course_element.text.strip()
            
            # Extract room (badge-primary)
            try:
                room_element = item.find_element(By.CSS_SELECTOR, ".badge-primary")
                room_text = room_element.text.strip()
            except Exception:
                room_text = None
            
            # Extract faculty (badge-danger)
            try:
                faculty_element = item.find_element(By.CSS_SELECTOR, ".badge-danger")
                faculty_text = faculty_element.text.strip()
            except Exception:
                faculty_text = None

            # Clean up time format (HH:MM:SS - HH:MM:SS → HH:MM–HH:MM)
            start_time, end_time = None, None
            if " - " in time_text:
                time_parts = time_text.split(" - ")
                if len(time_parts) == 2:
                    start_raw, end_raw = time_parts[0].strip(), time_parts[1].strip()
                    # Remove seconds
                    start_time = ":".join(start_raw.split(":")[:2]) if ":" in start_raw else start_raw
                    end_time = ":".join(end_raw.split(":")[:2]) if ":" in end_raw else end_raw

            events.append({
                "time": f"{start_time}–{end_time}" if start_time and end_time else time_text,
                "course": course_text,
                "room": room_text,
                "faculty": faculty_text
            })
            
        except Exception as e:
            print(f"⚠️ Error parsing class item: {e}")
            continue

    # Format and send the message
    if events:
        today_str = date.today().strftime('%A, %d %B %Y')
        message_lines = [f"📅 Today's Classes ({today_str})\n"]
        
        for i, event in enumerate(events, 1):
            line_parts = [f"{i}. {event['time']}"]
            line_parts.append(event['course'])
            if event['room']:
                line_parts.append(f"📍 {event['room']}")
            if event['faculty']:
                line_parts.append(f"👨‍🏫 {event['faculty']}")
            
            message_lines.append(" | ".join(line_parts))
        
        message = "\n".join(message_lines)
        send_telegram_message(message)
        print("📩 Sent Today's Classes text message.")
    else:
        today_str = date.today().strftime('%A, %d %B %Y')
        message = f"📅 Today's Classes ({today_str})\n\nNo classes scheduled for today! 🎉"
        send_telegram_message(message)
        print("📩 Sent 'no classes' message.")

    print("✅ Successfully fetched and sent Today's Classes!")

except Exception as e:
    error_msg = f"❌ Error fetching Today's Classes: {str(e)}"
    print(error_msg)
    try:
        send_telegram_message(error_msg)
    except Exception:
        pass
    raise
finally:
    driver.quit()
    print("�� Browser closed.")
