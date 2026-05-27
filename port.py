import socket
import threading
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Banner
print(Fore.CYAN + """
██████╗  ██████╗ ██████╗ ████████╗
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
██████╔╝██║   ██║██████╔╝   ██║   
██╔═══╝ ██║   ██║██╔══██╗   ██║   
██║     ╚██████╔╝██║  ██║   ██║   
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   

   ███████╗ ██████╗ █████╗ ███╗   ██╗
   ██╔════╝██╔════╝██╔══██╗████╗  ██║
   ███████╗██║     ███████║██╔██╗ ██║
   ╚════██║██║     ██╔══██║██║╚██╗██║
   ███████║╚██████╗██║  ██║██║ ╚████║
   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝

        PORT SCANNER
          By Neeraj
""")

# Target input
target = input(Fore.YELLOW + "Enter Target IP/Domain: ")

# Open ports list
open_ports = []

# ALL ports
start_port = 1
end_port = 65535

print(
    Fore.CYAN +
    f"\n[*] PORT SCANNER is scanning {target} from {start_port} to {end_port}\n"
)

# Lock for thread safety
lock = threading.Lock()


# Scan function
def scan_port(port):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(0.3)

        result = s.connect_ex((target, port))

        if result == 0:

            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            with lock:

                print(
                    Fore.GREEN +
                    f"[OPEN] Port {port} ({service})"
                )

                open_ports.append((port, service))

                with open("results.txt", "a") as file:
                    file.write(
                        f"Port {port} OPEN ({service})\n"
                    )

        s.close()

    except:
        pass


# Thread list
threads = []

# Start scanning
for port in range(start_port, end_port + 1):

    thread = threading.Thread(
        target=scan_port,
        args=(port,)
    )

    threads.append(thread)

    thread.start()

    # Limit active threads
    if len(threads) >= 500:

        for thread in threads:
            thread.join()

        threads = []


# Wait remaining threads
for thread in threads:
    thread.join()

# Scan complete
print(Fore.YELLOW + "\n[✓] PORT SCANNER Scan Complete!\n")

# Summary
if open_ports:

    print(Fore.CYAN + "Open Ports Summary:\n")

    for port, service in open_ports:
        print(
            Fore.GREEN +
            f"➜ Port {port} ({service})"
        )

    print(
        Fore.YELLOW +
        f"\nTotal Open Ports Found: {len(open_ports)}"
    )

else:
    print(Fore.RED + "No open ports found.")
