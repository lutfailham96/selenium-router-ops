from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

def setup_webdriver(enable_gui: bool) -> WebDriver:
    # Automatically install the latest chromedriver
    chromedriver_autoinstaller.install()
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if not enable_gui:
        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    # Create a new instance of the Chrome driver
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

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
