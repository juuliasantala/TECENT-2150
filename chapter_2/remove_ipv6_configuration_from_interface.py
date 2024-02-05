#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for removing IPv6 from a interface configuration with
RESTCONF (even though the speakers of this technical seminar love IPv6 and
therefor highly disapprove removing it other than in testing purposes)

The script has been tested with DevNet reservable sandbox on February 2024:
"IOS XE on Cat 8kv"

------------

Copyright (c) 2024 Cisco and/or its affiliates.
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

import requests
import urllib3

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2024 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Following line disables warnings of the unverified certificate. Do not use in production!
urllib3.disable_warnings()

def remove_interface_ipv6_config(device_ip:str, username:str, password:str,
                                 interface_type:str, interface_number:str,
                                 port:int=443, verify:bool=False)->None:
    '''
    Function to remove interface IPV6 configuration on an IOS XE device using RESTCONF.
    '''
    print(f"Removing IPv6 configuration from interface {interface} on device {device_ip}...",
          end=" ")
    base_url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-native:native"
    url = f"{base_url}/interface/{interface_type}={interface_number}/ipv6"
    header = {"Accept": "application/yang-data+json"}

    response = requests.delete(url, headers=header,
                            auth=(username, password),
                            verify=verify, timeout=10)

    if response.status_code == 204:
        print("Success!")
    else:
        print("An error occurred:")
        print(response.text)

if __name__ == "__main__":
    # Update the IP address and credentials to match with your environment
    # if not using the DevNet reservable C8Kv sandbox!

    devices = [
        "10.10.20.48" #The IP address of the reservable sandbox
    ]

    # The credentials of the reservable sandbox
    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }

    # The interfaces whose IPv6 configuration should be removed.
    # Current default values defined based on DevNet sandbox, feel free to adjust
    # to your device or your need.
    interfaces  = [
        {"type": "GigabitEthernet", "number": 1},
        {"type": "GigabitEthernet", "number": 2},
        {"type": "GigabitEthernet", "number": 3}
    ]

    for device in devices:
        for interface in interfaces:
            remove_interface_ipv6_config(device, credentials["username"], credentials["password"],
                                         interface["type"], interface["number"])
