from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import re
from datetime import datetime
from fetch_otp import get_latest_otp

import os

# Get configuration from environment variables (for cloud deployment)
# Fall back to hardcoded values for local development
SYSTEM_ID = os.getenv('SYSTEM_ID', "2023497222")
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', "7688760570:AAFxql5tfEBIkBvwche2Zj_74zRUuVlS7rY")
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', "6244107851")


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


def try_find_any_table(driver: webdriver.Chrome):
    table_selectors = [
        (By.CSS_SELECTOR, "table.table"),
        (By.CSS_SELECTOR, "table#table1"),
        (By.CSS_SELECTOR, "table[class*='timetable']"),
        (By.CSS_SELECTOR, "table.dataTable"),
        (By.CSS_SELECTOR, "table.datatable"),
        (By.TAG_NAME, "table"),
    ]
    for selector in table_selectors:
        try:
            table = WebDriverWait(driver, 3).until(EC.presence_of_element_located(selector))
            return table
        except Exception:
            continue
    return None


# Set up Selenium WebDriver for cloud deployment
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run in headless mode for cloud
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1600,2400')

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

    # Navigate to Timetable Page
    driver.get("https://student.sharda.ac.in/admin/timetable")
    print("🔄 Navigating to timetable page...")
    time.sleep(5)

    # Save artifacts for debugging
    try:
        driver.save_screenshot('timetable_page.png')
        with open('timetable_page.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("📸 Saved timetable screenshot and HTML.")
    except Exception:
        pass

    # Locate timetable table
    timetable_table = try_find_any_table(driver)
    if not timetable_table:
        # Fallback path: use dashboard 'Today's Class' list populated by AJAX
        print("❗ Timetable table not found, trying dashboard today's classes fallback...")
        driver.get("https://student.sharda.ac.in/admin/home")
        time.sleep(2)
        # Dismiss any blocking modals/backdrops if present
        try:
            driver.execute_script(
                "document.querySelectorAll('.modal, .modal-backdrop').forEach(e => e.remove());"
            )
        except Exception:
            pass
        try:
            today_ul = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.todayclass"))
            )
            # Wait briefly for AJAX to populate
            time.sleep(1.0)
            items = today_ul.find_elements(By.TAG_NAME, "li")
            events = []
            for it in items:
                try:
                    t = it.find_element(By.TAG_NAME, "h4").text.strip()
                except Exception:
                    t = ""
                try:
                    title = it.find_element(By.TAG_NAME, "p").text.strip()
                except Exception:
                    title = ""
                try:
                    room = it.find_element(By.CSS_SELECTOR, ".badge-primary").text.strip()
                except Exception:
                    room = None
                try:
                    faculty = it.find_element(By.CSS_SELECTOR, ".badge-danger").text.strip()
                except Exception:
                    faculty = None

                # Clean up time like HH:MM:SS - HH:MM:SS → HH:MM–HH:MM
                start_raw, end_raw = None, None
                if "-" in t:
                    parts = [p.strip() for p in t.split("-")]
                    if len(parts) == 2:
                        start_raw, end_raw = parts
                def drop_seconds(s):
                    c = s.split(":")
                    return ":".join(c[:2]) if len(c) >= 2 else s
                start_t = drop_seconds(start_raw) if start_raw else None
                end_t = drop_seconds(end_raw) if end_raw else None

                events.append({
                    "start": start_t,
                    "end": end_t,
                    "title": title,
                    "room": room,
                    "faculty": faculty,
                })

            # Send screenshot of the section
            try:
                today_ul.screenshot('timetable_today.png')
                send_telegram_photo('timetable_today.png', caption="📅 Today's Classes")
            except Exception:
                try:
                    driver.save_screenshot('timetable_page.png')
                    send_telegram_photo('timetable_page.png', caption="📅 Today's Classes")
                except Exception:
                    pass

            # Format and send text summary
            if events:
                from datetime import date
                message_lines = []
                for e in events:
                    time_seg = f"{e['start']}–{e['end']}" if e['start'] and e['end'] else (e['start'] or "")
                    parts = []
                    if time_seg:
                        parts.append(time_seg)
                    if e['title']:
                        parts.append(e['title'])
                    if e['room']:
                        parts.append(f"({e['room']})")
                    if e['faculty']:
                        parts.append(f"— {e['faculty']}")
                    line = " ".join(parts).strip()
                    if line:
                        message_lines.append("- " + line)
                today_str = date.today().strftime('%a, %d %b %Y')
                message = f"📅 Today's Classes ({today_str})\n\n" + ("\n".join(message_lines) if message_lines else "No classes found.")
                send_telegram_message(message)
                print("📩 Sent today's classes from dashboard.")
                # End success path
                print("📩 Sent timetable to Telegram!")
                return
            else:
                raise Exception("No classes found in today's classes list")
        except Exception as e2:
            # As a last resort, report the original issue
            raise Exception("Could not find timetable table or today's classes on dashboard.") from e2

    # Try to send a screenshot of the timetable table (fallback to full page)
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", timetable_table)
        time.sleep(0.3)
        timetable_table.screenshot('timetable_table.png')
        send_telegram_photo('timetable_table.png', caption='📅 Timetable (table view)')
    except Exception:
        try:
            driver.save_screenshot('timetable_page.png')
            send_telegram_photo('timetable_page.png', caption='📅 Timetable (page view)')
        except Exception:
            pass

    # Heuristic parsing to extract Day/Time/Course/Room/Faculty from a grid-like timetable
    def normalize_header(text: str) -> str:
        return re.sub(r"\s+", " ", (text or "").strip()).lower()

    weekday_names = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    # Collect headers from thead or header row
    header_cells = timetable_table.find_elements(By.CSS_SELECTOR, "thead th")
    if not header_cells:
        # Fallback: first row in tbody may contain headers
        first_row_th = timetable_table.find_elements(By.CSS_SELECTOR, "tbody tr th")
        header_cells = first_row_th

    headers = [c.text.strip() for c in header_cells if c.text and c.text.strip()]
    normalized_headers = [normalize_header(h) for h in headers]

    # Identify day columns and (optional) time column
    day_col_indices = {}
    time_col_index = None
    for idx, h in enumerate(normalized_headers):
        if any(day in h for day in weekday_names):
            # Map exact day name to column index
            for day in weekday_names:
                if day in h:
                    day_col_indices[day] = idx
        if any(token in h for token in ["time", "period", "slot"]):
            time_col_index = idx

    # Fetch body rows
    body_rows = timetable_table.find_elements(By.CSS_SELECTOR, "tbody tr")
    if not body_rows:
        body_rows = timetable_table.find_elements(By.TAG_NAME, "tr")

    print(f"📊 Found {len(body_rows)} rows in timetable table")

    time_pattern = re.compile(r"(\d{1,2}:\d{2})\s*(am|pm|AM|PM)?\s*[-–]\s*(\d{1,2}:\d{2})\s*(am|pm|AM|PM)?")

    def extract_time_range(text: str):
        if not text:
            return None, None
        m = time_pattern.search(text)
        if not m:
            return None, None
        start = m.group(1) + (f" {m.group(2)}" if m.group(2) else "")
        end = m.group(3) + (f" {m.group(4)}" if m.group(4) else "")
        return start.strip(), end.strip()

    events = []  # list of dicts: {day, start, end, title, room, faculty, raw}

    for row in body_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if not cells:
            continue

        # Determine time range from either a designated time column or the first cell
        time_text_source = None
        if time_col_index is not None and time_col_index < len(cells):
            time_text_source = cells[time_col_index].text.strip()
        else:
            time_text_source = cells[0].text.strip()
        start_time, end_time = extract_time_range(time_text_source)

        # Build map of day -> cell text using detected day columns; if not detected, try all cells beyond first
        if day_col_indices:
            for day, idx in day_col_indices.items():
                if idx >= len(cells):
                    continue
                cell_text = (cells[idx].text or "").strip()
                if not cell_text or normalize_header(cell_text) == "holiday":
                    continue
                events.append({
                    "day": day,
                    "start": start_time,
                    "end": end_time,
                    "raw": cell_text,
                })
        else:
            # Fallback: treat each non-empty cell after the first as a class for an unknown day
            for idx, c in enumerate(cells[1:], start=1):
                cell_text = (c.text or "").strip()
                if not cell_text or normalize_header(cell_text) == "holiday":
                    continue
                events.append({
                    "day": None,
                    "start": start_time,
                    "end": end_time,
                    "raw": cell_text,
                })

    if not events:
        raise Exception("No timetable data found in the table")

    # Post-process events to extract a concise title and room/faculty from raw
    def split_title_room_faculty(raw: str):
        # The raw often looks like: "COURSE\nRoom ... | COURSE2 ..." for multiple entries; split on newlines or pipes
        # We will only take the first segment per cell; duplicates are handled later
        first_segment = re.split(r"\n|\|", raw)[0].strip()

        # Try to separate course from room/faculty keywords
        # Heuristics for room/location/teacher tokens
        room_match = re.search(r"(Room\s*No?\.?\s*[^|\n]+|Room\s*\d+[^|\n]*|Block\s*\d+[^|\n]*|Lab[^|\n]*)", first_segment, flags=re.IGNORECASE)
        faculty_match = re.search(r"(Dr\.?\s*[^|\n]+|Prof\.?\s*[^|\n]+|Sir\s*[^|\n]+|Ms\.?\s*[^|\n]+|Mr\.?\s*[^|\n]+)", first_segment)

        room = room_match.group(1).strip() if room_match else None
        faculty = faculty_match.group(1).strip() if faculty_match else None

        # Remove room/faculty fragments from title if present
        title = first_segment
        if room:
            title = title.replace(room, "").strip(" -|,")
        if faculty:
            title = title.replace(faculty, "").strip(" -|,")
        title = re.sub(r"\s+", " ", title).strip()

        return title or first_segment, room, faculty

    normalized_events = []
    for ev in events:
        title, room, faculty = split_title_room_faculty(ev["raw"])
        normalized_events.append({
            "day": ev["day"],
            "start": ev["start"],
            "end": ev["end"],
            "title": title,
            "room": room,
            "faculty": faculty,
        })

    # Prefer showing today's schedule; if empty, show next non-empty day; else show a compact weekly summary
    today_idx = datetime.now().weekday()
    day_name_by_idx = {i: name for i, name in enumerate(weekday_names)}

    def format_event_line(ev):
        parts = []
        time_part = None
        if ev["start"] and ev["end"]:
            time_part = f"{ev['start']}–{ev['end']}"
        elif ev["start"]:
            time_part = ev["start"]
        if time_part:
            parts.append(time_part)
        parts.append(ev["title"])
        if ev["room"]:
            parts.append(f"({ev['room']})")
        if ev["faculty"]:
            parts.append(f"— {ev['faculty']}")
        return " ".join(parts)

    def events_for_day(day: str):
        return [e for e in normalized_events if e["day"] == day]

    # If day columns were not detected, fall back to listing all entries we have
    if day_col_indices:
        # Try today, else next day with entries
        chosen_day = day_name_by_idx.get(today_idx)
        todays_events = events_for_day(chosen_day)
        if not todays_events:
            for i in range(7):
                candidate_day = day_name_by_idx.get((today_idx + i) % 7)
                evs = events_for_day(candidate_day)
                if evs:
                    chosen_day = candidate_day
                    todays_events = evs
                    break

        if todays_events:
            message_header = f"📅 {chosen_day.capitalize()} Timetable\n\n"
            message_body = "\n".join(format_event_line(e) for e in todays_events)
            send_telegram_message(message_header + (message_body or "No classes found."))
        else:
            # Weekly compact summary
            lines = []
            for day in weekday_names:
                day_events = events_for_day(day)
                if not day_events:
                    continue
                lines.append(day.capitalize() + ":")
                for e in day_events:
                    lines.append("- " + format_event_line(e))
            message = "📅 Timetable\n\n" + ("\n".join(lines) if lines else "No classes found.")
            send_telegram_message(message)
    else:
        # Unknown day mapping, list everything with whatever time we could extract
        unique_lines = []
        seen = set()
        for e in normalized_events:
            line = format_event_line(e)
            if line and line not in seen:
                seen.add(line)
                unique_lines.append("- " + line)
        message = "📅 Timetable\n\n" + ("\n".join(unique_lines) if unique_lines else "No classes found.")
        send_telegram_message(message)

    print("📩 Sent timetable to Telegram!")

except Exception as e:
    error_msg = f"❌ Error extracting timetable: {str(e)}"
    print(error_msg)
    try:
        send_telegram_message(error_msg)
    except Exception:
        pass
    raise
finally:
    driver.quit()
    print("🚪 Browser closed.")


