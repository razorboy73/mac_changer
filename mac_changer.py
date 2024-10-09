#!/usr/bin/env python
import subprocess
import argparse
import re
import math
import email

original_mac = ""
changed_mac = ""
test_variable =""
test_variable2 =""


def main():
    global original_mac
    global changed_mac
    interface, new_mac = get_arguments()
    ifconfig_result = check_interface(interface)
    print(f'Current MAC Address: {ifconfig_result}')
    original_mac = ifconfig_result
    change_mac(interface, new_mac)
    ifconfig_result = check_interface(interface)
    print(ifconfig_result)
    changed_mac = ifconfig_result
    print(confirm_changes(new_mac))


def confirm_changes(new_mac):
    global original_mac
    global changed_mac
    # if original_mac != changed_mac:
    #     return("MAC Address successfully changed")
    #     else:
    #   return("[-]MAC Address not changed")


    if changed_mac == new_mac:
        return("Confirming that MAC Address successfully changed to the requested MAC")
    else:
        return("[-]Confirming MAC Address not changed")



def find_mac(ifconfig_results):
    pattern = rb'ether ([0-9a-fA-F:]{17})'
    # Using re.search to find the MAC address
    mac_address_search_result = re.search(pattern, ifconfig_results)
    # print(f"mac_address_search_result: {mac_address_search_result}")
    if mac_address_search_result:
        mac_address = mac_address_search_result.group(1).decode()
        return mac_address
    else:
        return ('No MAC address found')


def check_interface(interface):
    ifconfig_results = subprocess.check_output(["ifconfig", interface])
    mac_address = find_mac(ifconfig_results)
    return mac_address


def change_mac(interface, new_mac):
    print(f"Changing MAC address for {interface} to {new_mac}")

    subprocess.call(["ifconfig", f"{interface}", "down"])
    subprocess.call(["ifconfig", f"{interface}", "hw", "ether", f"{new_mac}"])
    subprocess.call(["ifconfig", f"{interface}", "up"])
    # print(f"MAC address for {interface} has been changed to {new_mac}")


def get_arguments():
    parser = argparse.ArgumentParser(description='Input the interface and MAC address')
    parser.add_argument("-i", "--interface", dest="interface", type=str, help='The interface you want to modify')
    parser.add_argument("--mac", "-m", dest="mac", required=True, type=str, help='The new mac address')
    args = parser.parse_args()
    print(f'Interface Argument: {args.interface}')
    if not args.interface:
        parser.error("[-] Please specify an interface. use --help for assistance")
    # handled errors for the mac address within the arguments
    return args.interface, args.mac


if __name__ == "__main__":
    main()
