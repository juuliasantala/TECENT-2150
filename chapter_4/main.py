#!/usr/bin/env python
'''
Example script to make change static routes with test-driven approach.
Before and after the change, a test is ran, to signify whether tests pass or not.

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

import os
from testcases import ping_test
import update_static_routes
import helper_functions
import webex

__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

def main():
    '''
    Function to test and configure IPv6 static routes.
    '''

    # 1. Define paths to files used in the configuration
    configuration_file = os.path.join("source_of_truth", "configuration.yaml")
    template_file = os.path.join("source_of_truth", "template.j2")

    # 2. Get the dictionary formatted details of devices to be configured / tested
    devices = helper_functions.get_yaml_data_from_source_of_truth(file_name="devices.yaml")

    # 3. Get the dictionary formatted details for the tests
    # (in this case, the IP addresses for the ping test)
    test_config = helper_functions.get_yaml_data_from_source_of_truth(file_name="test_config.yaml")

    # 4. Dynamically create the testbed
    my_testbed = helper_functions.create_testbed(devices)

    # 5. Run the Pre test (Ping test) -> this should fail as you have not configured routes yet
    print("\n**********\nStarting the pre-test...")
    pre_test = ping_test.run(testbed=my_testbed, destinations=test_config["Ping_test"]["destinations"])

    # 6. Run the functions to configure the static routes on the network device(s)
    print("\n**********\nStarting the configuration change...")
    route_payload = update_static_routes.create_payload_for_routes(template_file, configuration_file)
    for device in devices["devices"]:
        update_static_routes.configure_routes(device["address"],
                         devices["credentials"]["username"],
                         devices["credentials"]["password"],
                         route_payload)

    # 7. Rerun the test -> now it should pass as route is configured.
    # (Note! When run against DevNet sandbox, this test will not pass)
    print("\n**********\nStarting the post-test...")
    post_test = ping_test.run(testbed=my_testbed, destinations=test_config["Ping_test"]["destinations"])

    # 8. Sending out a Webex card based on the outcome.
    webex.send_summary_card(pre_test=pre_test, post_test=post_test)

if __name__ == "__main__":
    main()