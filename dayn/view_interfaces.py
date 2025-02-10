#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for viewing IPv6 configuration on GigabitEthernet
interfaces with NETCONF.

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

def view_interface_ipv6(device_ip:str, username:str, password:str, port:int=830, verify:bool=False)->None:
    '''
    Function to view IPv6 configuration on an IOS XE GigabitEthernet interface
    using NETCONF.
    '''
    print(f"\nConnecting to device {device_ip}...", end=" ")

    device = {
        "host": device_ip,
        "port": port,
        "username": username,
        "password": password,
        "hostkey_verify": verify
    }

    filter_config = """
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet/>
        </interface>
      </native>
      """

    filter_oper = """
      <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
          <interface/>
      </interfaces>
      """

    try:
        with manager.connect(**device, device_params={"name":"iosxe"},timeout=10) as connection:
            print("success!")

            response_config = connection.get(filter=("subtree",filter_config)).data_xml
            response_oper = connection.get(filter=("subtree",filter_oper)).data_xml

    except Exception as err:
        print("failed!")
        print(err)
        return 1
    
    # Parsing XML formatter response into Python dictionary
    config = xmltodict.parse(response_config)
    oper = xmltodict.parse(response_oper)

    oper_data = {}

    for interface in oper["data"]["interfaces"]["interface"]:
        oper_data[interface["name"]] = {
            "ipv4": interface["ipv4"] if "ipv4" in interface else None,
            "ipv6": interface["ipv6-addrs"] if "ipv6-addrs" in interface else None}
 
    interfaces_config = config["data"]["native"]["interface"]["GigabitEthernet"]
    
    for interface in interfaces_config:
        print(f"\nGigabitEthernet {interface['name']} (Description: '{interface.get('description')}')")
        interface_oper = oper_data[f"GigabitEthernet{interface['name']}"]

        if "ipv6" in interface:
            ipv6_addresses = interface_oper['ipv6']
            if isinstance(ipv6_addresses, str):
                ipv6_addresses = [ipv6_addresses] 
            print("- IPv6 enabled!")
            print(f'  - Configured address: {interface.get("ipv6").get("address")}')
            print(f'  - Configured neighbor discovery: {interface.get("ipv6").get("nd")}')
            print(f'  - Configured OSPFv3: {interface.get("ipv6").get("ospf")}')
            print(f"  - Actual address: {', '.join(ipv6_addresses) if ipv6_addresses else None}")
            
        else:
            print("- No IPv6 address configured!")
    print(f"\n{'*'*6}")

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
        view_interface_ipv6(device, credentials["username"], credentials["password"])
