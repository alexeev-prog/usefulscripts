#!/usr/bin/env python3
import ssl
import socket
from datetime import datetime


def check_ssl_expiry(domain, days_before=7):
    context = ssl.create_default_context()

    with socket.create_connection((domain, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()

    expiry_date = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
    remaining_days = (expiry_date - datetime.utcnow()).days

    if remaining_days <= days_before:
        print(f"SSL Cert of {domain} expires in {remaining_days} days!")


check_ssl_expiry("example.com")
