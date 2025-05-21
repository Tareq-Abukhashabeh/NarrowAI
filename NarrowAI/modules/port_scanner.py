import socket
import concurrent.futures
import subprocess
import re

common_ports = [21, 22, 25, 53, 80, 110, 143, 443, 445, 3306, 8080]

def detect_service_versions(target):
    print("[*] Running service version detection...")
    try:
        result = subprocess.run(
            ["nmap", "-sV", "--min-rate", "1000", target],
            capture_output=True,
            text=True
        )
        # Clean the nmap output by removing unnecessary headers and extra blank lines
        output = result.stdout
        lines = output.splitlines()

        # Find start of port/service info (line containing "PORT")
        start_index = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("PORT"):
                start_index = i
                break
        
        # Extract the useful part starting from "PORT" header till end or empty line after ports
        cleaned_lines = []
        for line in lines[start_index:]:
            if line.strip() == "" and cleaned_lines:
                break
            cleaned_lines.append(line.rstrip())

        cleaned_output = "\n".join(cleaned_lines).strip()
        return cleaned_output if cleaned_output else output.strip()

    except Exception as e:
        return f"[!] Service version scan failed: {e}"

def scan_port(domain, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        result = sock.connect_ex((domain, port))
        if result == 0:
            return port
    except Exception:
        return None
    finally:
        sock.close()
    return None

def scan_ports(domain, ports=common_ports):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(scan_port, domain, port) for port in ports]
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port:
                open_ports.append(port)
    return open_ports
