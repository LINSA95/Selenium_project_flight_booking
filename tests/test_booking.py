import sys
import os

# Ensure the root project directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Booking import perform_booking
from Main import get_driver


def test_booking():
    """Test case for flight booking process."""
    driver = get_driver()

    try:
        perform_booking()
        assert True, "Booking was successful!"
    except Exception as e:
        assert False, f"Booking failed: {e}"
    finally:
        driver.quit()
