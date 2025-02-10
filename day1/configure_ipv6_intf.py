#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for configuring IPv6 on one device's interfaces
with NETCONF.

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

def configure_ipv6_on_intf(device_ip,
                           username,
                           password,
                           ipv6_address,
                           nd_prefix,
                           port=830,
                           verify=False):

    print(f"\nConnecting to device {device_ip}...", end=" ")

    device = {
        "host": device_ip,
        "port": port,
        "username": username,
        "password": password,
        "hostkey_verify": verify
    }

    payload = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>4</name>
            <ipv6>
              <enable/>
              <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospfv3">
                <process>
                  <id>1</id>
                  <area>0</area>
                </process>
              </ospf>
            </ipv6>
          </GigabitEthernet>
          <GigabitEthernet>
            <name>5</name>
            <ipv6>
              <enable/>
              <address>
                <prefix-list>
                  <prefix>{ipv6_address}</prefix>
                </prefix-list>
              </address>
              <nd>
                <prefix xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-nd">
                  <ipv6-prefix-list>
                    <ipv6-prefix>{nd_prefix}</ipv6-prefix>
                  </ipv6-prefix-list>
                </prefix>
              </nd>
              <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospfv3">
                <process>
                  <id>1</id>
                  <area>0</area>
                </process>
              </ospf>
            </ipv6>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """

    with manager.connect(**device, device_params={"name":"iosxe"},timeout=10) as connection:
        print("success!")
        response = connection.edit_config(target="running", config=payload)
        print(response)

if __name__ == "__main__":

    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }

    R3 = "198.18.11.2"

    R3_configuration = {"address": "2001:420:4021:1a45::1/64", "nd": "2001:420:4021:1a45::/64"}

    configure_ipv6_on_intf(R3, credentials["username"], credentials["password"],
                           R3_configuration["address"], R3_configuration["nd"])
