import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)
# import SeleniumProject1
# from SeleniumProject1.One_way_trip import chrome_options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    """Fixture to initialize and teardown WebDriver."""


    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

    driver.implicitly_wait(8)
    yield driver  # Return WebDriver instance to tests
    driver.quit()  # Cleanup after tests finish
