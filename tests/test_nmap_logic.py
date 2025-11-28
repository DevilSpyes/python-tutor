
import socket

# Mock classes for testing logic without full network interaction
class Target:
    def __init__(self, host):
        self.host = host
        self.ip = "127.0.0.1" # Mock IP
        self.open_ports = []

class NmapScanner:
    def _guess_service(self, port):
        services = {
            21: "ftp", 22: "ssh", 80: "http"
        }
        return services.get(port, "unknown")

def parse_ports(input_str):
    if not input_str.strip():
        return [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 3389, 8000, 8080]

    ports = set()
    parts = input_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            except ValueError:
                pass
        else:
            try:
                ports.add(int(part))
            except ValueError:
                pass
                
    return sorted(list(ports))

# Test Logic
print("--- Testing Port Parsing ---")
print(f"1-5: {parse_ports('1-5')}")
print(f"22, 80: {parse_ports('22, 80')}")
print(f"Empty: {parse_ports('')}")

print("\n--- Testing Service Guessing ---")
scanner = NmapScanner()
print(f"Port 22: {scanner._guess_service(22)}")
print(f"Port 9999: {scanner._guess_service(9999)}")

print("\n--- Testing Target Class ---")
t = Target("localhost")
print(f"Target IP: {t.ip}")
