import threading
import time

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# CONFIGURATION
# ============================================================

APITOKEN = "e70f41cd904c4a3998fde1d73a13c947"

CHAT_APP_PACKAGE = "net.gochat.app"
CHAT_APP_ACTIVITY = "com.vianeos.octochat.Default"

MESSAGE = "hi headspin 2"
CONTACT_NAME = "headspin 2"


# ============================================================
# DEVICE CONFIGURATION
# ============================================================

DEVICES = {
    "Device 1": {
        "device_name": "SM-A546E",
        "udid": "RZCW31MATCE",
        "appium_url": (
            f"https://dev-in-blr-0.headspin.io:7008"
            f"/v0/{APITOKEN}/wd/hub"
        ),
    },

    "Device 2": {
        "device_name": "SM-G780F",
        "udid": "RZ8NC0VQ79X",
        "appium_url": (
            f"https://dev-gb-lhr-3.headspin.io:7007"
            f"/v0/{APITOKEN}/wd/hub"
        ),
    },
}


# ============================================================
# DEVICE 1 LOCATORS
# ============================================================

DEVICE_1_SEARCH_BUTTON = (
    '//android.widget.Button'
    '[@resource-id="net.gochat.app:id/calls_search_bar"]'
)

DEVICE_1_SEARCH_INPUT = (
    '//android.widget.AutoCompleteTextView'
    '[@resource-id="net.gochat.app:id/search_src_text"]'
)

DEVICE_1_SEARCH_CONTACT = (
    '//android.widget.TextView'
    '[@resource-id="net.gochat.app:id/search_contact_name"]'
)

DEVICE_1_CHAT_TEXTFIELD = (
    '//android.widget.EditText'
    '[@resource-id="net.gochat.app:id/chat_input_field"]'
)

DEVICE_1_SEND_BUTTON = (
    '//android.widget.Button[@content-desc="Send Icon"]'
)


# ============================================================
# DEVICE 2 LOCATORS
# ============================================================

DEVICE_2_CHATS_TAB = (
    '//android.widget.TextView'
    '[@resource-id="net.gochat.app:id/tab_text" and @text="Chats"]'
)

DEVICE_2_CHAT_NAME = (
    '//android.widget.TextView'
    '[@resource-id="net.gochat.app:id/chat_title" and @text="‎Headspin"]'
)

HAMBURGER_BUTTON = (
    '//android.widget.Button[@content-desc="last"]'
)

DELETE_CHAT = (
    '//android.widget.TextView'
    '[@resource-id="net.gochat.app:id/title" and @text="Delete Chat"]'
)

DELETE_CONFIRM_BUTTON = (
    '//android.widget.Button'
    '[@resource-id="net.gochat.app:id/positive_btn"]'
)


# ============================================================
# GLOBAL DRIVER STORAGE
# ============================================================

drivers = {
    "Device 1": None,
    "Device 2": None,
}

session_errors = {
    "Device 1": None,
    "Device 2": None,
}


# ============================================================
# START APPIUM SESSION
# ============================================================

def start_session(device_key):

    device = DEVICES[device_key]

    print()
    print("=" * 70)
    print(f"[{device_key}] STARTING APPIUM SESSION")
    print("=" * 70)

    try:

        options = AppiumOptions()

        capabilities = {
            "platformName": "android",
            "appium:automationName": "uiautomator2",
            "appium:deviceName": device["device_name"],
            "appium:udid": device["udid"],

            # ====================================================
            # HEADSPIN RECORDER / CAPTURE
            # ====================================================

            "headspin:capture": True,
            "headspin:capture.disableHttp2": True,
        }

        options.load_capabilities(capabilities)

        print(f"[{device_key}] Device Name : {device['device_name']}")
        print(f"[{device_key}] UDID        : {device['udid']}")
        print(f"[{device_key}] Capture     : ENABLED")
        print(f"[{device_key}] Connecting...")

        driver = webdriver.Remote(
            command_executor=device["appium_url"],
            options=options,
        )

        drivers[device_key] = driver

        print()
        print(f"[{device_key}] SESSION CREATED")
        print(f"[{device_key}] Session ID: {driver.session_id}")

    except Exception as e:

        session_errors[device_key] = e

        print()
        print(f"[{device_key}] SESSION CREATION FAILED")
        print(f"[{device_key}] Error: {e}")


# ============================================================
# LAUNCH APPLICATION FROM FRESH PROCESS
# ============================================================

def launch_chat_app(driver, device_key):

    print()
    print("=" * 70)
    print(f"[{device_key}] LAUNCHING APPLICATION FROM HOME")
    print("=" * 70)

    try:

        # --------------------------------------------------------
        # Terminate the currently running application
        # --------------------------------------------------------

        print(
            f"[{device_key}] Terminating existing application..."
        )

        try:
            driver.terminate_app(CHAT_APP_PACKAGE)

            print(
                f"[{device_key}] Application terminated."
            )

        except Exception as e:

            print(
                f"[{device_key}] Application was not running "
                f"or could not be terminated: {e}"
            )

        time.sleep(2)

        # --------------------------------------------------------
        # Launch application again
        # --------------------------------------------------------

        print(
            f"[{device_key}] Starting application..."
        )

        driver.activate_app(CHAT_APP_PACKAGE)

        # Wait for application to initialize
        time.sleep(5)

        # --------------------------------------------------------
        # Print current state
        # --------------------------------------------------------

        try:
            print(
                f"[{device_key}] Current Package : "
                f"{driver.current_package}"
            )
        except Exception:
            pass

        try:
            print(
                f"[{device_key}] Current Activity: "
                f"{driver.current_activity}"
            )
        except Exception:
            pass

        print()
        print(
            f"[{device_key}] Application started "
            f"from a fresh process."
        )

        return True

    except Exception as e:

        print()
        print(
            f"[{device_key}] APPLICATION LAUNCH FAILED"
        )

        print(
            f"[{device_key}] Error: {e}"
        )

        return False


# ============================================================
# FIND SEARCH BUTTON
# ============================================================

def find_search_button(driver):

    print()
    print("=" * 70)
    print("SEARCH FIELD CHECK")
    print("=" * 70)

    for attempt in range(1, 4):

        print(
            f"Search attempt {attempt}/3"
        )

        try:

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        AppiumBy.XPATH,
                        DEVICE_1_SEARCH_BUTTON
                    )
                )
            )

            print(
                "Search button found."
            )

            return element

        except Exception as e:

            print(
                f"Search button not found "
                f"on attempt {attempt}."
            )

            print(
                f"Error: {e}"
            )

            time.sleep(3)

            # Relaunch the app if UI has not loaded correctly
            try:

                driver.activate_app(
                    CHAT_APP_PACKAGE
                )

                time.sleep(2)

            except Exception:
                pass

    # ========================================================
    # DIAGNOSTICS
    # ========================================================

    print()
    print("=" * 70)
    print("SEARCH FIELD DIAGNOSTICS")
    print("=" * 70)

    try:
        print(
            "Current Package :",
            driver.current_package
        )
    except Exception as e:
        print(
            "Could not get current package:",
            e
        )

    try:
        print(
            "Current Activity:",
            driver.current_activity
        )
    except Exception as e:
        print(
            "Could not get current activity:",
            e
        )

    print()
    print("Expected Search XPath:")
    print(
        DEVICE_1_SEARCH_BUTTON
    )

    print()
    print("CURRENT PAGE SOURCE")
    print("-" * 70)

    try:
        print(
            driver.page_source
        )
    except Exception as e:
        print(
            "Could not get page source:",
            e
        )

    print("-" * 70)

    return None


# ============================================================
# ENTER CHAT MESSAGE
# ============================================================

def enter_chat_message(driver, message):

    print()
    print(
        "[Device 1] Looking for chat textfield..."
    )

    chat_textfield = WebDriverWait(
        driver,
        30
    ).until(
        EC.presence_of_element_located(
            (
                AppiumBy.XPATH,
                DEVICE_1_CHAT_TEXTFIELD
            )
        )
    )

    print(
        "[Device 1] Chat textfield found."
    )

    # Click first
    chat_textfield.click()

    time.sleep(1)

    # --------------------------------------------------------
    # Try send_keys()
    # --------------------------------------------------------

    try:

        chat_textfield.send_keys(
            message
        )

        print(
            f"[Device 1] Message entered using send_keys(): "
            f"{message}"
        )

        return True

    except Exception as e:

        print(
            "[Device 1] send_keys() failed."
        )

        print(
            f"[Device 1] Error: {e}"
        )

    # --------------------------------------------------------
    # Try set_value()
    # --------------------------------------------------------

    try:

        chat_textfield.set_value(
            message
        )

        print(
            f"[Device 1] Message entered using set_value(): "
            f"{message}"
        )

        return True

    except Exception as e:

        print(
            "[Device 1] set_value() failed."
        )

        print(
            f"[Device 1] Error: {e}"
        )

    return False


# ============================================================
# VERIFY MESSAGE
# ============================================================

def verify_message(
    driver,
    message,
    device_key,
    timeout=30
):

    message_xpath = (
        f'//android.widget.TextView[@text="{message}"]'
    )

    print()
    print(
        f"[{device_key}] Verifying message..."
    )

    print(
        f"[{device_key}] XPath: "
        f"{message_xpath}"
    )

    try:

        element = WebDriverWait(
            driver,
            timeout
        ).until(
            EC.presence_of_element_located(
                (
                    AppiumBy.XPATH,
                    message_xpath
                )
            )
        )

        actual_message = (
            element.get_attribute("text")
        )

        print(
            f"[{device_key}] Expected: {message}"
        )

        print(
            f"[{device_key}] Actual  : {actual_message}"
        )

        if actual_message == message:

            print(
                f"[{device_key}] MESSAGE VERIFIED"
            )

            return True

        raise Exception(
            f"Message mismatch. "
            f"Expected '{message}', "
            f"received '{actual_message}'"
        )

    except Exception as e:

        print()
        print(
            f"[{device_key}] MESSAGE VERIFICATION FAILED"
        )

        raise e


# ============================================================
# DEVICE 1 - SEND MESSAGE
# ============================================================

def send_message(driver):

    print()
    print("=" * 70)
    print("DEVICE 1 - SEND MESSAGE")
    print("=" * 70)

    # --------------------------------------------------------
    # STEP 1
    # Search button
    # --------------------------------------------------------

    print()
    print(
        "[Device 1] Step 1: Finding search button..."
    )

    search_button = find_search_button(
        driver
    )

    if search_button is None:

        raise Exception(
            "Device 1 search button could not be located."
        )

    search_button.click()

    print(
        "[Device 1] Search button clicked."
    )

    time.sleep(2)

    # --------------------------------------------------------
    # STEP 2
    # Search input
    # --------------------------------------------------------

    print()
    print(
        "[Device 1] Step 2: Entering contact name..."
    )

    search_input = WebDriverWait(
        driver,
        30
    ).until(
        EC.presence_of_element_located(
            (
                AppiumBy.XPATH,
                DEVICE_1_SEARCH_INPUT
            )
        )
    )

    search_input.click()

    time.sleep(1)

    try:

        search_input.set_value(
            CONTACT_NAME
        )

        print(
            f"[Device 1] Contact entered using "
            f"set_value(): {CONTACT_NAME}"
        )

    except Exception as e:

        print(
            "[Device 1] Search set_value() failed."
        )

        print(
            f"Error: {e}"
        )

        try:

            search_input.send_keys(
                CONTACT_NAME
            )

            print(
                f"[Device 1] Contact entered using "
                f"send_keys(): {CONTACT_NAME}"
            )

        except Exception as e2:

            raise Exception(
                f"Could not enter contact name: {e2}"
            )

    time.sleep(3)

    # --------------------------------------------------------
    # STEP 3
    # Select contact
    # --------------------------------------------------------

    print()
    print(
        "[Device 1] Step 3: Selecting contact..."
    )

    contact = WebDriverWait(
        driver,
        30
    ).until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                DEVICE_1_SEARCH_CONTACT
            )
        )
    )

    contact.click()

    print(
        "[Device 1] Contact selected."
    )

    time.sleep(3)

    # --------------------------------------------------------
    # STEP 4
    # Enter message
    # --------------------------------------------------------

    print()
    print(
        "[Device 1] Step 4: Entering message..."
    )

    message_entered = enter_chat_message(
        driver,
        MESSAGE
    )

    if not message_entered:

        raise Exception(
            "Could not enter message into "
            "chat textfield."
        )

    time.sleep(1)

    # --------------------------------------------------------
    # STEP 5
    # Send message
    # --------------------------------------------------------

    print()
    print(
        "[Device 1] Step 5: Sending message..."
    )

    send_button = WebDriverWait(
        driver,
        30
    ).until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                DEVICE_1_SEND_BUTTON
            )
        )
    )

    send_button.click()

    print(
        "[Device 1] Send button clicked."
    )

    time.sleep(3)

    # --------------------------------------------------------
    # STEP 6
    # Verify sent message
    # --------------------------------------------------------

    print()
    print(
        "[Device 1] Step 6: Verifying sent message..."
    )

    verify_message(
        driver,
        MESSAGE,
        "Device 1"
    )

    print()
    print("=" * 70)
    print("DEVICE 1 MESSAGE SENT SUCCESSFULLY")
    print("=" * 70)


# ============================================================
# DEVICE 2 - RECEIVE MESSAGE
# ============================================================

def receive_message(driver):

    print()
    print("=" * 70)
    print("DEVICE 2 - RECEIVE MESSAGE")
    print("=" * 70)

    # --------------------------------------------------------
    # STEP 1
    # Open Chats
    # --------------------------------------------------------

    print()
    print(
        "[Device 2] Step 1: Opening Chats..."
    )

    chats_tab = WebDriverWait(
        driver,
        30
    ).until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                DEVICE_2_CHATS_TAB
            )
        )
    )

    chats_tab.click()

    print(
        "[Device 2] Chats clicked."
    )

    time.sleep(3)

    # --------------------------------------------------------
    # STEP 2
    # Open Headspin chat
    # --------------------------------------------------------

    print()
    print(
        "[Device 2] Step 2: Opening Headspin chat..."
    )

    chat_name = WebDriverWait(
        driver,
        30
    ).until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                DEVICE_2_CHAT_NAME
            )
        )
    )

    chat_name.click()

    print(
        "[Device 2] Headspin chat opened."
    )

    time.sleep(3)

    # --------------------------------------------------------
    # STEP 3
    # Verify received message
    # --------------------------------------------------------

    print()
    print(
        "[Device 2] Step 3: Verifying received message..."
    )

    verify_message(
        driver,
        MESSAGE,
        "Device 2"
    )

    print()
    print("=" * 70)
    print("DEVICE 2 MESSAGE RECEIVED SUCCESSFULLY")
    print("=" * 70)


# ============================================================
# DELETE CHAT
# ============================================================

def delete_chat(driver, device_key):

    print()
    print("=" * 70)
    print(f"[{device_key}] DELETE CHAT")
    print("=" * 70)

    # --------------------------------------------------------
    # Open hamburger menu
    # --------------------------------------------------------

    print(
        f"[{device_key}] Opening hamburger menu..."
    )

    hamburger = WebDriverWait(
        driver,
        30
    ).until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                HAMBURGER_BUTTON
            )
        )
    )

    hamburger.click()

    print(
        f"[{device_key}] Hamburger menu clicked."
    )

    time.sleep(2)

    # --------------------------------------------------------
    # Delete Chat
    # --------------------------------------------------------

    print(
        f"[{device_key}] Selecting Delete Chat..."
    )

    delete_button = WebDriverWait(
        driver,
        30
    ).until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                DELETE_CHAT
            )
        )
    )

    delete_button.click()

    print(
        f"[{device_key}] Delete Chat clicked."
    )

    time.sleep(2)

    # --------------------------------------------------------
    # Confirm Delete
    # --------------------------------------------------------

    print(
        f"[{device_key}] Confirming chat deletion..."
    )

    delete_confirm_button = WebDriverWait(
        driver,
        30
    ).until(
        EC.element_to_be_clickable(
            (
                AppiumBy.XPATH,
                DELETE_CONFIRM_BUTTON
            )
        )
    )

    delete_confirm_button.click()

    print(
        f"[{device_key}] Delete confirmation button clicked."
    )

    time.sleep(3)

    print(
        f"[{device_key}] Chat deletion completed."
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("HEADSPIN TWO-DEVICE CHAT TEST")
    print("=" * 70)

    print(
        f"Message  : {MESSAGE}"
    )

    print(
        f"Contact  : {CONTACT_NAME}"
    )

    print(
        "Device 1 : SM-A546E"
    )

    print(
        "Device 2 : SM-G780F"
    )

    print(
        "Recorder : ENABLED"
    )

    print(
        "App State: FRESH PROCESS"
    )

    print("=" * 70)

    # ========================================================
    # START BOTH SESSIONS IN PARALLEL
    # ========================================================

    print()
    print(
        "STARTING TWO INDEPENDENT APPIUM SESSIONS"
    )

    thread_1 = threading.Thread(
        target=start_session,
        args=("Device 1",)
    )

    thread_2 = threading.Thread(
        target=start_session,
        args=("Device 2",)
    )

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    # ========================================================
    # CHECK SESSIONS
    # ========================================================

    if (
        drivers["Device 1"] is None
        or drivers["Device 2"] is None
    ):

        print()
        print("=" * 70)
        print("SESSION CREATION FAILED")
        print("=" * 70)

        if session_errors["Device 1"]:

            print(
                "[Device 1] Error:",
                session_errors["Device 1"]
            )

        if session_errors["Device 2"]:

            print(
                "[Device 2] Error:",
                session_errors["Device 2"]
            )

        for driver in drivers.values():

            if driver:

                try:
                    driver.quit()
                except Exception:
                    pass

        return

    driver_1 = drivers["Device 1"]
    driver_2 = drivers["Device 2"]

    try:

        # ====================================================
        # LAUNCH BOTH APPLICATIONS
        # ====================================================

        print()
        print("=" * 70)
        print("RESETTING APPLICATION STATE")
        print("=" * 70)

        device_1_started = launch_chat_app(
            driver_1,
            "Device 1"
        )

        device_2_started = launch_chat_app(
            driver_2,
            "Device 2"
        )

        if not device_1_started:

            raise Exception(
                "Device 1 application could not be launched."
            )

        if not device_2_started:

            raise Exception(
                "Device 2 application could not be launched."
            )

        # ====================================================
        # DEVICE 1 SEND MESSAGE
        # ====================================================

        send_message(
            driver_1
        )

        # ====================================================
        # DEVICE 2 RECEIVE MESSAGE
        # ====================================================

        receive_message(
            driver_2
        )

        # ====================================================
        # DELETE DEVICE 2 CHAT
        # ====================================================

        delete_chat(
            driver_2,
            "Device 2"
        )

        # ====================================================
        # DELETE DEVICE 1 CHAT
        # ====================================================

        delete_chat(
            driver_1,
            "Device 1"
        )

        # ====================================================
        # TEST PASSED
        # ====================================================

        print()
        print("=" * 70)
        print("TEST PASSED")
        print("=" * 70)

        print()
        print("Message successfully:")
        print("  1. Sent from Device 1")
        print("  2. Verified on Device 1")
        print("  3. Received on Device 2")
        print("  4. Verified on Device 2")
        print("  5. Chat deleted on Device 2")
        print("  6. Delete confirmed on Device 2")
        print("  7. Chat deleted on Device 1")
        print("  8. Delete confirmed on Device 1")

        print()
        print("HeadSpin recorder/capture:")
        print("  Device 1 - ENABLED")
        print("  Device 2 - ENABLED")

    except Exception as e:

        print()
        print("=" * 70)
        print("TEST FAILED")
        print("=" * 70)

        print()
        print("Error:")
        print(e)

    finally:

        # ====================================================
        # CLOSE DEVICE 1
        # ====================================================

        print()
        print(
            "Closing Device 1 session..."
        )

        try:

            driver_1.quit()

            print(
                "Device 1 session closed."
            )

        except Exception as e:

            print(
                "Device 1 quit error:",
                e
            )

        # ====================================================
        # CLOSE DEVICE 2
        # ====================================================

        print()
        print(
            "Closing Device 2 session..."
        )

        try:

            driver_2.quit()

            print(
                "Device 2 session closed."
            )

        except Exception as e:

            print(
                "Device 2 quit error:",
                e
            )

        print()
        print("=" * 70)
        print("ALL SESSIONS CLOSED")
        print("=" * 70)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()