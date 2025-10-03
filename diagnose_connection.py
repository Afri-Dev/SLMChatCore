"""
Quick diagnostic script to help identify Flutter connection issues
Run this on your PC to verify the API is accessible from your network
"""
import socket
import requests
import json
from colorama import init, Fore, Style

init(autoreset=True)

def print_header(text):
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{text}")
    print(f"{Fore.CYAN}{'='*60}\n")

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Create a socket to find local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return None

def test_localhost():
    """Test if API is accessible on localhost"""
    print_header("🏥 Testing API on localhost")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ SUCCESS: API responds on localhost:8000")
            print(f"{Fore.WHITE}Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"{Fore.RED}❌ FAIL: Got status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}❌ FAIL: Connection refused - API server not running!")
        print(f"{Fore.YELLOW}⚠️  Start the server with: uvicorn faq_api:app --reload --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"{Fore.RED}❌ FAIL: {e}")
        return False

def test_network_ip(ip):
    """Test if API is accessible from network IP"""
    print_header(f"🌐 Testing API on network IP: {ip}")
    try:
        response = requests.get(f"http://{ip}:8000/health", timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ SUCCESS: API is accessible from network!")
            print(f"{Fore.WHITE}Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"{Fore.RED}❌ FAIL: Got status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}❌ FAIL: Connection refused from network IP")
        print(f"{Fore.YELLOW}⚠️  Possible causes:")
        print(f"{Fore.YELLOW}   1. API server not bound to 0.0.0.0 (check uvicorn --host parameter)")
        print(f"{Fore.YELLOW}   2. Windows Firewall blocking port 8000")
        print(f"{Fore.YELLOW}   3. Antivirus software blocking connections")
        return False
    except Exception as e:
        print(f"{Fore.RED}❌ FAIL: {e}")
        return False

def check_port_listening():
    """Check if port 8000 is listening"""
    print_header("🔌 Checking if port 8000 is listening")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        
        if result == 0:
            print(f"{Fore.GREEN}✅ Port 8000 is open and listening")
            return True
        else:
            print(f"{Fore.RED}❌ Port 8000 is not listening")
            print(f"{Fore.YELLOW}⚠️  Start the API server first!")
            return False
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}")
        return False

def generate_flutter_config(ip):
    """Generate Flutter configuration for each platform"""
    print_header("📱 Flutter Configuration Guide")
    
    print(f"{Fore.GREEN}Copy the appropriate baseUrl to your Flutter app's api_service.dart:\n")
    
    print(f"{Fore.YELLOW}For Android Emulator:")
    print(f"{Fore.WHITE}  static const String baseUrl = 'http://10.0.2.2:8000';\n")
    
    print(f"{Fore.YELLOW}For iOS Simulator:")
    print(f"{Fore.WHITE}  static const String baseUrl = 'http://localhost:8000';\n")
    
    print(f"{Fore.YELLOW}For Real Device (Phone/Tablet):")
    print(f"{Fore.WHITE}  static const String baseUrl = 'http://{ip}:8000';\n")
    
    print(f"{Fore.CYAN}📋 Instructions for your Flutter developer:")
    print(f"{Fore.WHITE}1. Open: lib/services/api_service.dart")
    print(f"{Fore.WHITE}2. Update the baseUrl constant based on your platform")
    print(f"{Fore.WHITE}3. Save and hot restart Flutter app (press 'R' in terminal)")
    print(f"{Fore.WHITE}4. For real device: Ensure device and PC are on same WiFi")
    print(f"{Fore.WHITE}5. For real device: Allow port 8000 in Windows Firewall")

def test_firewall():
    """Test if firewall might be blocking"""
    print_header("🔥 Firewall Check")
    print(f"{Fore.YELLOW}To allow port 8000 through Windows Firewall, run this in PowerShell as Administrator:\n")
    print(f"{Fore.WHITE}New-NetFirewallRule -DisplayName 'FAQ API Server' -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow\n")

def main():
    print(f"{Fore.MAGENTA}{Style.BRIGHT}")
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         Flutter FAQ API - Connection Diagnostics          ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Get local IP
    local_ip = get_local_ip()
    if local_ip:
        print(f"{Fore.CYAN}🖥️  Your PC's IP Address: {Fore.GREEN}{local_ip}")
    else:
        print(f"{Fore.RED}❌ Could not determine local IP address")
    
    print(f"{Fore.CYAN}📍 This IP is what you'll use in Flutter for real devices\n")
    
    # Run tests
    results = []
    
    # Test 1: Port listening
    port_ok = check_port_listening()
    results.append(("Port 8000 Listening", port_ok))
    
    if not port_ok:
        print(f"\n{Fore.RED}⚠️  STOP: Start the API server first!")
        print(f"{Fore.YELLOW}Run: uvicorn faq_api:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # Test 2: Localhost access
    localhost_ok = test_localhost()
    results.append(("Localhost Access", localhost_ok))
    
    # Test 3: Network IP access (if we have an IP)
    network_ok = False
    if local_ip:
        network_ok = test_network_ip(local_ip)
        results.append(("Network IP Access", network_ok))
    
    # Summary
    print_header("📊 Summary")
    
    for test_name, result in results:
        status = f"{Fore.GREEN}✅ PASS" if result else f"{Fore.RED}❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    
    if localhost_ok and not network_ok:
        print(f"{Fore.YELLOW}⚠️  API works locally but not accessible from network")
        print(f"{Fore.YELLOW}   This means:")
        print(f"{Fore.WHITE}   • Android/iOS emulators will work")
        print(f"{Fore.WHITE}   • Real devices will NOT work")
        print(f"{Fore.YELLOW}   Solutions:")
        print(f"{Fore.WHITE}   1. Check Windows Firewall (see below)")
        print(f"{Fore.WHITE}   2. Or use ngrok: ngrok http 8000")
        test_firewall()
    
    elif localhost_ok and network_ok:
        print(f"{Fore.GREEN}🎉 Success! API is fully accessible!")
        print(f"{Fore.WHITE}   • Emulators: ✅ Will work")
        print(f"{Fore.WHITE}   • Real devices: ✅ Will work (if on same WiFi)")
    
    elif not localhost_ok:
        print(f"{Fore.RED}⚠️  API server is not responding")
        print(f"{Fore.YELLOW}   Make sure it's running with:")
        print(f"{Fore.WHITE}   uvicorn faq_api:app --reload --host 0.0.0.0 --port 8000")
    
    # Generate Flutter config
    if local_ip:
        generate_flutter_config(local_ip)
    
    print(f"\n{Fore.CYAN}📖 For detailed troubleshooting, see: FLUTTER_TROUBLESHOOTING.md")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Interrupted by user")
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {e}")
