#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for viewing interface configuration with RESTCONF.

The script has been tested with DevNet reservable sandbox on May 2023:
"IOS XE on Cat 8kv Latest Code"

------------

Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import json
import requests
import urllib3

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Following line disables warnings of the unverified certificate. Do not use in production!
urllib3.disable_warnings()

def view_interface_config(device_ip:str, username:str, password:str,
                          port:int=443, verify:bool=False,
                          interface_type:str="GigabitEthernet")->None:
    '''
    Function to view interface configuration on an IOS XE device using RESTCONF.
    '''
    print(f"Retrieving interface configuration from device {device_ip}...", end=" ")

    # First retrieve native model information - this defines what has been configured
    url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-native:native/interface/{interface_type}"
    header = {"Accept": "application/yang-data+json"}

    configured_response = requests.get(url, headers=header,
                                auth=(username, password),
                                verify=verify, timeout=10)

    # Then lets retrieve 
    url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface"
    operational_response = requests.get(url, headers=header,
                            auth=(username, password),
                            verify=verify, timeout=10)

    operational_interfaces = {}
    if operational_response.status_code == 200:
        for interface in operational_response.json()["Cisco-IOS-XE-interfaces-oper:interface"]:
            operational_interfaces[interface["name"]] = {
                "ipv4": interface["ipv4"] if "ipv4" in interface else None,
                "ipv6": interface["ipv6-addrs"] if "ipv6-addrs" in interface else None
            }

    else:
        print("Error in retrieving operational interface configuration!")
        print(operational_response.text)

    if configured_response.status_code == 200:
        print("Success!")
        for interface in configured_response.json()[f"Cisco-IOS-XE-native:{interface_type}"]:
            interface_number = interface['name']
            print(f"\n{interface_type} {interface_number} ('{interface.get('description')}')")
            if "ip" in interface:
                print("- IPv4 address present!")
                print(f"  - Configured: {interface['ip']['address']}")
                print(f"  - Actual: {operational_interfaces[f'{interface_type}{interface_number}']['ipv4']}")
            else:
                print("- No IPv4 address configured!")
            if "ipv6" in interface:
                ipv6_addresses = operational_interfaces[f'{interface_type}{interface_number}']['ipv6']
                print("- IPv6 address present!")
                print(f'  - Configured: {interface["ipv6"]["address"]["prefix-list"]}')
                print(f"  - Actual: {', '.join(ipv6_addresses) if ipv6_addresses else None}")
                
            else:
                print("- No IPv6 address configured!")
    else:
        print("Error in retrieving configured interface configuration!")
        print(configured_response.text)

if __name__ == "__main__":
    # Update the IP address and credentials to match with your environment
    # if not using the DevNet reservable C8Kv sandbox!

    devices = [
        "10.10.20.48" #The IP address of the reservable sandbox
    ]

    #The credentials of the reservable sandbox
    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }

    for device in devices:
        view_interface_config(device, credentials["username"], credentials["password"])
