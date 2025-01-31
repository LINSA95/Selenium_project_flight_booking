from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import datetime
from One_way_trip import trip_details, contact_info, passenger_details, payment_details, is_valid_date

def is_valid_date(date_string):
    """Check if the given date is today or a future date."""
    return datetime.datetime.strptime(date_string, "%d/%m/%Y").date() >= datetime.datetime.now().date()

def wait_and_click(driver, locator):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator)).click()

def wait_and_send_keys(driver, locator, value):
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))
    element.clear()
    element.send_keys(value)

def read_booking_data(file_path):
    """Reads booking data from Excel."""
    df = pd.read_excel(file_path)
    return df

def perform_booking():
    # Load data from Excel
    data = read_booking_data('data/booking_data.xlsx')  # Adjust the path as needed

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.get("https://www.easemytrip.com/offers/no-convenience-fee.html")
    driver.maximize_window()

    try:
        for index, row in data.iterrows():
            # Use Excel data for each booking entry
            booking_data = {
                "origin": row["origin"],
                "destination": row["destination"],
                "date": row["date"],
                "return_date": row.get("return_date", ""),  # Handle missing return date
                "trip_type": row["trip_type"],
                "adults": row["adults"],
                "childs": row["childs"],
                "infants": row["infants"]
            }

            if not is_valid_date(booking_data["date"]):
                print(f"Departure date {booking_data['date']} cannot be in the past.")
                continue

            # Select Trip Type
            trip_type_xpath = {
                "One Way": "//*[text()='One Way']",
                "Round Trip": "//*[text()='Round Trip']",
                "Multi City": "//*[text()='Multi City']"
            }
            wait_and_click(driver, (By.XPATH, trip_type_xpath[booking_data["trip_type"]]))

            # Enter Origin & Destination
            for field, value, input_id, result_xpath in zip(
                ["origin", "destination"],
                [booking_data["origin"], booking_data["destination"]],
                ["a_FromSector_show", "a_Editbox13_show"],
                ["//span[contains(text(),'HYD')]"] * 2
            ):
                wait_and_click(driver, (By.ID, field[:3] + "city"))
                wait_and_send_keys(driver, (By.ID, input_id), value)
                wait_and_click(driver, (By.XPATH, result_xpath.replace("HYD", value)))

            # Enter Departure Date
            wait_and_click(driver, (By.ID, "ddate"))
            try:
                selected_date = driver.find_element(By.ID, booking_data["date"])
                if "past" in selected_date.get_attribute("class"):
                    print(f"Select a valid date: {booking_data['date']}")
                else:
                    selected_date.click()
            except NoSuchElementException:
                print("Error: Date element not found.")

            # Enter Return Date if applicable
            if booking_data["trip_type"] == "Round Trip" and booking_data["return_date"]:
                wait_and_click(driver, (By.ID, "rdate"))
                wait_and_click(driver, (By.ID, booking_data["return_date"]))

            # Adjust Number of Passengers
            wait_and_click(driver, (By.XPATH, '//*[@id="myFunction4"]'))
            for _ in range(booking_data["adults"] - 1):
                wait_and_click(driver, (By.CSS_SELECTOR, ".add.plus_box1"))
            for _ in range(booking_data["childs"]):
                wait_and_click(driver, (By.CSS_SELECTOR, ".add.plus_boxChd"))

            # Search Flights
            wait_and_click(driver, (By.CSS_SELECTOR, ".srchBtnSe"))

            # Select First Flight
            wait_and_click(driver, (By.CLASS_NAME, "btn.book-bt-n"))

            # Enter Contact Details
            wait_and_send_keys(driver, (By.ID, "txtEmailId"), contact_info)
            wait_and_click(driver, (By.ID, "spnVerifyEmail"))

            # Enter Passenger Details (using the passenger details in the Excel or predefined list)
            passenger_details = [
                {"first_name": "Nayan", "last_name": "Asawa", "title": "Mr"},
                {"first_name": "Krishna", "last_name": "Vyas", "title": "Mr"}
            ]
            for index, passenger in enumerate(passenger_details):
                wait_and_send_keys(driver, (By.ID, f"txtFNAdult{index}"), passenger["first_name"])
                wait_and_send_keys(driver, (By.ID, f"txtLNAdult{index}"), passenger["last_name"])
                Select(driver.find_element(By.ID, f"titleAdult{index}")).select_by_value(passenger["title"])

            # Enter Child Details
            wait_and_send_keys(driver, (By.ID, "txtFNChild0"), "Madhav")
            wait_and_send_keys(driver, (By.ID, "txtLNChild0"), "Asawa")
            Select(driver.find_element(By.ID, "titleChild0")).select_by_value("MSTR")

            # Enter Phone Number
            wait_and_send_keys(driver, (By.ID, "txtCPhone"), contact_info)

            # Submit Booking
            wait_and_click(driver, (By.ID, "spnTransaction"))
            wait_and_click(driver, (By.ID, "skipPop"))

            # Skip Additional Popups
            try:
                skip_popup = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "edit_btn"))
                )
                skip_popup.click()
            except TimeoutException:
                pass

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    perform_booking()
