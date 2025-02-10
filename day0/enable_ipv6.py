#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for enabling IPv6 with NETCONF on multiple devices.

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

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2025 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

def enable_ipv6(device_ip, username, password, port=830, verify=False):

    print(f"\nConnecting to device {device_ip}...", end=" ")

    device = {
        "host": device_ip,
        "port": port,
        "username": username,
        "password": password,
        "hostkey_verify": verify
    }

    payload = """
        <config>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <ipv6>
                    <unicast-routing/>
                    <router>
                        <ospf>
                            <id>1</id>
                        </ospf>
                    </router>
                </ipv6>
            </native>
        </config>
    """

    with manager.connect(**device, device_params={"name":"iosxe"},timeout=10) as connection:
        print("success!")
        response = connection.edit_config(target="running", config=payload)
        print(response)

if __name__ == "__main__":
    devices = [
        "198.18.133.101",
        "198.18.11.2",
        "198.18.12.2"
    ]

    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }

    for device in devices:
        enable_ipv6(device, credentials["username"], credentials["password"])
