#!/usr/bin/env python
import subprocess
#set up some variables
interface = input("interface: ")
new_mac = input("new mac: ")

print("[+] changing MAC address for " + interface + " to "+ new_mac)

#subprocess.call("ifconfig",shell=True)
subprocess.call("ifconfig " + interface + " down", shell=True)
subprocess.call("ifconfig " + interface + " hw ether " + new_mac, shell=True)
subprocess.call("ifconfig " + interface + " up", shell=True)
subprocess.call("ifconfig",shell=True)