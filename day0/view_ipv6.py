#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for viewing IPv6 configuration with NETCONF.

------------

Copyright (c) 2025 Cisco and/or its affiliates.
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

from ncclient import manager
import xmltodict

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2025 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


def view_ipv6(device_ip:str, username:str, password:str, port:int=830, verify:bool=False)->None:
    '''
    Function to view IPv6 configuration on an IOS XE device using NETCONF.
    '''
    print(f"\nConnecting to device {device_ip}...", end=" ")

    device = {
        "host": device_ip,
        "port": port,
        "username": username,
        "password": password,
        "hostkey_verify": verify
    }

    try:
        with manager.connect(**device, device_params={"name":"iosxe"},timeout=10) as connection:
            print("success!")

            # xpath defines that we are only interested in retrieving configuration data from native
            # model's ipv6 module. If IPv6 is not enabled, this request returns empty <data> tags
            response = connection.get_config(source="running", filter=("xpath", "native/ipv6")).data_xml

    except Exception as err:
        print("failed!")
        print(err)
        return 1
    
    # Parsing XML formatter response into Python dictionary
    config = xmltodict.parse(response)

    # Checking if IPv6 configuration related keys exist in the returned payload,
    # and printing out correct message based on this
    if not config["data"].get("native"):
        print("No IPv6 configuration present!")
    elif config["data"]["native"].get("ipv6"):
        print("IPv6 configured!")
        print("Configuration:")
        print(response)


if __name__ == "__main__":
    # Update the IP address and credentials to match with your environment

    devices = [
        "198.18.133.101",
        "198.18.7.2",
        "198.18.11.2",
        "198.18.12.2"
    ]

    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }

    for device in devices:
        view_ipv6(device, credentials["username"], credentials["password"])
