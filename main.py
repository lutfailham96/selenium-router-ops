import argparse
import json
from routers.f670l import F670L
from routers.f609 import F609
from routers.common import detect_router, setup_webdriver, proceed_command

def main() -> None:
    parser = argparse.ArgumentParser(description='Router management script.')
    parser.add_argument('-u', '--username', required=True, help='Router username')
    parser.add_argument('-p', '--password', required=True, help='Router password')
    parser.add_argument('-ip', '--router_ip', required=True, help='Router IP address')
    parser.add_argument('-c', '--command', required=True, default='wifi_info', choices=['reboot', 'wifi_info', 'dl_config'], help='Command to execute')
    parser.add_argument('-g', '--gui', required=False, default=False, help='Enable GUI webdriver')
    args = parser.parse_args()

    router_ip = args.router_ip
    router_username = args.username
    router_password = args.password
    router_command = args.command
    enable_gui = args.gui

    # setup webdriver
    driver = setup_webdriver(router_ip, enable_gui)

    router_name = detect_router(driver, router_ip)
    if router_name == "F670L":
        f670l = F670L(driver, router_ip, router_username, router_password)
        proceed_command(f670l, router_command)
    elif router_name == "F609":
        f609 = F609(driver, router_ip, router_username, router_password)
        proceed_command(f609, router_command)
    else:
        data = {
            "ipRouter": router_ip,
            "status": "error",
            "message": "Router not supported yet",
        }
        print(json.dumps(data, separators=(',', ':')))

    # close webdriver
    driver.quit()

if __name__ == "__main__":
    main()
