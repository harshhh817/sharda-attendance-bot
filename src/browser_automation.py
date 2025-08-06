""Browser automation for Sharda University attendance checking."""
import time
from typing import Dict, List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)

from .config import config
from .logger import logger
from .otp_fetcher import get_otp

class BrowserAutomation:
    ""Handles browser automation for Sharda University attendance checking."""
    
    def __init__(self, headless: bool = None):
        ""Initialize the browser automation."""
        self.headless = headless if headless is not None else config.HEADLESS
        self.driver = None
        self.attendance_data = []
        
    def __enter__(self):
        ""Context manager entry."""
        self.setup_browser()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        ""Context manager exit."""
        self.quit()
        
    def setup_browser(self):
        ""Set up the Chrome browser with appropriate options."""
        try:
            logger.info("Setting up Chrome browser...")
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Common options
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-notifications")
            
            # Initialize the WebDriver
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            # Set timeouts
            self.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
            self.driver.implicitly_wait(5)  # Global implicit wait
            
            logger.info("Browser setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup browser: {e}")
            raise
    
    def wait_for_element(self, by: str, value: str, timeout: int = None) -> Optional[object]:
        ""Wait for an element to be present on the page."""
        timeout = timeout or config.ELEMENT_TIMEOUT
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Element not found: {by}={value}")
            return None
    
    def login(self) -> bool:
        ""Log in to the Sharda University portal."""
        try:
            logger.info("Navigating to login page...")
            self.driver.get(config.LOGIN_URL)
            
            # Enter System ID
            logger.info("Entering system ID...")
            system_id_field = self.wait_for_element(By.ID, "system_id")
            if not system_id_field:
                logger.error("System ID field not found")
                return False
                
            system_id_field.clear()
            system_id_field.send_keys(config.SYSTEM_ID)
            
            # Click OTP Request Button
            logger.info("Requesting OTP...")
            otp_button = self.wait_for_element(By.ID, "send_stu_otp_email")
            if not otp_button:
                logger.error("OTP request button not found")
                return False
                
            otp_button.click()
            
            # Get OTP from email
            logger.info("Fetching OTP from email...")
            otp = get_otp()
            if not otp:
                logger.error("Failed to retrieve OTP")
                return False
                
            # Enter OTP
            logger.info("Entering OTP...")
            otp_field = self.wait_for_element(By.ID, "otp")
            if not otp_field:
                logger.error("OTP field not found")
                return False
                
            otp_field.clear()
            otp_field.send_keys(otp)
            
            # Click Login Button
            login_button = self.wait_for_element(By.CLASS_NAME, "stu-login")
            if not login_button:
                logger.error("Login button not found")
                return False
                
            login_button.click()
            
            # Verify login was successful
            if not self.wait_for_element(By.CLASS_NAME, "user-profile", 10):
                logger.error("Login verification failed - user profile not found")
                return False
                
            logger.info("Successfully logged in")
            return True
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            self.driver.save_screenshot("login_error.png")
            return False
    
    def get_attendance(self) -> List[Dict[str, str]]:
        ""Fetch attendance data from the portal."""
        try:
            logger.info("Navigating to attendance page...")
            self.driver.get(config.ATTENDANCE_URL)
            
            # Wait for the page to load
            time.sleep(5)  # Allow time for dynamic content to load
            
            # Take a screenshot for debugging
            self.driver.save_screenshot("attendance_page.png")
            logger.info("Saved attendance page screenshot")
            
            # Try to find the attendance table
            table = self.wait_for_element(By.TAG_NAME, "table")
            if not table:
                logger.error("No tables found on the page")
                return []
                
            # Get all rows from the table
            rows = table.find_elements(By.TAG_NAME, "tr")
            if not rows:
                logger.warning("No rows found in the table")
                return []
                
            attendance_data = []
            
            # Process each row (skip header row if present)
            for row in rows[1:]:
                try:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if not cols:
                        continue
                        
                    # Extract data from columns (adjust indices as needed)
                    course_data = {
                        'course_code': cols[0].text.strip() if len(cols) > 0 else "N/A",
                        'course_name': cols[1].text.strip() if len(cols) > 1 else "N/A",
                        'attendance': "N/A"
                    }
                    
                    # Try to find the attendance percentage
                    for col in cols:
                        if '%' in col.text:
                            course_data['attendance'] = col.text.strip()
                            break
                    
                    attendance_data.append(course_data)
                    
                except Exception as e:
                    logger.warning(f"Error processing row: {e}")
                    continue
            
            logger.info(f"Successfully fetched attendance for {len(attendance_data)} courses")
            return attendance_data
            
        except Exception as e:
            logger.error(f"Error fetching attendance: {e}")
            self.driver.save_screenshot("attendance_error.png")
            return []
    
    def format_attendance(self, attendance_data: List[Dict[str, str]]) -> str:
        ""Format attendance data as a readable string."""
        if not attendance_data:
            return "No attendance data available."
            
        lines = ["📊 *Attendance Report*\n"]
        
        for course in attendance_data:
            lines.append(
                f"• *{course['course_code']}*: {course['attendance']} - {course['course_name']}"
            )
        
        return "\n".join(lines)
    
    def quit(self):
        ""Close the browser."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Browser closed")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
            finally:
                self.driver = None

def check_attendance() -> Tuple[bool, str]:
    ""
    Check attendance and return status and message.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        with BrowserAutomation() as browser:
            # Log in
            if not browser.login():
                return False, "❌ Login failed. Please check your credentials and try again."
            
            # Get attendance data
            attendance_data = browser.get_attendance()
            if not attendance_data:
                return False, "❌ Failed to fetch attendance data. The website structure may have changed."
            
            # Format the results
            message = browser.format_attendance(attendance_data)
            return True, message
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False, f"❌ An unexpected error occurred: {str(e)}"
