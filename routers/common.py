import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

download_dir = os.path.join(os.getcwd(), 'downloads')

def setup_webdriver(allowed_insecure_ip: str, enable_gui: bool) -> WebDriver:
    # Automatically install the latest chromedriver
    chromedriver_autoinstaller.install()
    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,       # Set the download directory
        "download.prompt_for_download": False,            # Disable download prompts
        "directory_upgrade": True,                        # Automatically overwrite the download directory
        "safebrowsing.enabled": True                      # Enable safe browsing
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument(f"--unsafely-treat-insecure-origin-as-secure=http://{allowed_insecure_ip},https://{allowed_insecure_ip}")
    if not enable_gui:
        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    # Create a new instance of the Chrome driver
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def wait_for_download_to_complete(file_name: str, timeout: int=30):
    os.makedirs(download_dir, exist_ok=True)
    end_time = time.time() + timeout
    while time.time() < end_time:
        # Check if the target file exists and no temporary file is present
        file_path = os.path.join(download_dir, file_name)
        temp_file_path = file_path + '.crdownload'
        if os.path.exists(file_path) and not os.path.exists(temp_file_path):
            return file_path
        time.sleep(1)
    return None

def rename_downloaded_file(old_file_name: str, new_file_name: str) -> str:
    new_file = os.path.join(download_dir, new_file_name)
    os.rename(old_file_name, new_file)
    return new_file

def detect_router(driver: WebDriver, router_ip: str) -> str:
    driver.get(f"http://{router_ip}/")
    driver_title = driver.title
    if driver_title == "F670L":
        return "F670L"
    if driver_title == "F609" or driver_title == "ZXHN F609":
        return "F609"
    return driver_title

def proceed_command(router: any, command: str) -> None:
    if command == 'reboot':
        router.get_homepage()
        router.do_login()
        router.reboot()
    elif command == 'wifi_info':
        router.get_homepage()
        router.do_login()
        print(router.get_wifi_info())
    elif command == 'dl_config':
        router.get_homepage()
        router.do_login()
        router.download_user_config()
    elif command == 'device_info':
        router.get_homepage()
        router.do_login()
        print(router.get_device_info())

