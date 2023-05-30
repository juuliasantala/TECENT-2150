#!/usr/bin/env python
'''
Helper functions for Chapter 4 content.
This script includes functions to read the data from devices.yaml, as well
as to create dynamically a pyATS testbed. The function to create a testbed
expects the data to come exactly in the format that is defined in devices.yaml.

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

__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

def get_yaml_data_from_source_of_truth(file_name:str):
    '''
    This function reads a yaml file from source_of_truth folder, and returns
    a dictionary including the contents of the file.
    '''
    import os, yaml

    yaml_file = os.path.join("source_of_truth", file_name)
    with open(yaml_file, encoding="utf-8") as file:
        content = yaml.safe_load(file.read())
    return content

def create_testbed(devices:dict):
    '''
    This function creates and returns dynamically a pyATS testbed from a dictionary.
    Note that this script expects the data in dictionary to be in the
    following format:

        {
            "devices": [
                "hostname": "string",
                "address": "ip or domain",
                "ssh_port: number # this is optional! use if ssh port is not default 22
            ],
            "credentials": {
                "username": "string",
                "password: "string"
            }
        }
    '''
    from pyats.topology import Testbed

    testbed = Testbed("Dynamically created testbed")
    testbed.credentials["default"] = {
        "username": devices["credentials"]["username"],
        "password":devices["credentials"]["password"]
    }

    for device in devices["devices"]:
        device_config = {
            "hostname":device["hostname"],
            "address":device["address"]
        }
        if "ssh_port" in device:
            device_config["ssh_port"] = device["ssh_port"]

        new_device = _create_ios_xe_device(**device_config)
        new_device.testbed = testbed
    
    return testbed

def _create_ios_xe_device(hostname:str,
                          address:str,
                          ssh_port:int=22):
    '''
    This is an internal function called by create_testbed.
    This function will create the device specific testbed configuration.
    '''
    from pyats.topology import Device

    os = "iosxe" 
    connections = {
        "cli": {
            "ip": address,
            "protocol": "ssh",
            "port": ssh_port
        }
    }

    device = Device(hostname, os=os, connections=connections)
    return device
