#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample Ping test for connectivity testing.

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
from pyats import aetest, topology
import yaml

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2025 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

class PingTestcase(aetest.Testcase):
    '''
    Simple Testcase for checking connectivity from the network devices.
    '''

    @aetest.setup
    def connect(self, testbed, destinations_file):

        with open(destinations_file, encoding="utf-8") as file:
            self.destinations = yaml.safe_load(file.read())

        testbed.connect(log_stdout=False)
        aetest.loop.mark(self.ping, device=testbed)
    
    @aetest.test
    def ping(self, steps, device):
        for destination in self.destinations:
            with steps.start(
                f"Checking Ping from {device.hostname} to {destination}", continue_=True
                ) as step:
                try:
                    device.ping(destination)
                except:
                    step.failed(f'Ping {destination} from device {device.hostname} unsuccessful')
                else:
                    step.passed(f'Ping {destination} from device {device.hostname} successful')

    @aetest.cleanup
    def disconnect(self, testbed):
        testbed.disconnect()

if __name__ == "__main__":

    my_testbed = topology.loader.load("testbed.yaml")

    result = aetest.main(testbed=my_testbed, destinations_file="ping_destinations.yaml")
    if str(result) != "passed":
        sys.exit(1)

