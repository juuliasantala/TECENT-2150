#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Examples on using ipaddress library with IPv6.
https://docs.python.org/3/library/ipaddress.html

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

import ipaddress

# 1. Validating your IPv6 address

# By using the IPv6Address class, you can validate if an IPv6 address is
# a valid address. If it is not a valid address, an AddressValueError will
# be raised.
# By placing this verification in the "try-expect" structure, we can gracefully
# catch the error when it is raised, without crashing the script.

print("VALIDATE ADDRESS!")

my_address = "2001:c0f3::1234::1"

try:
    ipv6_address = ipaddress.IPv6Address(my_address)
except ipaddress.AddressValueError as error:
    print(f"Alert! {my_address} is not a valid IPv6 address!")
    print(error)

# 2. Are these addresses in the network?

# In addition to IPv6Address, the library has also IPv6Network class that allows
# actions on the network level. You can easily test with this structure whether
# certain IPv6 addresses belong to this network.

print("\nARE THESE ADDRESSES IN THE NETWORK?")
my_network = ipaddress.IPv6Network("2001:db8:16::0/124")

router_1 = ipaddress.IPv6Address("2001:db8:16::9")
router_2 = ipaddress.IPv6Address("2001:db8:16::10")

if router_1 in my_network:
    print(f"{router_1} is in the network {my_network}")
else:
    print(f"{router_1} is NOT in the network {my_network}")

if router_2 in my_network:
    print(f"{router_2} is in the network {my_network}")
else:
    print(f"{router_2} is NOT in the network {my_network}")


# 3. Loop through all the IPv6 addresses in the network

# Using the IPv6Network from the previous example, you can loop through
# all the available addresses.

print("\nWHAT ADDRESSES IN A NETWORK?")
for address in my_network:
    print(address)

# 4. How many addresses in a network?

# IPv6Network supports the method num_addresses which gives the count of addresses
# in the network
print("\nHOW MANY ADDRESSES IN THE NETWORK?")
my_network = ipaddress.IPv6Network("2001:db8::0/126")
print(my_network.num_addresses)
