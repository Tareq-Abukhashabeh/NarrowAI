# modules/dns_lookup.py

import dns.resolver

def get_dns_records(domain):
    records = {}
    record_types = ["A", "AAAA", "MX", "NS", "CNAME", "TXT"]

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            records[rtype] = [str(rdata).strip('"') for rdata in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.resolver.Timeout):
            continue  # Skip if no such record

    if not records:
        return "No DNS records found."

    output = []
    for rtype, values in records.items():
        output.append(f"{rtype} Records:")
        for val in values:
            output.append(f"  - {val}")
    return '\n'.join(output)
