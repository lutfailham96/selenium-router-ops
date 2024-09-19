from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import json
from routers.common import wait_for_download_to_complete, rename_downloaded_file

class F609:
    def __init__(self, driver: WebDriver, router_ip: str, router_username: str, router_password: str) -> None:
        self.driver = driver
        self.router_ip = router_ip
        self.router_username = router_username
        self.router_password = router_password
        self.router_name = "F609"

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

    def get_essid(self, ssid_option_id: str, ssid_dropdown_value: str, ssid_input_id: str) -> str:
        ssid_select = self.driver.find_element(By.ID, ssid_option_id)
        ssid_dropdown = Select(ssid_select)
        ssid_dropdown.select_by_value(ssid_dropdown_value)

        ssid_input_present = EC.presence_of_element_located((By.ID, ssid_input_id))
        WebDriverWait(self.driver, 10).until(ssid_input_present)

        ssid_input_field = self.driver.find_element(By.ID, ssid_input_id)
        return ssid_input_field.get_attribute("value")

    def get_security(self, ssid_option_id: str, ssid_dropdown_value: str, encryption_type_id: str, passphrase_id: str) -> str:
        ssid_select = self.driver.find_element(By.ID, ssid_option_id)
        ssid_dropdown = Select(ssid_select)
        ssid_dropdown.select_by_value(ssid_dropdown_value)

        encryption_type_option = self.driver.find_element(By.ID, encryption_type_id)
        encryption_type_value = encryption_type_option.get_attribute("value")

        passphrase_value = ""
        if encryption_type_value != "Open System":
            passphrase_present = EC.presence_of_element_located((By.ID, passphrase_id))
            WebDriverWait(self.driver, 10).until(passphrase_present)

            passphrase_field = self.driver.find_element(By.ID, passphrase_id)
            passphrase_value = passphrase_field.get_attribute("value")

        return passphrase_value

    def get_device_info(self) -> dict:
        # Start page
        self.driver.get(f"http://{self.router_ip}/start.ghtml")

        # Switch to main frame
        self.driver.switch_to.frame(1)

        data = {}

        # Table status
        table_present = EC.presence_of_element_located((By.ID, "TABLE_DEV"))
        WebDriverWait(self.driver, 10).until(table_present)
        data["ipRouter"] = self.router_ip
        data["model"] = self.driver.find_element(By.ID, "Frm_ModelName").text
        data["serial"] = self.driver.find_element(By.ID, "Frm_SerialNumber").text
        data["hardwareVersion"] = self.driver.find_element(By.ID, "Frm_HardwareVer").text
        data["softwareVersion"] = self.driver.find_element(By.ID, "Frm_SoftwareVer").text
        data["bootLoaderVersion"] = self.driver.find_element(By.ID, "Frm_BootVer").text
        data["ponSerial"] = self.driver.find_element(By.ID, "Frm_PonSerialNumber").text
        data["batchNumber"] = self.driver.find_element(By.ID, "Frm_SoftwareVerExtent").text

        ui_present = EC.presence_of_element_located((By.ID, "smLanStatu"))
        WebDriverWait(self.driver, 10).until(ui_present)
        self.driver.find_element(By.ID, "smLanStatu").click()

        wlan_present = EC.presence_of_element_located((By.ID, "ssmWLAN"))
        WebDriverWait(self.driver, 10).until(wlan_present)
        self.driver.find_element(By.ID, "ssmWLAN").click()

        table_present = EC.presence_of_element_located((By.ID, "tbl_basic_info"))
        WebDriverWait(self.driver, 10).until(table_present)

        for i in range(4):
            data[f"macWlan{i+1}"] = self.driver.find_element(By.ID, f"td_Bssid{i}").text

        return json.dumps(data, separators=(',', ':'))

    def get_wifi_info(self) -> dict:
        # Switch to main frame
        self.driver.switch_to.frame(1)

        # Click network menu
        network_present = EC.presence_of_element_located((By.ID, 'mmNet'))
        WebDriverWait(self.driver, 10).until(network_present)
        self.driver.find_element(By.ID, "mmNet").click()

        # Click wlan menu
        wlan_present = EC.presence_of_element_located((By.ID, "smWLAN"))
        WebDriverWait(self.driver, 10).until(wlan_present)
        self.driver.find_element(By.ID, "smWLAN").click()

        wifi2ghz = {}
        # Get essid
        ssid_present = EC.presence_of_element_located((By.ID, "ssmWLANMul"))
        WebDriverWait(self.driver, 10).until(ssid_present)
        self.driver.find_element(By.ID, "ssmWLANMul").click()

        for i in range(4):
            wifi2ghz[f"ssid{i + 1}Name"] = self.get_essid("Frm_SSID_SET", f"IGD.LD1.WLAN{i + 1}", "Frm_ESSID")

        # Get passphrase
        security_present = EC.presence_of_element_located((By.ID, "ssmWLANSec"))
        WebDriverWait(self.driver, 10).until(security_present)
        self.driver.find_element(By.ID, "ssmWLANSec").click()

        for i in range(4):
            wifi2ghz[f"ssid{i + 1}Password"] = self.get_security("Frm_SSID_SET", f"IGD.LD1.WLAN{i + 1}", "Frm_Authentication", "Frm_KeyPassphrase")

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
            "ipRouter": self.router_ip,
            "routerName": self.router_name,
            "wifi2ghz": reordered_wifi2ghz,
            "wifi5ghz": None,
        }

        return json.dumps(data, separators=(',', ':'))

    def reboot(self) -> None:
        # Switch to main frame
        self.driver.switch_to.frame(1)

        # Router management menu
        management_present = EC.presence_of_element_located((By.ID, "Fnt_mmManager"))
        WebDriverWait(self.driver, 10).until(management_present)
        self.driver.find_element(By.ID, "Fnt_mmManager").click()

        # System management menu
        smanagement_present = EC.presence_of_element_located((By.ID, "smSysMgr"))
        WebDriverWait(self.driver, 10).until(smanagement_present)
        self.driver.find_element(By.ID, "smSysMgr").click()

        # Reboot router
        reboot_present = EC.presence_of_element_located((By.ID, "Submit1"))
        WebDriverWait(self.driver, 10).until(reboot_present)
        self.driver.find_element(By.ID, "Submit1").click()

        confirm_present = EC.presence_of_element_located((By.ID, "msgconfirmb"))
        WebDriverWait(self.driver, 10).until(confirm_present)
        self.driver.find_element(By.ID, "msgconfirmb").click()

    def download_user_config(self) -> None:
        # Switch to main frame
        self.driver.switch_to.frame(1)

        # Router management menu
        management_present = EC.presence_of_element_located((By.ID, "Fnt_mmManager"))
        WebDriverWait(self.driver, 10).until(management_present)
        self.driver.find_element(By.ID, "Fnt_mmManager").click()

        # System management menu
        smanagement_present = EC.presence_of_element_located((By.ID, "smSysMgr"))
        WebDriverWait(self.driver, 10).until(smanagement_present)
        self.driver.find_element(By.ID, "smSysMgr").click()


        # User configuration management menu
        umanagement_present = EC.presence_of_element_located((By.ID, "ssmConfMgr"))
        WebDriverWait(self.driver, 10).until(umanagement_present)
        self.driver.find_element(By.ID, "ssmConfMgr").click()

        # Download user config
        download_present = EC.presence_of_element_located((By.ID, "download"))
        WebDriverWait(self.driver, 10).until(download_present)
        self.driver.find_element(By.ID, "download").click()

        # Rename config file
        original_filename = "config.bin"
        downloaded_file = wait_for_download_to_complete(original_filename)
        if downloaded_file:
            config_file = rename_downloaded_file(downloaded_file, f"{self.router_ip}-{self.router_name}-config.bin")
            print(f"User configuration downloaded to: {config_file}")
        else:
            print("Download failed or file not found")