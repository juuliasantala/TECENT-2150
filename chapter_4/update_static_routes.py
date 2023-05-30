#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for updating IPv6 static configuration with RESTCONF.
This script uses Jinja2 template for the payload.

The script has been tested with DevNet reservable sandbox on May 2023:
"IOS XE on Cat 8kv Latest Code"

------------

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
"""

import os
import requests
import urllib3
import jinja2
import yaml

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Following line disables warnings of the unverified certificate. Do not use in production!
urllib3.disable_warnings()

def create_payload_for_routes(template, values):
    '''Create a configuration from Jinja2 template and values from YAML file.'''

    print(f"Creating configuration from {template} and {values}...", end=" ")
    with open(values, encoding="utf-8") as my_values:
        config = yaml.safe_load(my_values.read())
    with open(template, encoding="utf-8") as my_template:
        template = jinja2.Template(my_template.read())

    configuration_payload = template.render(routes=config["Routes"])
    print("Payload created!")
    return configuration_payload

def configure_routes(device_ip:str, username:str, password:str,
                         payload:str,
                         port:int=443, verify:bool=False)->None:
    '''
    Function to configure IPv6 static routes on an IOS XE device using RESTCONF.
    '''
    print(f"Configuring routes on {device_ip}...", end=" ")

    url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-native:native/ipv6"
    header = {"Content-Type": "application/yang-data+json"}

    response = requests.patch(url, headers=header, auth=(username, password),
                              data=payload, verify=verify)

    if response.status_code in (200, 204):
        print("Success!")
    else:
        print("Error!")
        print(response.text)

if __name__ == "__main__":
    device_file = os.path.join("source_of_truth", "devices.yaml")
    configuration_file = os.path.join("source_of_truth", "configuration.yaml")
    template_file = os.path.join("source_of_truth", "template.j2")

    with open(device_file, encoding="utf-8") as device_file:
        devices = yaml.safe_load(device_file.read())

    route_payload = create_payload_for_routes(template_file, configuration_file)

    for device in devices["devices"]:
        configure_routes(device["address"],
                         devices["credentials"]["username"],
                         devices["credentials"]["password"],
                         route_payload)
