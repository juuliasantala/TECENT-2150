#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for updating interface configuration with RESTCONF.

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

import requests
import urllib3

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Following line disables warnings of the unverified certificate. Do not use in production!
urllib3.disable_warnings()

def configure_interfaces(device_ip:str, username:str, password:str,
                        configuration:list,
                        port:int=443, verify:bool=False)->None:
    '''
    Function to configure interface on an IOS XE device using RESTCONF.
    '''
    print(f"Configuring interfaces on {device_ip}...", end=" ")

    url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-native:native/interface"
    header = {"Content-Type": "application/yang-data+json"}
    payload = {
        "Cisco-IOS-XE-native:interface": {
            "GigabitEthernet": [
                {
                    "name": interface["number"],
                    "description": interface["description"],
                    "ipv6": {
                        "address": {
                            "prefix-list": [
                                {
                                    "prefix":interface["ipv6_prefix"]
                                }
                            ]
                        },
                        "enable": [None]
                    }
                }
            for interface in configuration if interface["type"] == "GigabitEthernet"
            ]
        }
    }

    response = requests.patch(url, headers=header, auth=(username, password),
                              json=payload, verify=verify)

    if response.status_code in (200, 204):
        print("Success!")
    else:
        print("Error!")
        print(response.text)

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

    # Note that the interface descriptions used in the demo do not match to the DevNet
    # sandbox topology.
    interfaces = [
        {
            "type": "GigabitEthernet",
            "number": 1,
            "description": "Towards Internet",
            "ipv6_prefix": "2001:db8:2200:001::01/64"
        },
        {
            "type": "GigabitEthernet",
            "number": 2,
            "description": "Towards LAN",
            "ipv6_prefix": "2001:db8:2200:001::10/64"
        }
    ]

    for device in devices:
        configure_interfaces(device, credentials["username"], credentials["password"], interfaces)
