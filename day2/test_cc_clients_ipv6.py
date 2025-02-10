#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for testing with pyATS whether clients have IPv6 addresses.
Note that this API is supported since the version 2.3.7

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

from pyats import aetest
import requests

class CommonSetup(aetest.CommonSetup):
    '''
    Common setup tasks - this class is instantiated only once per testscript.
    '''
    test_data = None

    @aetest.subsection
    def cc_authenticate(self, cc_creds):
        auth = (cc_creds["username"], cc_creds["password"])
        url = f"{cc_creds['url']}/dna/system/api/v1/auth/token"

        response = requests.post(url, auth=auth, verify=False)

        if response.ok:
            self.token = response.json()["Token"]
            self.passed()
        else:
            self.failed(f"Issue while getting token: {response.text}")


    @aetest.subsection
    def get_data(self, cc_creds):
        url = f"{cc_creds['url']}/dna/data/api/v1/clients"
        headers = {
            "x-auth-token":self.token,
            "X-CALLER-ID":"pyATS"
        }

        try:
            response = requests.get(url, headers=headers, verify=False)

            if response.ok:
                self.data = response.json()
                print(self.data)
                self.passed()
            else:
                self.failed(f"Issue while getting clients: {response.text}")
        except Exception as err:
            self.failed(f"Issue while executing API call: {err}")

    @aetest.subsection
    def mark_tests_for_looping(self):
        """
        device_list includes details (name and uuid) for each of the devices
        whose interface configuration is to be tested.
        This method loops through all the devices in the device_list and calls
        the test InterfaceConfigTestcase on all of them one by one.
        """
        aetest.loop.mark(Ipv6ClientTestcase, client=self.data)

class Ipv6ClientTestcase(aetest.Testcase):
    '''
    Simple Testcase for checking port status using Cisco Catalyst Center.
    '''

    @aetest.test
    def validate_client_ipv6_addresses(self, steps, client):
        '''
        Retrieve interface configuration from Catalyst Center for the selected device
        '''
        client_username = client["username"]
        client_type = client["type"]
        ipv6_addresses = client["ipv6Addresses"]

        with  steps.start(
            f"Checking for link local on {client_username}({client_type})",
            continue_=False
        ) as step:
            if ipv6_addresses:
                for address in ipv6_addresses:
                    if "fe80" in address:
                        step.passed(f"✅ Link local address present: {address} ✅")
            else:
                step.failed("❌ Link local address NOT present ❌")

        with  steps.start(
            f"Checking for other addresses on {client_username}({client_type})",
            continue_=True
        ) as step:
            
            if len(ipv6_addresses) > 1:
                step.passed(f"✅ Multiple addresses present: {ipv6_addresses} ✅")
            else:
                step.failed("❌ One or less addresses present ❌")

class CommonCleanup(aetest.CommonCleanup):
    '''
    Common cleanup tasks - this class is instantiated only once per testscript.
    '''
    @aetest.subsection
    def cleanup(self):
        ''' No cleanup needed for this Catalyst Center testcase '''
        pass

if __name__ == "__main__":

    cat_creds = {
        "url": "https://<YOUR CAT CENTER>",
        "username":"<YOUR USERNAME>",
        "password": "<YOUR PASSWORD>"
    }

    aetest.main(cc_creds=cat_creds)
