import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

def make_payment(driver):
    """Handles the payment process on EaseMyTrip."""
    card_number = "371449635398431"
    card_name = "NAYAN ASAWA"
    cvv = "199"

    try:
        print("Navigating to payment page...")

        # Wait until card input is interactable and enter card details
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "CC"))).send_keys(card_number)

        # Enter cardholder name
        driver.find_element(By.ID, "CCN").send_keys(card_name)

        # Enter CVV
        driver.find_element(By.ID, "CCCVV").send_keys(cvv)

        # Select expiration month
        Select(driver.find_element(By.ID, "CCMM")).select_by_value("03")  # March

        # Select expiration year
        Select(driver.find_element(By.ID, "CCYYYY")).select_by_value("2028")

        # Click "Make Payment"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="card"]/div[12]'))).click()

        print("Payment submitted successfully!")

    except TimeoutException:
        print("Error: A required element did not load in time.")
    except Exception as e:
        print("An error occurred during payment:")
        traceback.print_exc()
