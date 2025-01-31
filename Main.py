import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from Booking import perform_booking
# from One_way_trip import chrome_options
from Payment import make_payment
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    """Creates and returns a WebDriver instance with necessary configurations."""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(8)
    return driver  # Returns the initialized WebDriver instance

def main():
    driver = get_driver()  # Get the WebDriver instance

    try:
        # Perform flight booking
        perform_booking(driver)

        # Perform payment
        make_payment(driver)

        print("✅ Booking and payment process completed successfully!")

    except Exception as e:
        print("An error occurred during the booking and payment process:")
        traceback.print_exc()  # Logs full error traceback for debugging

    finally:
        driver.quit()  # Ensure WebDriver is closed properly

if __name__ == "__main__":
    main()
