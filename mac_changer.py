#!/usr/bin/env python
import subprocess
import argparse
import re


original_mac = ""
changed_mac = ""

"""
This program changes the MAC address for the specified interface.
1. Get input from the user for interface and MAC address via command line.
2. Validates the MAC address format.
3. Checks and changes the MAC address.
4. Confirms whether the MAC address was successfully updated.
"""




def get_arguments():
    """
    Parses command line arguments for interface and MAC address.
    """
    #this creates a parser object
    parser = argparse.ArgumentParser(description='Input the interface and MAC address')
    #adds the two agurments we want to collect
    parser.add_argument("-i", "--interface", dest="interface", type=str, help='The interface you want to modify')
    parser.add_argument("--mac", "-m", dest="new_mac", required=True, type=str, help='The new mac address')
    #(options,arguments) = parser.parse_args()
    args = parser.parse_args()
    #pyprint(f'parser args: {args}')
    print(f'Interface Argument: {args.interface}')
    print(f'MAC Address Argument: {args.new_mac}')
    if not args.interface:
        parser.error("[-] Please specify an interface. use --help for assistance")
    # handled errors for the mac address within the arguments
    return args.interface, args.new_mac


def validate_mac(mac):
    """Validates mack address format"""
    pattern = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
    return re.match(pattern, mac) is not None

def find_mac(ifconfig_results):
    """
    Finds and returns the MAC address from the ifconfig output.
    """
    pattern = rb'ether ([0-9a-fA-F:]{17})'
    mac_address_search_result = re.search(pattern, ifconfig_results)
    #print(f"mac_address_search_result: {mac_address_search_result}")
    if mac_address_search_result:
        mac_address = mac_address_search_result.group(1).decode()
        return mac_address
    else:
        return None

def check_interface(interface):
    """
    Retrieves the current MAC address for the specified interface.
    """
    try: 
        ifconfig_results = subprocess.check_output(["ifconfig", interface],stderr=subprocess.STDOUT)
        return find_mac(ifconfig_results)
    
    except subprocess.CalledProcessError as e:
        print(f"[-] Error checking interface: {e.output.decode().strip()}")
        return None
    

def change_mac(interface, new_mac):
    """
    Changes the MAC address for the specified interface.
    """
    print(f"Changing MAC address for {interface} to {new_mac}")
    #subprocess.call waits for command to execute
    #use a list of parameters to prevent malicious commands
    try:
        subprocess.run(["ifconfig", f"{interface}", "down"])
        subprocess.run(["ifconfig", f"{interface}", "hw", "ether", f"{new_mac}"])
        subprocess.run(["ifconfig", f"{interface}", "up"])
        print(f"MAC address for {interface} has been changed to {new_mac}")
    except subprocess.CalledProcessError as e:
        print(f"[-] Error changing MAC address: {e}")

def confirm_changes(new_mac):
    """
    Confirms if the MAC address has been successfully updated.
    """
    # if original_mac != changed_mac:
    #     return("MAC Address successfully changed")
    #     else:
    #   return("[-]MAC Address not changed")
    if changed_mac == new_mac:
        return True
    else:
        return False


def main():
    
    #get command line arguments
    interface, new_mac = get_arguments()
    #check_interface uses find_mac to find mac in the if config results

    #validate the MAC address format
    if not validate_mac(new_mac):
        print("[-] Invalid MAC address format. Please enter a valid MAC address.")
        return
    

    #check and display the original MAC address
    original_mac = check_interface(interface)
    if not original_mac:
        print("[-] Unable to retrieve the current MAC address.")
        return
    print(f"Current MAC Address: {original_mac}")

    # Verify if the MAC address was updated
    updated_mac= change_mac(interface, new_mac)
    #check that it swapped uses find_mac to find mac in the if config results

    if updated_mac:
          return f"[+] MAC Address successfully changed to {new_mac}"
    else:
        return "[-] MAC Address change failed."
    print(confirm_changes(new_mac))

if __name__ == "__main__":
    main()
