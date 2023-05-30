#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for viewing IPv6 configuration with RESTCONF.

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

import pprint # for prettier JSON indentation
import requests
import urllib3

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Following line disables warnings of the unverified certificate. Do not use in production!
urllib3.disable_warnings()

def view_ipv6(device_ip:str, username:str, password:str, port:int=443, verify:bool=False)->None:
    '''
    Function to view IPv6 configuration on an IOS XE device using RESTCONF.
    '''
    print(f"Retrieving IPv6 configuration from device {device_ip}...", end=" ")

    url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-native:native/ipv6/"
    header = {"Accept": "application/yang-data+json"}

    response = requests.get(url, headers=header,
                            auth=(username, password),
                            verify=verify, timeout=10)
    if response.status_code == 200:
        print("IPv6 configured!")
        print("Configuration:")
        pprint.pprint(response.json())
    elif response.status_code == 204:
        print("No IPv6 configuration present!")
    else:
        print("Error in retrieving IPv6 configuration!")
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

    for device in devices:
        view_ipv6(device, credentials["username"], credentials["password"])
