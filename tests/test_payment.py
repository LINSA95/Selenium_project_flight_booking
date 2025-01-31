import sys
import os

# Ensure the root project directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Payment import make_payment
from Main import get_driver


def test_payment():
    """Test case for the payment process."""
    driver = get_driver()

    try:
        make_payment(driver)
        assert True, "Payment was successful!"
    except Exception as e:
        assert False, f"Payment failed: {e}"
    finally:
        driver.quit()
