#!/usr/bin/env python3
import socket
import ssl
import sys
from datetime import datetime, timezone


def check_ssl_expiry(domain, days_before=7):
    context = ssl.create_default_context()

    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()

    expiry_date = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
    remaining_days = (
        expiry_date - datetime.now(timezone.utc).replace(tzinfo=None)
    ).days

    print(f"Domain: {domain}")
    print(f"Remaining days: {remaining_days}")
    print(f"Days before: {days_before}")


check_ssl_expiry(sys.argv[1])
