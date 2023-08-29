import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

visits_counter = 0

url_list = [
    'https://youtube.com',
    # ... (other URLs)
    'https://kyu.ac.ke',
]

# List of proxy URLs
proxies = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt"
]

# Combine proxy lists into a single list
all_proxies = []

for proxy in proxies:
    response = requests.get(proxy)
    if response.status_code == 200:
        proxy_lines = response.text.split("\n")
        all_proxies.extend(proxy_lines)

# Filter out empty lines and duplicates
proxies_list = list(filter(None, all_proxies))
proxies_list = list(set(proxies_list))

# Configure Chrome to open URLs in new tabs
chrome_options = Options()
chrome_options.add_argument("--new-tab")

# Loop through each proxy in the list
for pro in proxies_list:
    # Check the validity of the proxy
    try:
        requests.get("https://www.google.com/", proxies={"http": pro, "https": pro}, timeout=3)
    except:
        print(f"Skipping proxy {pro} (not working)")
        continue

    # Configure Chrome to use the proxy
    chrome_options = Options()
    chrome_options.add_argument('--new-tab')
    chrome_options.add_argument('--proxy-server=%s' % pro)
    chrome_options.add_argument('--headless')
    chrome = webdriver.Chrome(options=chrome_options)

    # Visit each website only once
    for url in url_list:
        chrome.execute_script("window.open('{}', '_blank')".format(url))
        visits_counter += 1
        time.sleep(7)
        print("Visited {} pages using proxies".format(visits_counter))
    time.sleep(70)

    chrome.quit()
