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

YOUTUBE_URL = "https://www.youtube.com"


# ============================================================
# BROWSER CONFIGURATION
# ============================================================
#
# Each entry represents one browser session.
#
# If you have multiple HeadSpin browser endpoints, add them
# here.
#
# browserName and browserVersion are the browser capabilities.
#
# The appium_url determines which HeadSpin browser endpoint
# will be used.
#
# ============================================================

BROWSERS = [
    {
        "name": "Chrome",

        "browserName": "chrome",

        "browserVersion": "131.0.6778.70",

        "appium_url": (
            f"https://dev-id-jk-0.headspin.io:9099/v0/{APITOKEN}/wd/hub"
        ),
    },

    {
        "name": "firefox",

        "browserName": "firefox",

        "browserVersion": "129.0",

        "appium_url": (
           f"https://dev-id-jk-0.headspin.io:9099/v0/{APITOKEN}/wd/hub"
        ),
    },

    # Add more browsers here if required.
    #
    # {
    #     "name": "Chrome Browser 3",
    #     "browserName": "chrome",
    #     "browserVersion": "131.0.6778.70",
    #     "appium_url": (
    #         f"https://YOUR-HEADSPIN-ENDPOINT/"
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
# CREATE BROWSER OPTIONS
# ============================================================

def create_options(browser):

    options = AppiumOptions()

    options.load_capabilities({

        # ----------------------------------------------------
        # Browser capabilities
        # ----------------------------------------------------

        "browserName": browser["browserName"],

        "browserVersion": browser["browserVersion"],

        # ----------------------------------------------------
        # Platform
        # ----------------------------------------------------

        "platformName": "Android",

        # ----------------------------------------------------
        # HeadSpin browser configuration
        # ----------------------------------------------------

        "headspin:initialScreenSize": {
            "width": 1920,
            "height": 1080
        },

        # ----------------------------------------------------
        # Appium
        # ----------------------------------------------------

        "appium:automationName": "uiautomator2",

        "appium:newCommandTimeout": 300,

        "appium:browserName": browser["browserName"],

        # ----------------------------------------------------
        # HeadSpin capture
        # ----------------------------------------------------

        "headspin:options": {
            "capture.video": False
        }
    })

    return options


# ============================================================
# WAIT FOR BROWSER
# ============================================================

def wait_for_browser(driver, browser_name):

    print(
        f"[{browser_name}] Waiting for Chrome..."
    )

    wait = WebDriverWait(driver, 30)

    try:

        wait.until(
            lambda d: d.current_url != "data:,"
        )

        print(
            f"[{browser_name}] Browser is ready."
        )

        return True

    except Exception as e:

        print(
            f"[{browser_name}] "
            f"Browser did not become ready: {e}"
        )

        return False


# ============================================================
# OPEN YOUTUBE
# ============================================================

def open_youtube(driver, browser_name):

    print(
        f"[{browser_name}] "
        f"Opening YouTube..."
    )

    try:

        driver.get(YOUTUBE_URL)

        print(
            f"[{browser_name}] "
            f"YouTube URL opened."
        )

        WebDriverWait(driver, 30).until(
            lambda d: "youtube" in d.current_url.lower()
        )

        print(
            f"[{browser_name}] "
            f"YouTube loaded."
        )

        return True

    except Exception as e:

        print(
            f"[{browser_name}] "
            f"Could not open YouTube: {e}"
        )

        return False


# ============================================================
# HANDLE YOUTUBE CONSENT
# ============================================================

def handle_youtube_consent(driver, browser_name):

    print(
        f"[{browser_name}] "
        f"Checking for YouTube consent..."
    )

    selectors = [

        (
            AppiumBy.XPATH,
            "//button[contains(., 'Accept all')]"
        ),

        (
            AppiumBy.XPATH,
            "//button[contains(., 'I agree')]"
        ),

        (
            AppiumBy.XPATH,
            "//button[contains(., 'Accept')]"
        ),

        (
            AppiumBy.XPATH,
            "//*[contains(text(), 'Accept all')]"
        ),

    ]

    for locator in selectors:

        try:

            element = WebDriverWait(
                driver,
                5
            ).until(
                EC.element_to_be_clickable(locator)
            )

            element.click()

            print(
                f"[{browser_name}] "
                f"YouTube consent accepted."
            )

            time.sleep(2)

            return True

        except Exception:
            continue

    print(
        f"[{browser_name}] "
        f"No consent popup detected."
    )

    return True


# ============================================================
# FIND SEARCH BOX
# ============================================================

def find_search_box(driver, browser_name):

    print(
        f"[{browser_name}] "
        f"Looking for YouTube search box..."
    )

    wait = WebDriverWait(driver, 30)

    selectors = [

        # YouTube search input
        (
            AppiumBy.CSS_SELECTOR,
            "input#search"
        ),

        # Name selector
        (
            AppiumBy.NAME,
            "search_query"
        ),

        # XPath
        (
            AppiumBy.XPATH,
            "//input[@id='search']"
        ),

        (
            AppiumBy.XPATH,
            "//input[@name='search_query']"
        ),

    ]

    for locator in selectors:

        try:

            element = wait.until(
                EC.presence_of_element_located(locator)
            )

            print(
                f"[{browser_name}] "
                f"YouTube search box found."
            )

            return element

        except Exception:
            continue

    print(
        f"[{browser_name}] "
        f"YouTube search box not found."
    )

    return None


# ============================================================
# SEARCH YOUTUBE
# ============================================================

def search_youtube(
    driver,
    browser_name,
    search_text
):

    print(
        f"[{browser_name}] "
        f"Searching YouTube for: {search_text}"
    )

    search_box = find_search_box(
        driver,
        browser_name
    )

    if search_box is None:
        return False

    try:

        search_box.click()

        search_box.clear()

        search_box.send_keys(search_text)

        print(
            f"[{browser_name}] "
            f"Entered search text: {search_text}"
        )

    except Exception as e:

        print(
            f"[{browser_name}] "
            f"Could not enter search text: {e}"
        )

        return False

    time.sleep(1)

    # --------------------------------------------------------
    # Submit search using ENTER
    # --------------------------------------------------------

    try:

        search_box.send_keys("\n")

        print(
            f"[{browser_name}] "
            f"Search submitted."
        )

    except Exception as e:

        print(
            f"[{browser_name}] "
            f"Could not submit search: {e}"
        )

        return False

    # --------------------------------------------------------
    # Wait for search results
    # --------------------------------------------------------

    try:

        WebDriverWait(
            driver,
            30
        ).until(
            lambda d: "results" in d.current_url.lower()
        )

        print(
            f"[{browser_name}] "
            f"Search results loaded."
        )

    except Exception:

        # URL can sometimes remain unchanged depending on
        # YouTube/browser behavior. Wait for the page instead.

        time.sleep(5)

        print(
            f"[{browser_name}] "
            f"Search results wait completed."
        )

    return True


# ============================================================
# VERIFY SEARCH RESULTS
# ============================================================

def verify_search_results(
    driver,
    browser_name,
    search_text
):

    print(
        f"[{browser_name}] "
        f"Verifying search results..."
    )

    try:

        # ----------------------------------------------------
        # Check URL
        # ----------------------------------------------------

        current_url = driver.current_url

        print(
            f"[{browser_name}] "
            f"Current URL: {current_url}"
        )

        url_contains_search = (
            "search_query" in current_url.lower()
        )

        # ----------------------------------------------------
        # Check page source
        # ----------------------------------------------------

        page_source = driver.page_source

        text_found = (
            search_text.lower()
            in page_source.lower()
        )

        # ----------------------------------------------------
        # Check YouTube result elements
        # ----------------------------------------------------

        result_elements = driver.find_elements(
            AppiumBy.XPATH,
            "//*[contains(@href, '/watch')]"
        )

        results_found = len(result_elements) > 0

        print(
            f"[{browser_name}] "
            f"Search URL detected: {url_contains_search}"
        )

        print(
            f"[{browser_name}] "
            f"Search text detected: {text_found}"
        )

        print(
            f"[{browser_name}] "
            f"Video results detected: {results_found}"
        )

        # ----------------------------------------------------
        # PASS condition
        # ----------------------------------------------------

        if url_contains_search and (
            text_found or results_found
        ):

            print(
                f"[{browser_name}] PASS - "
                f"'{search_text}' search results found."
            )

            return True

        print(
            f"[{browser_name}] FAIL - "
            f"Search results not verified."
        )

        return False

    except Exception as e:

        print(
            f"[{browser_name}] "
            f"Verification failed: {e}"
        )

        return False


# ============================================================
# RUN TEST ON ONE BROWSER
# ============================================================

def run_test(browser):

    browser_name = browser["name"]

    driver = None

    try:

        print()
        print("=" * 70)

        print(
            f"[{browser_name}] TEST STARTED"
        )

        print("=" * 70)

        # ----------------------------------------------------
        # Create browser capabilities
        # ----------------------------------------------------

        options = create_options(browser)

        print(
            f"[{browser_name}] "
            f"Browser: {browser['browserName']}"
        )

        print(
            f"[{browser_name}] "
            f"Browser version: "
            f"{browser['browserVersion']}"
        )

        print(
            f"[{browser_name}] "
            f"Starting Appium browser session..."
        )

        # ----------------------------------------------------
        # Start Appium session
        # ----------------------------------------------------

        driver = webdriver.Remote(
            command_executor=browser["appium_url"],
            options=options
        )

        print(
            f"[{browser_name}] "
            f"Browser session started."
        )

        time.sleep(3)

        # ----------------------------------------------------
        # Browser information
        # ----------------------------------------------------

        try:

            print(
                f"[{browser_name}] "
                f"Current URL: "
                f"{driver.current_url}"
            )

        except Exception:
            pass

        # ----------------------------------------------------
        # Wait for browser
        # ----------------------------------------------------

        if not wait_for_browser(
            driver,
            browser_name
        ):

            with results_lock:
                results[browser_name] = False

            return

        # ----------------------------------------------------
        # Open YouTube
        # ----------------------------------------------------

        if not open_youtube(
            driver,
            browser_name
        ):

            with results_lock:
                results[browser_name] = False

            return

        # ----------------------------------------------------
        # Handle consent
        # ----------------------------------------------------

        handle_youtube_consent(
            driver,
            browser_name
        )

        time.sleep(2)

        # ----------------------------------------------------
        # Search YouTube
        # ----------------------------------------------------

        if not search_youtube(
            driver,
            browser_name,
            SEARCH_TEXT
        ):

            with results_lock:
                results[browser_name] = False

            return

        # ----------------------------------------------------
        # Verify results
        # ----------------------------------------------------

        test_passed = verify_search_results(
            driver,
            browser_name,
            SEARCH_TEXT
        )

        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        with results_lock:

            results[browser_name] = test_passed

        if test_passed:

            print(
                f"[{browser_name}] TEST PASSED"
            )

        else:

            print(
                f"[{browser_name}] TEST FAILED"
            )

    except Exception as e:

        print(
            f"[{browser_name}] ERROR: {e}"
        )

        with results_lock:

            results[browser_name] = False

    finally:

        # ----------------------------------------------------
        # Close browser session
        # ----------------------------------------------------

        if driver is not None:

            try:

                driver.quit()

                print(
                    f"[{browser_name}] "
                    f"Browser session closed."
                )

            except Exception as e:

                print(
                    f"[{browser_name}] "
                    f"Error closing session: {e}"
                )

        print("=" * 70)

        print(
            f"[{browser_name}] TEST FINISHED"
        )

        print("=" * 70)


# ============================================================
# RUN BROWSERS IN PARALLEL
# ============================================================

def run_parallel_tests():

    print()
    print("=" * 70)
    print("HEADSPIN PARALLEL YOUTUBE BROWSER TEST")
    print("=" * 70)

    print(
        f"Search text: {SEARCH_TEXT}"
    )

    print(
        f"Number of browsers: {len(BROWSERS)}"
    )

    print("=" * 70)

    threads = []

    # --------------------------------------------------------
    # Create one thread per browser
    # --------------------------------------------------------

    for browser in BROWSERS:

        thread = threading.Thread(
            target=run_test,
            args=(browser,),
            name=browser["name"]
        )

        threads.append(thread)

    print()
    print("Starting all browsers...")
    print()

    # --------------------------------------------------------
    # Start all browsers
    # --------------------------------------------------------

    for thread in threads:

        thread.start()

    # --------------------------------------------------------
    # Wait for all browsers
    # --------------------------------------------------------

    for thread in threads:

        thread.join()

    # --------------------------------------------------------
    # Final results
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("FINAL TEST RESULTS")
    print("=" * 70)

    all_passed = True

    for browser in BROWSERS:

        browser_name = browser["name"]

        passed = results.get(
            browser_name,
            False
        )

        if passed:

            print(
                f"[PASS] {browser_name}"
            )

        else:

            print(
                f"[FAIL] {browser_name}"
            )

            all_passed = False

    print("=" * 70)

    if all_passed:

        print(
            "ALL BROWSERS PASSED"
        )

        return 0

    print(
        "ONE OR MORE BROWSERS FAILED"
    )

    return 1


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    exit_code = run_parallel_tests()

    sys.exit(exit_code)