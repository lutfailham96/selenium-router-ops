from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import json
import sys
# import time

class F670L:
    def __init__(self, driver, ip_router, username, password):
        self.driver = driver
        self.ip_router = ip_router
        self.username = username
        self.password = password
        self.router_name = "F607L"

    def get_homepage(self):
        driver.get(f"http://{self.ip_router}/")

    def do_login(self):
        # credentials
        username = self.username
        password = self.password

        # fill form login
        username_field = self.driver.find_element(By.ID, "Frm_Username")
        password_field = self.driver.find_element(By.ID, "Frm_Password")
        username_field.send_keys(username)
        password_field.send_keys(password)

        # submit login
        login_button = self.driver.find_element(By.ID, "LoginId")
        login_button.click()

    def get_ssid_security(self, essid_id, encryption_type_id, passphrase_id):
        essid_field = self.driver.find_element(By.ID, essid_id)
        essid_value = essid_field.get_attribute("value")
        encryption_type_option = self.driver.find_element(By.ID, encryption_type_id)
        encryption_type_value = encryption_type_option.get_attribute("value")
        passphrase_value = ""
        if encryption_type_value != "No Security":
            passphrase_field = self.driver.find_element(By.ID, passphrase_id)
            passphrase_value = passphrase_field.get_attribute("value")
        return {
            "essid": essid_value,
            "passphrase": passphrase_value,
        }

    def get_wifi_info(self):
        # click localnet menu
        localnet_present = EC.presence_of_element_located((By.ID, "localnet"))
        WebDriverWait(self.driver, 10).until(localnet_present)
        localnet_menu = self.driver.find_element(By.ID, "localnet")
        localnet_menu.click()

        # click wlan menu
        wlan_present = EC.presence_of_element_located((By.ID, "wlanConfig"))
        WebDriverWait(self.driver, 10).until(wlan_present)
        wlan_menu = self.driver.find_element(By.ID, "wlanConfig")
        wlan_menu.click()

        # ssid name & passowrd
        # click ssid menu
        ssid_present = EC.presence_of_element_located((By.ID, "WLANSSIDConf"))
        WebDriverWait(self.driver, 10).until(ssid_present)
        ssid_menu = self.driver.find_element(By.ID, "WLANSSIDConf")
        ssid_menu.click()
        # get essid & passphrase
        wifi2ghz = {}
        for i in range(4):
            wifi2ghz_data = self.get_ssid_security(f"ESSID:{i}", f"EncryptionType:{i}", f"KeyPassphrase:{i}")
            wifi2ghz[f"ssid{i+1}Name"] = wifi2ghz_data["essid"]
            wifi2ghz[f"ssid{i+1}Password"] = wifi2ghz_data["passphrase"]
        wifi5ghz = {}
        for i in range(4, 8):
            wifi5ghz_data = self.get_ssid_security(f"ESSID:{i}", f"EncryptionType:{i}", f"KeyPassphrase:{i}")
            wifi5ghz[f"ssid{i-3}Name"] = wifi5ghz_data["essid"]
            wifi5ghz[f"ssid{i-3}Password"] = wifi5ghz_data["passphrase"]
        data = {
            "ipRouter": self.ip_router,
            "routerName": self.router_name,
            "wifi2ghz": wifi2ghz,
            "wifi5ghz": wifi5ghz,
        }
        return json.dumps(data, separators=(',', ':'))

class F609:
    def __init__(self, driver, ip_router, username, password):
        self.driver = driver
        self.ip_router = ip_router
        self.username = username
        self.password = password
        self.router_name = "F609"

    def get_homepage(self):
        driver.get(f"http://{self.ip_router}/")

    def do_login(self):
        # credentials
        username = self.username
        password = self.password

        # fill form login
        username_field = self.driver.find_element(By.ID, "Frm_Username")
        password_field = self.driver.find_element(By.ID, "Frm_Password")
        username_field.send_keys(username)
        password_field.send_keys(password)

        # submit login
        login_button = self.driver.find_element(By.ID, "LoginId")
        login_button.click()

    def get_essid(self, ssid_option_id, ssid_dropdown_value, ssid_input_id):
        ssid_select = self.driver.find_element(By.ID, ssid_option_id)
        ssid_dropdown = Select(ssid_select)
        ssid_dropdown.select_by_value(ssid_dropdown_value)
        ssid_input_present = EC.presence_of_element_located((By.ID, ssid_input_id))
        WebDriverWait(self.driver, 10).until(ssid_input_present)
        ssid_input_field = self.driver.find_element(By.ID, ssid_input_id)
        ssid_input_value = ssid_input_field.get_attribute("value")
        return ssid_input_value

    def get_security(self, ssid_option_id, ssid_dropdown_value, encryption_type_id):
        ssid_select = driver.find_element(By.ID, ssid_option_id)
        ssid_dropdown = Select(ssid_select)
        ssid_dropdown.select_by_value(ssid_dropdown_value)
        encryption_type_option = self.driver.find_element(By.ID, encryption_type_id)
        encryption_type_value = encryption_type_option.get_attribute("value")
        passphrase_value = ""
        if encryption_type_value != "Open System":
            password_present = EC.presence_of_element_located((By.ID, encryption_type_id))
            WebDriverWait(self.driver, 10).until(password_present)
            passphrase_field = self.driver.find_element(By.ID, encryption_type_id)
            passphrase_value = passphrase_field.get_attribute("value")
        return passphrase_value

    def get_wifi_info(self):
        # switch to main frame
        self.driver.switch_to.frame(1)

        # click network menu
        network_present = EC.presence_of_element_located((By.ID, 'mmNet'))
        WebDriverWait(self.driver, 10).until(network_present)
        network_menu = self.driver.find_element(By.ID, "mmNet")
        network_menu.click()

        # click wlan menu
        wlan_present = EC.presence_of_element_located((By.ID, "smWLAN"))
        WebDriverWait(self.driver, 10).until(wlan_present)
        wlan_menu = self.driver.find_element(By.ID, "smWLAN")
        wlan_menu.click()

        wifi2ghz = {}
        # get essid
        # click ssid menu
        ssid_present = EC.presence_of_element_located((By.ID, "ssmWLANMul"))
        WebDriverWait(self.driver, 10).until(ssid_present)
        ssid_menu = self.driver.find_element(By.ID, "ssmWLANMul")
        ssid_menu.click()
        for i in range(4):
            wifi2ghz[f"ssid{i+1}Name"] = self.get_essid("Frm_SSID_SET", f"IGD.LD1.WLAN{i+1}", "Frm_ESSID")
        # get passphrase
        # click security menu
        security_present = EC.presence_of_element_located((By.ID, "ssmWLANSec"))
        WebDriverWait(self.driver, 10).until(security_present)
        security_menu = self.driver.find_element(By.ID, "ssmWLANSec")
        security_menu.click()
        for i in range(4):
            wifi2ghz[f"ssid{i+1}Password"] = self.get_security("Frm_SSID_SET", f"IGD.LD1.WLAN{i+1}", "Frm_KeyPassphrase")
        reordered_wifi2ghz = {
            "ssid1Name": wifi2ghz["ssid1Name"],
            "ssid1Password": wifi2ghz["ssid1Password"],
            "ssid2Name": wifi2ghz["ssid2Name"],
            "ssid2Password": wifi2ghz["ssid2Password"],
            "ssid3Name": wifi2ghz["ssid3Name"],
            "ssid3Password": wifi2ghz["ssid3Password"],
            "ssid4Name": wifi2ghz["ssid4Name"],
            "ssid4Password": wifi2ghz["ssid4Password"]
        }
        data = {
            "ipRouter": self.ip_router,
            "routerName": self.router_name,
            "wifi2ghz": reordered_wifi2ghz,
            "wifi5ghz": "null",
        }
        return json.dumps(data, separators=(',', ':'))

# Automatically install the latest chromedriver
chromedriver_autoinstaller.install()
# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# Create a new instance of the Chrome driver
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

def detect_router(ip_router):
    driver.get(f"http://{ip_router}/")
    driver_title = driver.title
    if driver_title == "F670L":
        return driver_title
    if driver_title == "F609":
        return driver_title
    return driver_title

try:

    if len(sys.argv) > 1:
        ip_router = sys.argv[1]
    else:
        print("No IP provided!")
        exit(1)
    username = "admin"
    password = "Jaringanku!23456"
    router = detect_router(ip_router)
    if router == "F670L":
        f670l = F670L(driver, ip_router, username, password)
        f670l.get_homepage()
        f670l.do_login()
        print(f670l.get_wifi_info())
    elif router == "F609":
        f609 = F609(driver, ip_router, username, password)
        f609.get_homepage()
        f609.do_login()
        print(f609.get_wifi_info())
    else:
        data = {
            "ipRouter": ip_router,
            "status": "error",
            "message": f"Router {router} not supported yet"
        }

    # check last screen
    # time.sleep(10)
except Exception as e:
    print("An error occurred:", e)


# Close the browser
driver.quit()
