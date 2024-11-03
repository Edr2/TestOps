# test_insider.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import unittest
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InsiderTest(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        logger.info("Setting up WebDriver")

    def tearDown(self):
        if self.driver:
            self.driver.quit()
            logger.info("Closing WebDriver")

    def test_01_homepage(self):
        """Test Insider homepage loads correctly"""
        self.driver.get("https://useinsider.com/")
        assert "Insider" in self.driver.title
        logger.info("Homepage test passed")

    def test_02_careers_page(self):
        """Test Careers page and its components"""
        self.driver.get("https://useinsider.com/")

        print("TEST1")

        # Navigate to Careers
        # company_menu = self.wait.until(
        #     EC.element_to_be_clickable((By.XPATH, "//span[text()='Company']")))
        # company_menu.click()
        
        company_menu = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Company")))
        company_menu.click()

        print("TEST2")

        careers_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Careers']")))
        careers_link.click()

        # Verify components
        self.wait.until(
            EC.presence_of_element_located((By.ID, "location-slider")))
        self.wait.until(EC.presence_of_element_located((By.ID, "teams")))
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "life-at-insider")))
        logger.info("Careers page test passed")

    # def test_03_qa_jobs(self):
    #     """Test QA jobs filtering and content"""
    #     self.driver.get("https://useinsider.com/careers/quality-assurance/")

    #     # Click See all QA jobs
    #     see_all_jobs = self.wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'See all QA jobs')]"))
    #     )
    #     see_all_jobs.click()

    #     # Filter jobs
    #     location_filter = self.wait.until(
    #         EC.element_to_be_clickable((By.ID, "filter-by-location"))
    #     )
    #     location_filter.click()

    #     istanbul_option = self.wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Istanbul, Turkey')]"))
    #     )
    #     istanbul_option.click()

    #     department_filter = self.wait.until(
    #         EC.element_to_be_clickable((By.ID, "filter-by-department"))
    #     )
    #     department_filter.click()

    #     qa_option = self.wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Quality Assurance')]"))
    #     )
    #     qa_option.click()

    #     # Verify job listings
    #     jobs = self.wait.until(
    #         EC.presence_of_all_elements_located((By.CLASS_NAME, "job-item"))
    #     )

    #     for job in jobs:
    #         position = job.find_element(By.CLASS_NAME, "position").text
    #         department = job.find_element(By.CLASS_NAME, "department").text
    #         location = job.find_element(By.CLASS_NAME, "location").text

    #         assert "Quality Assurance" in position
    #         assert "Quality Assurance" in department
    #         assert "Istanbul, Turkey" in location

    #     logger.info("QA jobs test passed")

    # def test_04_application_form(self):
    #     """Test job application redirect"""
    #     self.driver.get("https://useinsider.com/careers/quality-assurance/")

    #     view_role_button = self.wait.until(
    #         EC.element_to_be_clickable((By.CLASS_NAME, "view-role-button"))
    #     )
    #     view_role_button.click()

    #     # Switch to new tab if needed
    #     self.driver.switch_to.window(self.driver.window_handles[-1])

    #     # Verify Lever application form
    #     self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "lever-job-title")))
    #     assert "lever" in self.driver.current_url.lower()
    #     logger.info("Application form test passed")

if __name__ == "__main__":
    unittest.main()
