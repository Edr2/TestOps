import unittest
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InsiderTest(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")
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

        # Step 1: Check and close the popup if it exists
        try:
            # Locate the popup close button by its class name and click it
            popup_close_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "ins-close-button")))
            popup_close_button.click()
        except TimeoutException:
            pass  # No popup appeared, continue with the test

        company_menu = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Company")))
        company_menu.click()

        careers_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Careers")))
        careers_link.click()

        # Verify components
        self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "location-slider-prev")))
        self.wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, "See all teams")))

        h2_elements = self.driver.find_elements(By.TAG_NAME, "h2")
        found = any("Life at Insider" in element.text
                    for element in h2_elements)
        self.assertTrue(
            found, "No <h2> elements with text 'Life at Insider' were found.")

        logger.info("Careers page test passed")

    def test_03_qa_jobs(self):
        # """Test QA jobs filtering and content"""
        # self.driver.get("https://useinsider.com/careers/quality-assurance/")

        # # Click See all QA jobs
        # see_all_jobs = self.wait.until(
        #     EC.element_to_be_clickable((By.LINK_TEXT, "See all QA jobs"))
        # )
        # see_all_jobs.click()

        #TODO It should go to that link, but after investigated and seeing that frontend send 4 same requests to fetch department, I give up for now
        #self.driver.get("https://useinsider.com/careers/open-positions/

        self.driver.get(
            "https://useinsider.com/careers/open-positions/?department=qualityassurance"
        )

        decline_cookie = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Decline All")))
        decline_cookie.click()

        # TODO element should be disabled in UI(frontend) till it's loaded
        # Maximum number of attempts to retry clicking on the dropdown
        max_attempts = 3
        attempt = 0

        while attempt < max_attempts:
            try:
                # Attempt to click the location filter
                location_filter = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.ID, "select2-filter-by-location-container")))
                location_filter.click()

                # Wait and try to find the Istanbul option
                istanbul_option = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         "//li[contains(text(), 'Istanbul, Turkey')]")))
                istanbul_option.click()
                logger.info("Successfully clicked on Istanbul option.")
                break  # Exit the loop if successful

            except TimeoutException:
                attempt += 1
                logger.info(f"Attempt {attempt} failed. Retrying...")
                if attempt == max_attempts:
                    logger.info(
                        "Failed to find and click the Istanbul option after several attempts."
                    )
                    raise  # Re-raise the exception after maximum retries

        department_filter = self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "select2-filter-by-department-container")))
        department_filter.click()

        # Wait for the <ul> element to be present
        ul_element = self.wait.until(
            EC.presence_of_element_located(
                (By.ID, "select2-filter-by-department-results")))

        # Scroll down the <ul> element
        self.driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight;", ul_element)

        qa_option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(text(), 'Quality Assurance')]")))

        # TODO If there will be 1 request instead 6 with same response, maybe we can implement this code below
        # li_element = self.driver.find_element(
        #     By.XPATH, "//li[contains(text(), 'Quality Assurance')]")
        # self.driver.execute_script("arguments[0].scrollIntoView(true);",
        #    li_element)
        # self.driver.execute_script("arguments[0].focus();", li_element)
        # self.driver.execute_script(
        #     "arguments[0].setAttribute('aria-selected', arguments[1]);",
        #     li_element, "true")
        # self.driver.execute_script("arguments[0].click();", li_element)
        # li_element.click()

        actions = ActionChains(self.driver)
        actions.move_to_element(qa_option).click().perform()

        #even when I explicitly set flag ?department=qualityassurance it show on start wrong departments :(
        # wait_more = WebDriverWait(self.driver, 15)
        time.sleep(5)
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='Quality Assurance']")))

        # Verify job listings
        self.wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "position-list-item")))
        jobs = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "position-list-item")))

        for job in jobs:
            position = job.find_element(By.CLASS_NAME, "position-department")
            position_text = position.text
            location = job.find_element(By.CLASS_NAME,
                                        "position-location").text

            logger.info("TEST -- position_text: " + position_text)

            assert "Quality Assurance" in position_text
            assert "Istanbul, Turkey" in location

            logger.info("TEST -- view_role_btn start")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                job)
            actions.move_to_element(job).perform()
            view_role_btn = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "View Role")))

            expected_url = view_role_btn.get_attribute("href")
            view_role_btn.click()

            self.wait.until(EC.number_of_windows_to_be(2))
            current_tabs = self.driver.window_handles
            self.driver.switch_to.window(current_tabs[1])

            assert expected_url in self.driver.current_url, f"Expected URL {expected_url}, but got {self.driver.current_url}"

        logger.info("QA jobs test passed")


if __name__ == "__main__":
    unittest.main()
