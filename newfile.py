import os
import time
import socket
import urllib.request
import json
import base64
import hashlib
import threading
from datetime import datetime

# Archivo para guardar los paquetes instalados de forma permanente
INSTALLED_FILE = ".termdroid_installed"

# Colores estilo Termux / Hacking
GREEN = '\033[92m'
RED = '\033[91m'
WHITE = '\033[97m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

history = []

# Cargar paquetes instalados previamente si existen
installed_packages = []
if os.path.exists(INSTALLED_FILE):
    try:
        with open(INSTALLED_FILE, "r") as f:
            installed_packages = [line.strip() for line in f if line.strip()]
    except:
        pass

AVAILABLE_PACKAGES = [
    "neofetch", "cowsay", "matrix", "traceroute", 
    "speedtest", "hashgen", "base64", "httpdump", 
    "weather", "whois", "maclookup"
]

# --- BANNER DE ADVERTENCIA ÉTICA Y EDUCATIVA ---
print(f"{RED}=====================================================")
print(f" [!] ADVERTENCIA: SOLO PARA USO ÉTICO Y EDUCATIVO [!]")
print(f"-----------------------------------------------------")
print(f" El uso no autorizado de estas herramientas contra")
print(f" objetivos sin consentimiento previo es ilegal.")
print(f" El usuario es el único responsable de sus actos.")
print(f"====================================================={RESET}")
print(f"{CYAN}  Termdroid NetScanner Pro Suite (v3 Persistent)   ")
print(f"  Type 'help' to show all available commands      {RESET}")
print(f"=====================================================")

while True:
    prompt_text = f"{GREEN}user@termdroid:~€{RESET} "
    command = input(prompt_text).strip()
    
    if command != "":
        history.append(command)
    
    parts = command.split()
    base_cmd = parts[0] if parts else ""
    
    if base_cmd == "help":
        print(f"\n{WHITE}--- NETWORK & SECURITY SUITE ---")
        print("help                 : Display this help menu")
        print("myip                 : Get your public IP & precise network info")
        print("ipinfo <ip/host>     : Detailed IP lookup & geolocation")
        print("dnslookup <domain>   : Real DNS resolution")
        print("ping <host>          : Real connection latency test")
        print("nmap <host>          : Standard TCP port scan (Top ports)")
        print("portscan <ip> <s> <e>: Fast multi-threaded port scanner")
        print("netstat              : Show active local connections")
        print("apt install <pkg>    : Install extra tools (e.g. maclookup)")
        print("apt list             : List available packages")
        print("whoami               : Show active user profile")
        print("date                 : Show current system date & time")
        print("history              : Show command execution history")
        print("clear                : Clear the terminal screen")
        print("exit                 : Close Termdroid session{RESET}")
        if installed_packages:
            print(f"\n{YELLOW}--- INSTALLED TOOLS ({len(installed_packages)}) ---{RESET}")
            for p in installed_packages:
                print(f" - {p}")
        print("")
        
    elif base_cmd == "apt":
        if len(parts) >= 2 and parts[1] == "list":
            print("--- AVAILABLE PACKAGES REPO ---")
            for pkg in AVAILABLE_PACKAGES:
                status = f"{GREEN}[installed]{RESET}" if pkg in installed_packages else f"{WHITE}[not installed]{RESET}"
                print(f" {pkg} {status}")
        elif len(parts) >= 3 and parts[1] == "install":
            pkg = parts[2].lower()
            if pkg in installed_packages:
                print(f"Package '{pkg}' is already installed.")
            elif pkg in AVAILABLE_PACKAGES:
                print(f"Reading package lists... Done")
                print(f"Downloading and configuring {pkg}...")
                time.sleep(0.3)
                installed_packages.append(pkg)
                
                # Guardar en archivo persistente
                try:
                    with open(INSTALLED_FILE, "w") as f:
                        for p in installed_packages:
                            f.write(p + "\n")
                except:
                    pass
                    
                print(f"{GREEN}[+] Successfully installed '{pkg}' (Saved persistently)!{RESET}")
            else:
                print(f"{RED}E: Unable to locate package '{pkg}'. Type 'apt list'.{RESET}")
        else:
            print("Usage: apt install <pkg>  or  apt list")

    # --- COMANDO MYIP ---
    elif base_cmd == "myip":
        print("Fetching your IP info and resolving routing nodes...")
        try:
            req = urllib.request.urlopen("https://ipinfo.io/json", timeout=5)
            data = json.loads(req.read().decode('utf-8'))
            
            ip = data.get('ip')
            hostname = "N/A"
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except:
                pass

            print(f"\n{WHITE}--- IPINFO ADVANCED NETWORK INFO ---")
            print(f"IP Address : {ip}")
            print(f"Node/Host  : {hostname}")
            print(f"City (Geo) : {data.get('city')} (Nota: Las ISPs agrupan nodos en capitales)")
            print(f"Region     : {data.get('region')}")
            print(f"Country    : {data.get('country')}")
            print(f"Coordinates: {data.get('loc')}")
            print(f"Org / ISP  : {data.get('org')}")
            print(f"Timezone   : {data.get('timezone')}{RESET}\n")
        except Exception as e:
            print(f"{RED}Error fetching from ipinfo.io: {e}{RESET}")

    # --- COMANDO IPINFO ---
    elif base_cmd == "ipinfo":
        target = parts[1] if len(parts) > 1 else ""
        print(f"Querying ipinfo.io database for {target if target else 'your connection'}...")
        try:
            if target:
                try:
                    target = socket.gethostbyname(target)
                except:
                    pass
                url = f"https://ipinfo.io/{target}/json"
            else:
                url = "https://ipinfo.io/json"

            req = urllib.request.urlopen(url, timeout=5)
            data = json.loads(req.read().decode('utf-8'))
            
            if data.get('ip'):
                ip_val = data.get('ip')
                resolved_host = "N/A"
                try:
                    resolved_host = socket.gethostbyaddr(ip_val)[0]
                except:
                    pass

                print(f"\n{WHITE}--- IPINFO LOOKUP RESULT ---")
                print(f"IP Address : {ip_val}")
                print(f"Hostname   : {resolved_host}")
                print(f"City       : {data.get('city', 'N/A')}")
                print(f"Region     : {data.get('region', 'N/A')}")
                print(f"Country    : {data.get('country', 'N/A')}")
                print(f"Coordinates: {data.get('loc', 'N/A')}")
                print(f"ASN / Org  : {data.get('org', 'N/A')}")
                print(f"Timezone   : {data.get('timezone', 'N/A')}{RESET}\n")
            else:
                print(f"{RED}Could not retrieve valid data for target.{RESET}")
        except Exception as e:
            print(f"{RED}Error connecting to ipinfo.io API: {e}{RESET}")

    elif base_cmd == "dnslookup":
        if len(parts) > 1:
            domain = parts[1]
            print(f"Resolving DNS for {domain}...")
            try:
                ip_res = socket.gethostbyname(domain)
                print(f"{GREEN}[+] {domain} ---> {ip_res}{RESET}")
            except socket.gaierror:
                print(f"{RED}DNS lookup failed: Could not resolve {domain}{RESET}")
        else:
            print("Usage: dnslookup <domain.com>")

    # --- COMANDO NMAP (SIN OBJETIVO POR DEFECTO) ---
    elif base_cmd == "nmap":
        if len(parts) > 1:
            target = parts[1]
            print(f"Starting standard Nmap scan on {target}...")
            try:
                target_ip = socket.gethostbyname(target)
                print(f"Target IP: {target_ip}\nPORT     STATE")
                common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]
                for port in common_ports:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.3)
                    if s.connect_ex((target_ip, port)) == 0:
                        print(f"{GREEN}{port}/tcp   open{RESET}")
                    else:
                        print(f"{WHITE}{port}/tcp   closed{RESET}")
                    s.close()
            except Exception as e:
                print(f"{RED}Scan error: {e}{RESET}")
        else:
            print(f"{RED}Usage: nmap <ip or domain> (Ejemplo: nmap 192.168.1.1){RESET}")

    # --- PORTSCAN ULTRARRÁPIDO CON HILOS ---
    elif base_cmd == "portscan":
        if len(parts) >= 4:
            target = parts[1]
            try:
                start_p = int(parts[2])
                end_p = int(parts[3])
                target_ip = socket.gethostbyname(target)
                print(f"Scanning range {start_p}-{end_p} on {target} ({target_ip}) using multi-threads...")
                
                open_ports = []
                lock = threading.Lock()

                def scan_port(p):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.2)
                    result = s.connect_ex((target_ip, p))
                    if result == 0:
                        with lock:
                            print(f"{GREEN}[OPEN] Port {p}{RESET}")
                            open_ports.append(p)
                    s.close()

                threads = []
                for p in range(start_p, end_p + 1):
                    t = threading.Thread(target=scan_port, args=(p,))
                    threads.append(t)
                    t.start()
                    if len(threads) >= 100:
                        for th in threads:
                            th.join()
                        threads = []

                for th in threads:
                    th.join()

                print(f"\nScan finished. Total open ports found: {len(open_ports)}")
            except Exception as e:
                print(f"{RED}Error in parameters: {e}{RESET}")
        else:
            print("Usage: portscan <host> <start> <end>")

    elif base_cmd == "netstat":
        print(f"{WHITE}--- ACTIVE LOCAL SOCKETS ---")
        print("Family: INET, Protocol: TCP/UDP")
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(f"Local Hostname : {hostname}")
            print(f"Local Bind IP  : {local_ip}")
            print(f"Status         : Interface Up / Listening{RESET}")
        except Exception as e:
            print(f"{RED}Error reading network interfaces: {e}{RESET}")

    elif base_cmd == "ping":
        target_host = parts[1] if len(parts) > 1 else "google.com"
        print(f"PING {target_host}...")
        try:
            t_ip = socket.gethostbyname(target_host)
            for i in range(3):
                start_t = time.time()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.0)
                try:
                    s.connect((t_ip, 80))
                    latency = (time.time() - start_t) * 1000
                    print(f"64 bytes from {t_ip}: icmp_seq={i+1} time={latency:.1f}ms")
                except:
                    print(f"Request timeout for icmp_seq={i+1}")
                s.close()
                time.sleep(0.2)
        except Exception:
            print(f"{RED}ping: unknown host {target_host}{RESET}")

    # --- PAQUETES EXTRA (PERSISTENTES) ---
    elif base_cmd in installed_packages:
        if base_cmd == "neofetch":
            print(f"{GREEN}       .-.       {RESET} user@termdroid")
            print(f"{GREEN}      /   \\      {RESET} --------------")
            print(f"{GREEN}     |  o o|     {RESET} OS: Termdroid NetScanner Edition")
            print(f"{GREEN}     \\  =-/      {RESET} Kernel: Linux 5.10-android")
            print(f"{GREEN}    / 'v' \\      {RESET} Installed Tools: {len(installed_packages)}")
            
        elif base_cmd == "cowsay":
            msg = " ".join(parts[1:]) if len(parts) > 1 else "Ethical hacking active!"
            print(f" __________________ ")
            print(f"< {msg} >")
            print( f" ------------------ ")
            print(f"        \\   ^__^")
            print(f"         \\  (oo)\\_______")
            print(f"            (__)\\       )\\/\\")
            print(f"                ||----w |")
            print(f"                ||     ||")
            
        elif base_cmd == "matrix":
            print(f"{GREEN}01011001 01110011 01110100 01100101 01101101{RESET}")
            for _ in range(5):
                time.sleep(0.15)
                print(f"{GREEN}1092834 98123 094812 3908 102938 49102 384{RESET}")
            print(f"{GREEN}[Matrix stream finished]{RESET}")
            
        elif base_cmd == "traceroute":
            target = parts[1] if len(parts) > 1 else "google.com"
            print(f"Tracing real route to {target}...")
            try:
                t_ip = socket.gethostbyname(target)
                print(f"1  gateway (local network)  1.2ms")
                start_t = time.time()
                urllib.request.urlopen(f"http://{t_ip}", timeout=3)
                total_time = (time.time() - start_t) * 1000
                print(f"2  target server ({t_ip})  {total_time:.1f}ms [Reached]")
            except Exception as e:
                print(f"{RED}Traceroute finished with network limitation: {e}{RESET}")
            
        elif base_cmd == "speedtest":
            print("Running real speed test (downloading test payload)...")
            try:
                start_t = time.time()
                req = urllib.request.urlopen("https://cloudflare.com/cdn-cgi/trace", timeout=5)
                data = req.read()
                duration = time.time() - start_t
                speed_kbps = (len(data) * 8) / duration / 1024
                print(f"{CYAN}Download throughput : {speed_kbps:.2f} Kbps{RESET}")
                print(f"{GREEN}Connection status   : Stable / Active{RESET}")
            except Exception as e:
                print(f"{RED}Speedtest error: {e}{RESET}")
            
        elif base_cmd == "hashgen":
            text = " ".join(parts[1:]) if len(parts) > 1 else "termdroid"
            md5_val = hashlib.md5(text.encode()).hexdigest()
            sha_val = hashlib.sha256(text.encode()).hexdigest()
            print(f"Text   : {text}")
            print(f"MD5    : {md5_val}")
            print(f"SHA256 : {sha_val}")
            
        elif base_cmd == "base64":
            if len(parts) > 2 and parts[1] == "-d":
                try:
                    dec = base64.b64decode(parts[2]).decode()
                    print(f"Decoded: {dec}")
                except:
                    print(f"{RED}Invalid base64 string{RESET}")
            else:
                txt = parts[1] if len(parts) > 1 else "hello"
                enc = base64.b64encode(txt.encode()).decode()
                print(f"Encoded: {enc}")
                
        elif base_cmd == "httpdump":
            url = parts[1] if len(parts) > 1 else "https://httpbin.org/headers"
            if not url.startswith("http"):
                url = "https://" + url
            print(f"Fetching real headers from {url}...")
            try:
                req = urllib.request.urlopen(url, timeout=4)
                print(f"Status Code: {req.getcode()}")
                for k, v in req.headers.items():
                    print(f"{k}: {v}")
            except Exception as e:
                print(f"{RED}Error: {e}{RESET}")
                
        elif base_cmd == "weather":
            city = parts[1] if len(parts) > 1 else "Madrid"
            print(f"Fetching real weather for {city}...")
            try:
                url = f"https://wttr.in/{city}?format=3"
                req = urllib.request.urlopen(url, timeout=4)
                print(f"{WHITE}{req.read().decode('utf-8')}{RESET}")
            except:
                print(f"{RED}Could not fetch weather data{RESET}")
                
        elif base_cmd == "whois":
            domain = parts[1] if len(parts) > 1 else "google.com"
            print(f"Querying real RDAP database for {domain}...")
            try:
                url = f"https://rdap.org/domain/{domain}"
                req = urllib.request.urlopen(url, timeout=5)
                data = json.loads(req.read().decode('utf-8'))
                
                print(f"\n{WHITE}--- REAL WHOIS / RDAP DATA ---")
                print(f"Domain Name : {data.get('ldhName', domain).upper()}")
                print(f"Handle      : {data.get('handle', 'N/A')}")
                statuses = data.get('status', [])
                if statuses:
                    print(f"Status      : {', '.join(statuses[:3])}")
                print(f"{RESET}\n")
            except Exception as e:
                print(f"{RED}Error fetching real whois data: {e}{RESET}")

        elif base_cmd == "maclookup":
            mac = parts[1] if len(parts) > 1 else "FC:FB:FB"
            print(f"Querying MAC vendor database for {mac}...")
            try:
                url = f"https://api.macvendors.com/{mac}"
                req = urllib.request.urlopen(url, timeout=4)
                vendor = req.read().decode('utf-8')
                print(f"{GREEN}[+] MAC Vendor: {vendor}{RESET}")
            except Exception as e:
                print(f"{RED}Could not find vendor for MAC: {e}{RESET}")

    # --- COMANDOS BÁSICOS ---
    elif base_cmd == "whoami":
        print("root@termdroid-mobile")

    elif base_cmd == "date":
        print(datetime.now().strftime("%a %b %d %H:%M:%S CEST %Y"))

    elif base_cmd == "history":
        for idx, cmd in enumerate(history, 1):
            print(f" {idx}  {cmd}")

    elif base_cmd == "clear":
        os.system('clear')
        
    elif base_cmd == "exit":
        print("Shutting down Termdroid...")
        break
        
    elif base_cmd == "":
        continue
        
    else:
        print(f"{RED}termdroid: command not found: '{command}'. Type 'help' or 'apt list'.{RESET}")
