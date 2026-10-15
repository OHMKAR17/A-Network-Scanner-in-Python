
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor

def check_host(ip):
    try:
        # A short connection timeout keeps scans from hanging
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((str(ip), 80))

            if result == 0:
                return f"[+] {ip} - Port 80 is open"

    except OSError:
        pass

    return None


def scan_network(network):
    try:
        subnet = ipaddress.ip_network(network, strict=False)

        # Limit this beginner project to small IPv4 networks
        if subnet.version != 4 or subnet.num_addresses > 256:
            print("Please enter an IPv4 network with at most 256 addresses.")
            return

        print(f"\nScanning {subnet} for devices with port 80 open...\n")

        with ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(check_host, subnet.hosts())

            found = 0
            for result in results:
                if result:
                    print(result)
                    found += 1

        print(f"\nScan complete. Responsive hosts found: {found}")
        print("Note: This checks port 80 only.")

    except ValueError:
        print("Invalid network. Example: 192.168.1.0/24")


print("==============================")
print("       NETWORK SCANNER")
print("==============================")

network = input("Enter your own network (e.g. 192.168.1.0/24): ").strip()
scan_network(network)
