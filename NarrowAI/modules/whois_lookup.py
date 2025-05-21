# modules/whois_lookup.py

import whois
import re

def get_whois(domain):
    try:
        w = whois.whois(domain)
        output = []

        if w.domain_name:
            output.append(f"Domain Name: {w.domain_name}")
        if w.registrar:
            output.append(f"Registrar: {w.registrar}")
        if w.creation_date:
            output.append(f"Creation Date: {w.creation_date}")
        if w.expiration_date:
            output.append(f"Expiration Date: {w.expiration_date}")
        if w.emails:
            if isinstance(w.emails, list):
                output.append(f"Registrant Emails: {', '.join(set(w.emails))}")
            else:
                output.append(f"Registrant Email: {w.emails}")
        if hasattr(w, 'dnssec') and w.dnssec:
            output.append(f"DNSSEC: {w.dnssec}")

        return '\n'.join(output) if output else "No WHOIS info found."

    except Exception as e:
        return f"WHOIS lookup failed: {e}"
