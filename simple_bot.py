#!/usr/bin/env python3
"""
Sharda Attendance Bot
Fetches attendance from the Sharda student portal via Selenium.
OTP is entered by the user via Telegram message.
"""

import os
import re
import asyncio
import logging
import time
from typing import Optional

from fetch_otp import get_latest_otp

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
SYSTEM_ID  = os.getenv('SYSTEM_ID')
EMAIL      = os.getenv('EMAIL')
BOT_TOKEN  = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID    = os.getenv('TELEGRAM_CHAT_ID')
LOGIN_URL  = os.getenv('LOGIN_URL', 'https://student.sharda.ac.in/login')

# Conversation states
WAITING_FOR_OTP = 1


# ─────────────────────────── Selenium helpers ──────────────────────────────

def create_driver() -> webdriver.Chrome:
    """Create a Chrome driver identical to question.py to prevent blocks."""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")  # Suppress severe warnings/prompts
    options.add_argument("--remote-allow-origins=*")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def navigate_to_login(driver: webdriver.Chrome) -> bool:
    """Open the login page and enter SYSTEM_ID to request an OTP."""
    try:
        logger.info(f"Navigating to login page: {LOGIN_URL}")
        driver.get(LOGIN_URL)

        wait = WebDriverWait(driver, 15)

        # Enter System ID
        system_id_field = wait.until(EC.presence_of_element_located((By.ID, "system_id")))
        system_id_field.clear()
        system_id_field.send_keys(SYSTEM_ID)
        logger.info("Entered System ID.")

        # Click OTP Request Button
        otp_button = wait.until(EC.element_to_be_clickable((By.ID, "send_stu_otp_email")))
        otp_button.click()
        logger.info("Clicked OTP request button.")

        time.sleep(3)
        return True

    except Exception as e:
        logger.error(f"navigate_to_login error: {e}")
        return False


def submit_otp_and_login(driver: webdriver.Chrome, otp: str) -> bool:
    """Enter the OTP and submit the login form."""
    try:
        wait = WebDriverWait(driver, 15)

        # Find OTP field
        otp_field = wait.until(EC.presence_of_element_located((By.ID, "otp")))
        otp_field.clear()
        otp_field.send_keys(otp.strip())
        logger.info("OTP entered successfully")

        # Click submit / verify button
        login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "stu-login")))
        login_button.click()
        logger.info("Clicked login/verify button")

        time.sleep(7) # Wait for Login redirect safely
        return True

    except Exception as e:
        logger.error(f"submit_otp_and_login error: {e}")
        return False


def scrape_attendance(driver: webdriver.Chrome) -> str:
    """Navigate to courses page and scrape all subject-wise data."""
    try:
        wait = WebDriverWait(driver, 15)

        # Check we're actually logged in
        current_url = driver.current_url
        page_text = driver.find_element(By.TAG_NAME, "body").text
        logger.info(f"Post-login URL: {current_url}")

        # Check for invalid OTP specifically
        if "invalid otp" in page_text.lower() or "incorrect otp" in page_text.lower():
            return "❌ Invalid OTP. Please try /attendance again."

        # Navigate to Courses Page for Subject-wise Attendance
        driver.get("https://student.sharda.ac.in/admin/courses")
        logger.info("Navigated to courses page for correct subject-wise data.")
        time.sleep(8)
        
        attendance_data = []
        try:
            attendance_table = wait.until(
                EC.presence_of_element_located((By.ID, "table1"))
            )
            time.sleep(3)  # Give time to render
            rows = attendance_table.find_elements(By.TAG_NAME, "tr")
            
            for row in rows[1:]: # Skip header
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 11:
                    course_name = cols[1].text.strip()
                    course_code = cols[2].text.strip()
                    
                    # Column 10 (last) is usually attendance percentage
                    percentage = cols[10].text.strip() or "N/A"
                    if not percentage.endswith('%') and percentage != "N/A" and percentage.replace('.','',1).isdigit():
                        percentage = percentage + "%"
                    
                    attendance_data.append(f"📚 {course_name} ({course_code}): {percentage}")
                    
            if attendance_data:
                return "📊 *Subject-wise Attendance Report*\n\n" + "\n".join(attendance_data)
        except Exception as e:
            logger.warning(f"Table scraping failed: {e}")
            logger.warning(f"Fallback page source preview: {driver.page_source[:500]}")

        # Fallback: extract percentages from page text using regex
        body_text = driver.find_element(By.TAG_NAME, "body").text
        lines = [line.strip() for line in body_text.split('\n') if '%' in line and line.strip()]
        
        if lines:
            summary = "📊 *Subject-wise Data (Regex Fallback)*\n\n" + "\n".join(lines[:20])
            return summary

        # Last resort: return first 800 chars of body text
        return f"ℹ️ Attendance page loaded but couldn't parse data.\n\n```\n{body_text[:800]}\n```"

    except Exception as e:
        logger.error(f"scrape_attendance error: {e}")
        return f"❌ Error fetching attendance: {e}"


# ─────────────────────────── Telegram handlers ─────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Sharda Attendance Bot*\n\n"
        "Use /attendance to check your attendance.\n"
        "The bot will open the Sharda portal, you'll receive an OTP on your email, "
        "then send it here.\n\n"
        "/help — show commands",
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Sharda Bot Commands*\n\n"
        "/start — Welcome message\n"
        "/attendance — Check attendance (you will be asked for OTP)\n"
        "/help — Show this help",
        parse_mode="Markdown"
    )


async def handle_attendance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fully automated attendance fetcher."""
    await update.message.reply_text("🔄 Opening Sharda portal and requesting OTP... please wait.")

    loop = asyncio.get_event_loop()

    def _automation_task():
        driver = create_driver()
        ok = navigate_to_login(driver)
        if not ok:
            try: driver.quit()
            except: pass
            return "❌ Could not reach the Sharda portal."
            
        time.sleep(5)  # Wait for email to arrive
        otp = get_latest_otp()
        
        if not otp:
            try: driver.quit()
            except: pass
            return "❌ Failed to fetch OTP independently via API."
            
        submit_otp_and_login(driver, otp)
        result = scrape_attendance(driver)
        
        try: driver.quit()
        except: pass
        return result

    try:
        result = await loop.run_in_executor(None, _automation_task)
    except Exception as e:
        result = f"❌ Error: {e}"

    try:
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception:
        # Fallback if markdown parsing fails due to raw unescaped text from the website
        await update.message.reply_text(result)


# ───────────────────────────────── Main ────────────────────────────────────

def main():
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in .env!")
        return
    if not SYSTEM_ID:
        logger.error("SYSTEM_ID not set in .env!")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("attendance", handle_attendance))

    logger.info("🚀 Sharda Attendance Bot started!")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
