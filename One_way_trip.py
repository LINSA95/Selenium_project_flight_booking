from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import datetime

def is_valid_date(date_string):
    """Check if the given date is today or a future date."""
    return datetime.datetime.strptime(date_string, "%d/%m/%Y").date() >= datetime.datetime.now().date()

# Contact Details
contact_info = {
    "email": "nayan.asawa@nineleaps.com",
    "phone": "7793992929"
}

# Trip Details
trip_details = {
    "origin": "HYD",
    "destination": "BLR",
    "departure_date": "20/05/2024",
    "return_date": "27/05/2024",
    "trip_type": "One Way"
}

# Passenger Details
passenger_details = {
    "adults": [
        {"first_name": "Nayan", "last_name": "Asawa", "title": "Mr"},
        {"first_name": "Krishna", "last_name": "Vyas", "title": "Mr"},
    ],
    "children": [
        {"first_name": "Madhav", "last_name": "Asawa", "title": "MSTR"}
    ],
    "infants": []
}

# Payment Details
payment_details = {
    "card_number": "371449635398431",
    "card_name": "NAYAN ASAWA",
    "cvv": "199",
    "expiry_month": "03",
    "expiry_year": "2028"
}

# Validate Dates
def validate_departure_date(departure_date):
    today = datetime.date.today()
    if departure_date < today:
        raise ValueError("Departure date cannot be in the past.")



if trip_details["trip_type"] == "Round Trip" and datetime.datetime.strptime(trip_details["return_date"], "%d/%m/%Y") < datetime.datetime.strptime(trip_details["departure_date"], "%d/%m/%Y"):
    print("Return date must be on or after the departure date.")
    raise ValueError("Return date must be on or after the departure date.")


# WebDriver Setup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.implicitly_wait(10)

def wait_and_click(locator):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator)).click()

def wait_and_send_keys(locator, value):
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))
    element.clear()
    element.send_keys(value)
