import os
import sys
import requests
import ipaddress
import socket
import google.generativeai as genai
from modules import whois_lookup, dns_lookup, subdomain_finder, email_extractor, port_scanner
import re
import webbrowser

# Configure Gemini
GEMINI_API_KEY = "API_KEY"   # Replace it with Your API Key 

def is_ip_address(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False

def analyze_report(report_text):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
You are a cybersecurity analyst and pentest. Based on the recon report below, provide:

===== Summary Analysis =====
- Tell me about the average security for this machine or domain and rate the security from 10.

===== Vulnerability Analysis =====
- Output a clean and readable table using plain text formatting.
- Each row: Port | Service | Version | Severity | Common vulnerabilities on version
- Give advice to achieve highest security for this machine or domain.

Recon Report:
{report_text}
"""

    def colorize_severity(text):
        text = re.sub(r'\bCritical\b', '\033[1;91mCritical\033[0m', text)   
        text = re.sub(r'\bHigh\b', '\033[95mHigh\033[0m', text)    
        text = re.sub(r'\bMedium\b', '\033[93mMedium\033[0m', text)   
        text = re.sub(r'\bLow\b', '\033[96mLow\033[0m', text)      
        return text

    try:
        response = model.generate_content(prompt)
        return colorize_severity(response.text.strip())
    except Exception as e:
        return f"[!] DRX0 AI failed: {e}"
        
def interactive_ai_chat(context):
    print("\n[*] You can now ask follow-up questions about the scan result.")
    print("Type 'exit' to quit.\n")

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=[{"role": "user", "parts": [f"Here is a recon report:\n{context}"]}])

    while True:
        print("------------------------------------------------------------------------------------------------------")
        user_input = input("[?] Ask DRX0 AI or type exit > ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            break

        # Handle CVE opening commands Under Development (NOT WORKING YET)
        if "open cve" in user_input.lower() or "show cve" in user_input.lower():
            open_cve_links_from_text(user_input)
            continue

        response = chat.send_message(user_input)
        print(f"\n[AI] {response.text.strip()}\n")


def load_wordlist(path):
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main(target):
    CYAN = "\033[96m"
    RED = "\033[91m"
    NC = "\033[0m" 



    print(f"""{RED}
██████╗ ██████╗ ██╗  ██╗ ██████╗ 
██╔══██╗██╔══██╗╚██╗██╔╝██╔═████╗
██║  ██║██████╔╝ ╚███╔╝ ██║██╔██║
██║  ██║██╔══██╗ ██╔██╗ ████╔╝██║
██████╔╝██║  ██║██╔╝ ██╗╚██████╔╝
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ 
{NC}""")

    print("====================================")
    print(f"{CYAN} Powered by Tareq Abu Khashabeh   {NC}")
    print(" GitHub: https://github.com/Tareq-Abukhashabeh")
    print("====================================")

    print(f"[+] Starting AI-powered reconnaissance on: {target}")
    is_ip = is_ip_address(target)

    if not is_ip:
        print("[*] Fetching WHOIS data...")
        whois_data = whois_lookup.get_whois(target)

        print("[*] Fetching DNS records...")
        dns_records = dns_lookup.get_dns_records(target)

        print("[*] Finding subdomains...")
        wordlist = load_wordlist('wordlists/subdomains.txt')
        subdomains = subdomain_finder.find_subdomains(target, wordlist)

        print("[*] Extracting emails from homepage...")
        emails = email_extractor.extract_emails(target)
    else:
        whois_data = "Skipped for IP"
        dns_records = "Skipped for IP"
        subdomains = []
        emails = []

    print("[*] Scanning common ports...")
    open_ports = port_scanner.scan_ports(target)
    service_info = port_scanner.detect_service_versions(target)

    # Compile Report
    report = f"ReconAI Report for {target}\n\n"
    report += "WHOIS Data:\n" + str(whois_data) + "\n\n"
    report += "DNS Records:\n" + str(dns_records) + "\n\n"
    report += f"Found Subdomains ({len(subdomains)}): {', '.join(subdomains)}\n\n"
    report += f"Found Emails ({len(emails)}): {', '.join(emails)}\n\n"
    report += f"Open Ports ({len(open_ports)}): {', '.join(map(str, open_ports))}\n\n"
    report += "Service Version Detection:\n" + service_info + "\n\n"

    print("[*] Analyzing report with AI...")
    ai_analysis = analyze_report(report)

    os.makedirs('output', exist_ok=True)
    with open('output/report.txt', 'w') as f:
        f.write(report + "\n--- AI Analysis ---\n" + ai_analysis)

    print("[+] Recon complete. Report saved to output/report.txt")
    print("\n--- AI Analysis ---\n")
    print(ai_analysis)
   
    # Prepare full context for follow-up chat
    full_context = report + "\n\n--- AI Analysis ---\n" + ai_analysis

    interactive_ai_chat(full_context)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <target>")
        sys.exit(1)
    main(sys.argv[1])
