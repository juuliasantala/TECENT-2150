#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for enabling IPv6 with Netmiko on one device.

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

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2025 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

R2 = {
    'device_type': 'cisco_xe',
    'host': '198.18.7.2',
    'username': 'developer',
    'password': 'C1sco12345'
}

net_connect = ConnectHandler(**R2)

config_commands = [
    'ipv6 unicast-routing',
    'ipv6 router ospf 1'
]

output = net_connect.send_config_set(config_commands)
print(output)

net_connect.disconnect()