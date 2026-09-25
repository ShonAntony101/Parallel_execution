import threading
import time
import sys

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# CONFIGURATION
# ============================================================

APITOKEN = "191cd7d19e0e4034992ac4dabf14d573"

SEARCH_TEXT = "MKBHD"

YOUTUBE_PACKAGE = "com.google.android.youtube"

YOUTUBE_ACTIVITY = (
    "com.google.android.youtube.app.honeycomb.Shell$HomeActivity"
)


# ============================================================
# DEVICE CONFIGURATION
# ============================================================

DEVICES = [
    {
        "name": "SAMSUNG Galaxy S24 Ultra",
        "device_id": "R5CWC0ARCJR",
        "device_name": "SAMSUNG Galaxy S24 Ultra",
        "appium_url": (
            f"https://dev-ca-tor-0.headspin.io:7047/"
            f"v0/{APITOKEN}/wd/hub"
        ),
    },
    {
        "name": "SAMSUNG Galaxy S20 FE",
        "device_id": "RZ8NC0VQ79X",
        "device_name": "SAMSUNG Galaxy S20 FE",
        "appium_url": (
            f"https://dev-gb-lhr-3.headspin.io:7007/"
            f"v0/{APITOKEN}/wd/hub"
        ),
    },
    # {
    #     "name": "XIAOMI Note 9S",
    #     "device_id": "ae4f0acd",
    #     "device_name": "XIAOMI Note 9S",
    #     "appium_url": (
    #         f"https://dev-gb-lhr-2.headspin.io:7048/"
    #         f"v0/{APITOKEN}/wd/hub"
    #     ),
    # },
]


# ============================================================
# RESULTS
# ============================================================

results = {}
results_lock = threading.Lock()


# ============================================================
# CREATE APPIUM OPTIONS
# ============================================================

def create_options(device):

    options = AppiumOptions()

    options.load_capabilities({
        "appium:options": {
            "automationName": "uiautomator2",
            "platformName": "Android",
            "deviceName": device["device_name"],
            "udid": device["device_id"],
            "appPackage": YOUTUBE_PACKAGE,
            "appActivity": YOUTUBE_ACTIVITY,
            "autoGrantPermissions": True,
            "newCommandTimeout": 300,
            "stayAwake": True,
        },

        "headspin:options": {
            "capture.video": True
        }
    })

    return options


# ============================================================
# WAIT FOR YOUTUBE
# ============================================================

def wait_for_youtube(driver, device_name):

    print(
        f"[{device_name}] Waiting for YouTube..."
    )

    wait = WebDriverWait(driver, 30)

    try:

        wait.until(
            lambda d: d.current_package == YOUTUBE_PACKAGE
        )

        print(
            f"[{device_name}] YouTube is active."
        )

        return True

    except Exception as e:

        print(
            f"[{device_name}] "
            f"YouTube did not become active: {e}"
        )

        return False


# ============================================================
# FIND SEARCH BUTTON
# ============================================================

def find_search_button(driver, device_name):

    wait = WebDriverWait(driver, 30)

    selectors = [
        (
            AppiumBy.ACCESSIBILITY_ID,
            "Search"
        ),
        (
            AppiumBy.XPATH,
            "//*[@content-desc='Search']"
        ),
        (
            AppiumBy.XPATH,
            "//android.widget.Button[@content-desc='Search']"
        ),
    ]

    for locator in selectors:

        try:

            element = wait.until(
                EC.presence_of_element_located(locator)
            )

            print(
                f"[{device_name}] Search button found."
            )

            return element

        except Exception:
            continue

    print(
        f"[{device_name}] Search button not found."
    )

    return None


# ============================================================
# FIND SEARCH INPUT
# ============================================================

def find_search_input(driver, device_name):

    wait = WebDriverWait(driver, 30)

    selectors = [
        (
            AppiumBy.XPATH,
            "//android.widget.EditText"
        ),
        (
            AppiumBy.CLASS_NAME,
            "android.widget.EditText"
        ),
        (
            AppiumBy.XPATH,
            "//*[@text='Search YouTube']"
        ),
    ]

    for locator in selectors:

        try:

            element = wait.until(
                EC.presence_of_element_located(locator)
            )

            print(
                f"[{device_name}] Search input found."
            )

            return element

        except Exception:
            continue

    print(
        f"[{device_name}] Search input not found."
    )

    return None


# ============================================================
# SEARCH YOUTUBE
# ============================================================

def search_youtube(driver, device_name, search_text):

    print(
        f"[{device_name}] "
        f"Searching for: {search_text}"
    )

    search_button = find_search_button(
        driver,
        device_name
    )

    if search_button is None:
        return False

    try:

        search_button.click()

        print(
            f"[{device_name}] "
            f"Search button clicked."
        )

    except Exception as e:

        print(
            f"[{device_name}] "
            f"Could not click Search: {e}"
        )

        return False

    time.sleep(2)

    search_input = find_search_input(
        driver,
        device_name
    )

    if search_input is None:
        return False

    try:

        search_input.click()

        search_input.clear()

        search_input.send_keys(search_text)

        print(
            f"[{device_name}] "
            f"Entered: {search_text}"
        )

    except Exception as e:

        print(
            f"[{device_name}] "
            f"Could not enter search text: {e}"
        )

        return False

    time.sleep(1)

    try:

        # Appium key command, not ADB
        driver.press_keycode(66)

        print(
            f"[{device_name}] "
            f"Search submitted."
        )

    except Exception as e:

        print(
            f"[{device_name}] "
            f"Could not submit search: {e}"
        )

        return False

    time.sleep(5)

    return True


# ============================================================
# VERIFY SEARCH RESULTS
# ============================================================

def verify_search_results(
    driver,
    device_name,
    search_text
):

    print(
        f"[{device_name}] "
        f"Verifying search results..."
    )

    try:

        page_source = driver.page_source

        if search_text.lower() in page_source.lower():

            print(
                f"[{device_name}] PASS - "
                f"'{search_text}' found."
            )

            return True

        print(
            f"[{device_name}] FAIL - "
            f"'{search_text}' not found."
        )

        return False

    except Exception as e:

        print(
            f"[{device_name}] "
            f"Verification failed: {e}"
        )

        return False


# ============================================================
# RUN TEST ON ONE DEVICE
# ============================================================

def run_test(device):

    device_name = device["name"]

    driver = None

    try:

        print()
        print("=" * 70)
        print(
            f"[{device_name}] TEST STARTED"
        )
        print("=" * 70)

        options = create_options(device)

        print(
            f"[{device_name}] "
            f"Starting Appium session..."
        )

        driver = webdriver.Remote(
            command_executor=device["appium_url"],
            options=options
        )

        print(
            f"[{device_name}] "
            f"Appium session started."
        )

        time.sleep(5)

        try:

            print(
                f"[{device_name}] "
                f"Current package: "
                f"{driver.current_package}"
            )

        except Exception:
            pass

        # ----------------------------------------------------
        # Wait for YouTube
        # ----------------------------------------------------

        if not wait_for_youtube(
            driver,
            device_name
        ):

            with results_lock:
                results[device_name] = False

            return

        # ----------------------------------------------------
        # Search YouTube
        # ----------------------------------------------------

        if not search_youtube(
            driver,
            device_name,
            SEARCH_TEXT
        ):

            with results_lock:
                results[device_name] = False

            return

        # ----------------------------------------------------
        # Verify
        # ----------------------------------------------------

        test_passed = verify_search_results(
            driver,
            device_name,
            SEARCH_TEXT
        )

        with results_lock:

            results[device_name] = test_passed

        if test_passed:

            print(
                f"[{device_name}] TEST PASSED"
            )

        else:

            print(
                f"[{device_name}] TEST FAILED"
            )

    except Exception as e:

        print(
            f"[{device_name}] ERROR: {e}"
        )

        with results_lock:

            results[device_name] = False

    finally:

        if driver is not None:

            try:

                driver.quit()

                print(
                    f"[{device_name}] "
                    f"Appium session closed."
                )

            except Exception as e:

                print(
                    f"[{device_name}] "
                    f"Error closing session: {e}"
                )

        print("=" * 70)

        print(
            f"[{device_name}] TEST FINISHED"
        )

        print("=" * 70)


# ============================================================
# RUN TESTS IN PARALLEL
# ============================================================

def run_parallel_tests():

    print()
    print("=" * 70)
    print("HEADSPIN PARALLEL YOUTUBE TEST")
    print("=" * 70)

    print(
        f"Search text: {SEARCH_TEXT}"
    )

    print(
        f"Number of devices: {len(DEVICES)}"
    )

    print("=" * 70)

    threads = []

    for device in DEVICES:

        thread = threading.Thread(
            target=run_test,
            args=(device,),
            name=device["name"]
        )

        threads.append(thread)

    print()
    print("Starting all devices...")
    print()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print()
    print("=" * 70)
    print("FINAL TEST RESULTS")
    print("=" * 70)

    all_passed = True

    for device in DEVICES:

        device_name = device["name"]

        passed = results.get(
            device_name,
            False
        )

        if passed:

            print(
                f"[PASS] {device_name}"
            )

        else:

            print(
                f"[FAIL] {device_name}"
            )

            all_passed = False

    print("=" * 70)

    if all_passed:

        print("ALL DEVICES PASSED")

        return 0

    print("ONE OR MORE DEVICES FAILED")

    return 1


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    exit_code = run_parallel_tests()

    sys.exit(exit_code)