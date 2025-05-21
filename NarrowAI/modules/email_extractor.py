# modules/email_extractor.py

import re
import requests

def extract_emails(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@" + re.escape(domain), response.text, re.IGNORECASE)
        return sorted(set(emails))
    except requests.RequestException:
        return []
