#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for configuring full IPv6 configuration with Netmiko.

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

from netmiko import ConnectHandler

R3 = {
    'device_type': 'cisco_xe',
    'host': '198.18.11.2',
    'username': 'developer',
    'password': 'C1sco12345'
}

net_connect = ConnectHandler(**R3)

config_commands = [
    'ipv6 unicast-routing',
    'ipv6 router ospf 1',
    'int gig 4',
    'ipv6 enable',
    'ipv6 ospf 1 area 0',
    'int gig 5',
    'ipv6 enable',
    'ipv6 ospf 1 area 0',
    'ipv6 address 2001:420:4021:1BD5::1/64',
    'ipv6 nd prefix 2001:420:4021:1BD5::/64'
]

output = net_connect.send_config_set(config_commands)
print(output)

net_connect.disconnect()

