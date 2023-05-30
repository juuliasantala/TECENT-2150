#!/usr/bin/env python
'''
Functional validation ("Does it work?") to test connectivity by executing
a simple pyATS ping test.

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
'''

from pyats import aetest

__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"


class CommonSetup(aetest.CommonSetup):
    '''
    Common setup tasks - this class is instantiated only once per testscript.
    '''

    @aetest.subsection
    def connect(self, testbed):
        '''
        First setup task: connect to all devices in the testbed
        '''
        testbed.connect(log_stdout=False)
        # If your script fails, change log_stdout=True to see more details on what is going on

    @aetest.subsection
    def mark_tests_for_looping(self, testbed):
        '''
        Each iteration of the marked Testcase will be passed the parameter
        "device" with the current device from the testbed.
        '''
        aetest.loop.mark(PingTestcase, device=testbed)

class PingTestcase(aetest.Testcase):
    '''
    Simple Testcase for checking connectivity from the network devices.
    '''

    @aetest.test
    def ping(self, steps, device, destinations, results):
        '''
        Simple ping test: using pyats API "ping", try pinging each of the IP addresses
        in the destinations tuple. If the ping is successful, the test step is marked passed,
        but if the ping is unsuccessful, the step is marked as failed.
        '''
        results[device.hostname] = {"Passed":[], "Failed":[]}
        for destination in destinations:
            with steps.start(
                f"Checking Ping from {device.hostname} to {destination}", continue_=True
                ) as step:
                try:
                    device.ping(destination)
                except:
                    results[device.hostname]["Failed"].append(destination)
                    step.failed(f'Ping {destination} from device {device.hostname} unsuccessful')
                else:
                    results[device.hostname]["Passed"].append(destination)
                    step.passed(f'Ping {destination} from device {device.hostname} successful')


class CommonCleanup(aetest.CommonCleanup):
    '''
    Common cleanup tasks - this class is instantiated only once per testscript.
    '''
    @aetest.subsection
    def disconnect(self, testbed):
        '''
        A method to be executed during common cleanup is defined under
        @aetest.subsection
        '''
        testbed.disconnect()

def run(testbed, destinations):
    '''
    Function to call the ping test.

    The summary of results can be collected to the test_results dictionary because a Dictionary is
    a mutable Python structure. This means that the changes done to it in the tests are saved into
    the same dictionary that has been initialized in the run function.
    '''
    results = {}
    ping_test = aetest.main(
                testable=__name__,
                testbed=testbed,
                destinations=destinations,
                results=results
            )
    return {"overall_result":ping_test, "details":results}
