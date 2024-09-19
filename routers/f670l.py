from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

class F670L:
    def __init__(self, driver: WebDriver, router_ip: str, router_username: str, router_password: str) -> None:
        self.driver = driver
        self.router_ip = router_ip
        self.router_username = router_username
        self.router_password = router_password
        self.router_name = "F670L"

    def get_homepage(self) -> None:
        self.driver.get(f"http://{self.router_ip}/")

    def do_login(self) -> None:
        # Fill form login
        username_field = self.driver.find_element(By.ID, "Frm_Username")
        password_field = self.driver.find_element(By.ID, "Frm_Password")
        username_field.send_keys(self.router_username)
        password_field.send_keys(self.router_password)

        # Submit login
        login_button = self.driver.find_element(By.ID, "LoginId")
        login_button.click()

    def get_ssid_security(self, essid_id: str, encryption_type_id: str, passphrase_id: str) -> dict:
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

    def get_wifi_info(self) -> dict:
        # Click localnet menu
        localnet_present = EC.presence_of_element_located((By.ID, "localnet"))
        WebDriverWait(self.driver, 10).until(localnet_present)
        self.driver.find_element(By.ID, "localnet").click()

        # Click wlan menu
        wlan_present = EC.presence_of_element_located((By.ID, "wlanConfig"))
        WebDriverWait(self.driver, 10).until(wlan_present)
        self.driver.find_element(By.ID, "wlanConfig").click()

        # Get SSID name & password
        wifi2ghz = {}
        ssid_present = EC.presence_of_element_located((By.ID, "WLANSSIDConf"))
        WebDriverWait(self.driver, 10).until(ssid_present)
        self.driver.find_element(By.ID, "WLANSSIDConf").click()

        for i in range(4):
            wifi2ghz_data = self.get_ssid_security(f"ESSID:{i}", f"EncryptionType:{i}", f"KeyPassphrase:{i}")
            wifi2ghz[f"ssid{i + 1}Name"] = wifi2ghz_data["essid"]
            wifi2ghz[f"ssid{i + 1}Password"] = wifi2ghz_data["passphrase"]

        wifi5ghz = {}
        for i in range(4, 8):
            wifi5ghz_data = self.get_ssid_security(f"ESSID:{i}", f"EncryptionType:{i}", f"KeyPassphrase:{i}")
            wifi5ghz[f"ssid{i - 3}Name"] = wifi5ghz_data["essid"]
            wifi5ghz[f"ssid{i - 3}Password"] = wifi5ghz_data["passphrase"]

        data = {
            "ipRouter": self.router_ip,
            "routerName": self.router_name,
            "wifi2ghz": wifi2ghz,
            "wifi5ghz": wifi5ghz,
        }

        return json.dumps(data, separators=(',', ':'))

    def reboot(self) -> None:
        pass
