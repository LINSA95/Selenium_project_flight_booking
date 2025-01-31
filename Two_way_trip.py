from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import datetime


# Function to validate dates
def is_valid_date(date_string):
    current_date = datetime.datetime.now().date()
    input_date = datetime.datetime.strptime(date_string, "%d/%m/%Y").date()
    return input_date >= current_date


# Booking details
booking_details = {
    "origin": "HYD",
    "destination": "BLR",
    "date": "25/04/2024",
    "return_date": "05/05/2024",
    "trip_type": "Round Trip",
    "adults": 2,
    "childs": 1,
    "infants": 0,
    "email": "nayan.asawa@nineleaps.com",
    "phone": "7793992929",
    "first1_N": "Nayan",
    "last1_N": "Asawa",
    "first2_N": "Krishna",
    "last2_N": "Vyas",
    "fchild1": "Madhav",
    "lchild1": "Asawa",
    "card1": "371449635398431",
    "c1name": "NAYAN ASAWA",
    "cvv": "199",
    "exp_month": "03",
    "exp_year": "2028",
}

# Validate departure and return dates
if not is_valid_date(booking_details["date"]):
    print("Error: Departure date should not be in the past.")
    exit()
if datetime.datetime.strptime(booking_details["return_date"], "%d/%m/%Y") < datetime.datetime.strptime(
        booking_details["date"], "%d/%m/%Y"):
    print("Error: Return date must be after the departure date.")
    exit()

# Initialize WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
service = Service("/home/nineleaps/Downloads/chromedriver-linux64/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10)


def find_and_click(xpath):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


def find_and_input(by, selector, value):
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((by, selector)))
    element.clear()
    element.send_keys(value)


try:
    driver.get("https://www.easemytrip.com/offers/no-convenience-fee.html")
    driver.maximize_window()

    # Select trip type
    trip_type_elements = {
        "One Way": "//*[@id='tripType']/li[1]",
        "Round Trip": "//*[@id='tripType']/li[2]",
        "Multi City": "//*[@id='tripType']/li[3]"
    }
    find_and_click(trip_type_elements[booking_details["trip_type"]])

    # Select origin
    find_and_click("//*[@id='frmcity']")
    find_and_input(By.ID, "a_FromSector_show", booking_details["origin"])
    find_and_click(f"//span[contains(text(),'{booking_details['origin']}')]")

    # Select destination
    find_and_click("//*[@id='tocity']")
    find_and_input(By.ID, "a_Editbox13_show", booking_details["destination"])
    find_and_click(f"//span[contains(text(),'{booking_details['destination']}')]")

    # Select dates
    find_and_click("//*[@id='ddate']")
    find_and_click(f"//*[@id='{booking_details['date']}']")

    if booking_details["trip_type"] == "Round Trip":
        find_and_click("//*[@id='rdate']")
        find_and_click(f"//*[@id='{booking_details['return_date']}']")

    # Select passengers
    find_and_click("//*[@id='myFunction4']")
    for _ in range(booking_details["adults"] - 1):
        find_and_click("//*[@class='add plus_box1']")
    for _ in range(booking_details["childs"]):
        find_and_click("//*[@class='add plus_boxChd']")

    # Search flights
    find_and_click("//*[@class='srchBtnSe']")
    find_and_click("//*[@id='BtnBookNow']")
    find_and_click("//*[@id='DivMoreFareRT']/div/div[3]/div/div/div[2]")

    # Scroll down and accept insurance
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    find_and_click("//*[@id='divInsuranceTab']/div[3]/div[1]/label")

    # Enter contact details
    find_and_input(By.XPATH, "//*[@id='txtEmailId']", booking_details["email"])
    find_and_click("//*[@id='spnVerifyEmail']")
    find_and_input(By.CSS_SELECTOR, "#txtCPhone", booking_details["phone"])

    # Enter passenger details
    passenger_details = [
        {"first": "first1_N", "last": "last1_N", "title_xpath": "//*[@id='titleAdult0']/option[@value='Mr']"},
        {"first": "first2_N", "last": "last2_N", "title_xpath": "//*[@id='titleAdult1']/option[@value='Mr']"}
    ]

    for i, passenger in enumerate(passenger_details):
        find_and_input(By.CSS_SELECTOR, f"#txtFNAdult{i}", booking_details[passenger["first"]])
        find_and_input(By.CSS_SELECTOR, f"#txtLNAdult{i}", booking_details[passenger["last"]])
        find_and_click(passenger["title_xpath"])

    # Child details
    find_and_input(By.CSS_SELECTOR, "#txtFNChild0", booking_details["fchild1"])
    Select(driver.find_element(By.ID, "titleChild0")).select_by_value("MSTR")
    find_and_input(By.CSS_SELECTOR, "#txtLNChild0", booking_details["lchild1"])

    # Click submit
    find_and_click("#spnTransaction")

    # Handle pop-ups and skip buttons
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "revw_rt_25")))
    find_and_click("//a[@class='edit_btn' and text()='Skip']")
    find_and_click("#skipPop")

    # Enter payment details
    find_and_input(By.ID, "CC", booking_details["card1"])
    find_and_input(By.ID, "CCN", booking_details["c1name"])
    find_and_input(By.ID, "CCCVV", booking_details["cvv"])
    Select(driver.find_element(By.ID, "CCMM")).select_by_value(booking_details["exp_month"])
    Select(driver.find_element(By.ID, "CCYYYY")).select_by_value(booking_details["exp_year"])
    find_and_click("//*[@id='card']/div[12]")  # Click "Make Payment"

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
