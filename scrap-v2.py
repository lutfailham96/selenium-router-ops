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

    def get_ssid_security(self, essidID, encryptionTypeID, passphraseID):
        essid_field = self.driver.find_element(By.ID, essidID)
        essid_value = essid_field.get_attribute("value")
        encryption_type_option = self.driver.find_element(By.ID, encryptionTypeID)
        encryption_type_value = encryption_type_option.get_attribute("value")
        passphrase_value = ""
        if encryption_type_value != "No Security":
            passphrase_field = self.driver.find_element(By.ID, passphraseID)
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
            wifi2ghz[f"ssid{i}Name"] = wifi2ghz_data["essid"]
            wifi2ghz[f"ssid{i}Password"] = wifi2ghz_data["passphrase"]
        # ssid5ghz1
        auth_type = self.driver.find_element(By.ID, "EncryptionType:4")
        auth_type_value = auth_type.get_attribute("value")
        ssid5ghz1_field = self.driver.find_element(By.ID, "ESSID:4")
        ssid5ghz1_text = ssid5ghz1_field.get_attribute("value")
        if auth_type_value != "No Security":
            password5ghz1_field = self.driver.find_element(By.ID, "KeyPassphrase:4")
            password5ghz1_text = password5ghz1_field.get_attribute("value")
        else:
            password2ghz1_text = ""
        # ssid5ghz2
        auth_type = self.driver.find_element(By.ID, "EncryptionType:5")
        auth_type_value = auth_type.get_attribute("value")
        ssid5ghz2_field = self.driver.find_element(By.ID, "ESSID:5")
        ssid5ghz2_text = ssid5ghz2_field.get_attribute("value")
        if auth_type_value != "No Security":
            password5ghz2_field = self.driver.find_element(By.ID, "KeyPassphrase:5")
            password5ghz2_text = password5ghz2_field.get_attribute("value")
        else:
            password2ghz2_text = ""
        # ssid5ghz3
        auth_type = self.driver.find_element(By.ID, "EncryptionType:6")
        auth_type_value = auth_type.get_attribute("value")
        ssid5ghz3_field = self.driver.find_element(By.ID, "ESSID:6")
        ssid5ghz3_text = ssid5ghz3_field.get_attribute("value")
        if auth_type_value != "No Security":
            password5ghz3_field = self.driver.find_element(By.ID, "KeyPassphrase:6")
            password5ghz3_text = password5ghz3_field.get_attribute("value")
        else:
            password2ghz3_text = ""
        # ssid5ghz4
        auth_type = self.driver.find_element(By.ID, "EncryptionType:7")
        auth_type_value = auth_type.get_attribute("value")
        ssid5ghz4_field = self.driver.find_element(By.ID, "ESSID:7")
        ssid5ghz4_text = ssid5ghz4_field.get_attribute("value")
        if auth_type_value != "No Security":
            password5ghz4_field = self.driver.find_element(By.ID, "KeyPassphrase:7")
            password5ghz4_text = password5ghz4_field.get_attribute("value")
        else:
            password5ghz4_text = ""
        data = {
            "ipRouter": self.ip_router,
            "routerName": self.router_name,
            "wifi2ghz": wifi2ghz,
            "wifi5ghz": {
                "ssid1Name": ssid5ghz1_text,
                "ssid1Password": password5ghz1_text,
                "ssid2Name": ssid5ghz2_text,
                "ssid1Password": password5ghz2_text,
                "ssid3Name": ssid5ghz3_text,
                "ssid3Password": password5ghz3_text,
                "ssid4Name": ssid5ghz4_text,
                "ssid4Password": password5ghz4_text,
            },
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

        # ssid name
        # click ssid menu
        ssid_present = EC.presence_of_element_located((By.ID, "ssmWLANMul"))
        WebDriverWait(self.driver, 10).until(ssid_present)
        ssid_menu = self.driver.find_element(By.ID, "ssmWLANMul")
        ssid_menu.click()
        # ssid1
        ssid_present = EC.presence_of_element_located((By.ID, "Frm_ESSID"))
        WebDriverWait(self.driver, 10).until(ssid_present)
        ssid1_field = self.driver.find_element(By.ID, "Frm_ESSID")
        ssid1_text = ssid1_field.get_attribute("value")
        # ssid2
        ssid_select = driver.find_element(By.ID, 'Frm_SSID_SET')
        ssid_dropdown = Select(ssid_select)
        ssid_dropdown.select_by_value("IGD.LD1.WLAN2")
        ssid_present = EC.presence_of_element_located((By.ID, "Frm_ESSID"))
        WebDriverWait(self.driver, 10).until(ssid_present)
        ssid2_field = self.driver.find_element(By.ID, "Frm_ESSID")
        ssid2_text = ssid2_field.get_attribute("value")
        # ssid3
        ssid_select = driver.find_element(By.ID, 'Frm_SSID_SET')
        ssid_dropdown = Select(ssid_select)
        ssid_dropdown.select_by_value("IGD.LD1.WLAN3")
        ssid_present = EC.presence_of_element_located((By.ID, "Frm_ESSID"))
        WebDriverWait(self.driver, 10).until(ssid_present)
        ssid3_field = self.driver.find_element(By.ID, "Frm_ESSID")
        ssid3_text = ssid3_field.get_attribute("value")
        # ssid4
        ssid_select = driver.find_element(By.ID, 'Frm_SSID_SET')
        ssid_dropdown = Select(ssid_select)
        ssid_dropdown.select_by_value("IGD.LD1.WLAN4")
        ssid_present = EC.presence_of_element_located((By.ID, "Frm_ESSID"))
        WebDriverWait(self.driver, 10).until(ssid_present)
        ssid4_field = self.driver.find_element(By.ID, "Frm_ESSID")
        ssid4_text = ssid4_field.get_attribute("value")

        # ssid security
        # click security menu
        security_present = EC.presence_of_element_located((By.ID, "ssmWLANSec"))
        WebDriverWait(self.driver, 10).until(security_present)
        security_menu = self.driver.find_element(By.ID, "ssmWLANSec")
        security_menu.click()
        # ssid1
        auth_type = self.driver.find_element(By.ID, "Frm_Authentication")
        auth_type_value = auth_type.get_attribute("value")
        if auth_type_value != "Open System":
            password_present = EC.presence_of_element_located((By.ID, "Frm_KeyPassphrase"))
            WebDriverWait(self.driver, 10).until(password_present)
            password1_field = self.driver.find_element(By.ID, "Frm_KeyPassphrase")
            password1_text = password1_field.get_attribute("value")
        else:
            password1_text = ""
        # ssid2
        ssid_select = driver.find_element(By.ID, 'Frm_SSID_SET')
        ssid_dropdown = Select(ssid_select)
        ssid_dropdown.select_by_value("IGD.LD1.WLAN2")
        auth_type = self.driver.find_element(By.ID, "Frm_Authentication")
        auth_type_value = auth_type.get_attribute("value")
        if auth_type_value != "Open System":
            password_present = EC.presence_of_element_located((By.ID, "Frm_KeyPassphrase"))
            WebDriverWait(self.driver, 10).until(password_present)
            password2_field = self.driver.find_element(By.ID, "Frm_KeyPassphrase")
            password2_text = password2_field.get_attribute("value")
        else:
            password2_text = ""
        # ssid3
        ssid_select = driver.find_element(By.ID, 'Frm_SSID_SET')
        ssid_dropdown = Select(ssid_select)
        ssid_dropdown.select_by_value("IGD.LD1.WLAN3")
        auth_type = self.driver.find_element(By.ID, "Frm_Authentication")
        auth_type_value = auth_type.get_attribute("value")
        if auth_type_value != "Open System":
            password_present = EC.presence_of_element_located((By.ID, "Frm_KeyPassphrase"))
            WebDriverWait(self.driver, 10).until(password_present)
            password3_field = self.driver.find_element(By.ID, "Frm_KeyPassphrase")
            password3_text = password3_field.get_attribute("value")
        else:
            password3_text = ""
        # ssid4
        ssid_select = driver.find_element(By.ID, 'Frm_SSID_SET')
        ssid_dropdown = Select(ssid_select)
        ssid_dropdown.select_by_value("IGD.LD1.WLAN4")
        auth_type = self.driver.find_element(By.ID, "Frm_Authentication")
        auth_type_value = auth_type.get_attribute("value")
        if auth_type_value != "Open System":
            password_present = EC.presence_of_element_located((By.ID, "Frm_KeyPassphrase"))
            WebDriverWait(self.driver, 10).until(password_present)
            password4_field = self.driver.find_element(By.ID, "Frm_KeyPassphrase")
            password4_text = password4_field.get_attribute("value")
        else:
            password4_text = ""
        data = {
            "ipRouter": self.ip_router,
            "routerName": self.router_name,
            "wifi2ghz": {
                "ssid1Name": ssid1_text,
                "ssid1Password": password1_text,
                "ssid2Name": ssid2_text,
                "ssid1Password": password2_text,
                "ssid3Name": ssid3_text,
                "ssid3Password": password3_text,
                "ssid4Name": ssid4_text,
                "ssid4Password": password4_text,
            },
            "wifi5ghz": "null",
        }
        return json.dumps(data, separators=(',', ':'))

# Automatically install the latest chromedriver
chromedriver_autoinstaller.install()
# Set up Chrome options
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
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
