# selenium-router-ops

A Selenium-based automation tool for managing and scraping WiFi information from your router. This project allows users to perform various administrative tasks seamlessly through automation.

## Features

- **WiFi Information Scraping**: Easily retrieve information about connected devices and WiFi settings.
- **Router Reboot**: Automate the process of rebooting your router to maintain optimal performance.
- **Customizable Scripts**: Modify and extend the functionality to meet your specific network management needs.

## Requirements

- Python 3.x
- Selenium
- WebDriver for your chosen browser (e.g., ChromeDriver for Chrome, GeckoDriver for Firefox)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/lutfailham96/selenium-router-ops.git
   cd selenium-router-ops

2. **Install Required Packages**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Download and Set Up WebDriver**:

    Ensure you download the appropriate WebDriver for your browser and add it to your system's PATH.

## Example Usage

1. **Get wifi information**:

    ```bash
    python3 main.py -u 'admin' -p 'admin' -ip 192.168.1.1 -c wifi_info
    ```

2. **Reboot router**:

    ```bash
    python3 main.py -u 'admin' -p 'admin' -ip 192.168.1.1 -c reboot
    ```

## Contributing

Contributions are welcome! If you have ideas for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the GPL v3 License. See the LICENSE file for details.

## Acknowledgements

- Selenium Documentation for guidance on automation tasks.
- Special thanks to the open-source community for tools and libraries that made this project possible.
