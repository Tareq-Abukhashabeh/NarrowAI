# modules/subdomain_finder.py

import requests

def find_subdomains(domain, wordlist):
    found = []
    for word in wordlist:
        sub = f"{word.strip()}.{domain}"
        try:
            response = requests.get(f"http://{sub}", timeout=2)
            if response.status_code < 400:
                found.append(sub)
        except requests.RequestException:
            continue
    return sorted(set(found))
