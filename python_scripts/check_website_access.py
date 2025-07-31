#!/usr/bin/env python3
import requests
from ping3 import ping


# Check website by HTTP request
def check_website(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"Site {url} available.")
        else:
            print(f"Site {url} return error code: {response.status_code}")
    except requests.exceptions.RequestException as ex:
        print(f"Connection error {url}: {ex}")


# Check IP (ping)
def check_ping(host):
    response = ping(host)
    if response:
        print(f"{host} available: ping {response * 1000:.2f} ms")
    else:
        print(f"{host} not available")


check_website("https://example.com")
check_ping("8.8.8.8")  # Ping to DNS Google
