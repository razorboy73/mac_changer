#!/usr/bin/env python
import subprocess
import argparse
import re


original_mac = ""
changed_mac = ""

"""
this program changes the MAC address for the indicated interface
1. Get input from user for interface and MAC address via command line
2. checks if the interface has been changed
3. changes interface address


"""


def main():
    global original_mac
    global changed_mac
    #get command line arguments
    interface, new_mac = get_arguments()
    #check_interface uses find_mac to find mac in the if config results
    ifconfig_result = check_interface(interface)
    print(f'Current MAC Address: {ifconfig_result}')
    #set original mac address
    original_mac = ifconfig_result
    #call the chnge mac function
    change_mac(interface, new_mac)
    #check that it swapped uses find_mac to find mac in the if config results
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
    # Using re.search to find the MAC address
    pattern = rb'ether ([0-9a-fA-F:]{17})'
    mac_address_search_result = re.search(pattern, ifconfig_results)
    print(f"mac_address_search_result: {mac_address_search_result}")
    if mac_address_search_result:
        mac_address = mac_address_search_result.group(1).decode()
        return mac_address
    else:
        return ('[-]No MAC address found')


def check_interface(interface):
    #get result from ifconfig
    ifconfig_results = subprocess.check_output(["ifconfig", interface])
    mac_address = find_mac(ifconfig_results)
    return mac_address


def change_mac(interface, new_mac):
    print(f"Changing MAC address for {interface} to {new_mac}")
    #subprocess.call waits for command to execute
    #use a list of parameters to prevent malicious commands
    subprocess.call(["ifconfig", f"{interface}", "down"])
    subprocess.call(["ifconfig", f"{interface}", "hw", "ether", f"{new_mac}"])
    subprocess.call(["ifconfig", f"{interface}", "up"])
    # print(f"MAC address for {interface} has been changed to {new_mac}")


def get_arguments():
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


if __name__ == "__main__":
    main()
