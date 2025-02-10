#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for testing whether an IPv6 address is valid or not.

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

import sys
import ipaddress
from pyats import aetest
import yaml

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2025 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def read_configuration(self, config_file):

        with open(config_file, encoding="utf-8") as my_values:
            config = yaml.safe_load(my_values.read())

        aetest.loop.mark(InterfaceConfigAnalysis, device=config.items())

class InterfaceConfigAnalysis(aetest.Testcase):

    @aetest.setup()
    def mark_interfaces_for_looping(self, device):
    
        aetest.loop.mark(self.validate_address, interface=device[1]["interfaces"])

    @aetest.test
    def validate_address(self, steps, device, interface):

        try:
            addresses = interface["ipv6_address"]
            subnet = interface["nd_prefix"]
        except KeyError:
            self.skipped(f"No IPv6 address configured on {device[0]} {interface}")

        for address in addresses:
            with  steps.start(f"Validating IP address {address} for {interface}", continue_=False) as step:
                try:
                    address_without_prefix = address.split("/")[0]
                    ipaddress.IPv6Address(address_without_prefix)
                except Exception as err:
                    step.failed(f"{address} is not a valid ip address: {err}")
                else:
                    step.passed(f"{address} is a valid ip address")

            with  steps.start(f"Validating subnet for IP address {address}", continue_=True) as step:

                is_in_network = ipaddress.IPv6Address(address_without_prefix) in ipaddress.IPv6Network(subnet)

                if is_in_network:
                    step.passed(f"{address} is in {subnet}")
                else:
                    step.failed(f"{address} NOT in {subnet}")

if __name__ == "__main__":

    result = aetest.main(config_file="sot.yaml")
    if str(result) != "passed":
        sys.exit(1)
