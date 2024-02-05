#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple Python sample script for enabling IPv6 on one device with RESTCONF.
Please review the other script 'enable_ipv6.py' in this repo to see a more
scalable implementation.

The script has been tested with DevNet reservable sandbox on February 2024:
"IOS XE on Cat 8kv"

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

# requests is a common library to use when automating REST based API calls.
import requests

# DevNet sandbox uses unverified certificate. To remove the warnings from your
# output, the following two lines can be used. DO NOT USE THESE IN PRODUCTION.
import urllib3
urllib3.disable_warnings()

# Define device details. This script targets only one device.
DEVICE = "10.10.20.48"
PASSWORD = "C1sco12345"
USERNAME = "developer"

# This is YANG based payload that will enable IPv6
payload = {
    "Cisco-IOS-XE-native:ipv6": {
        "unicast-routing": [None]
    }
}

# This is the URL targeting the correct configuration endpoint on the IOS XE.
# f-string (indicated with an f before the string) allows us to input a
# variable into our string with {variable_name}.
url = f"https://{DEVICE}:443/restconf/data/Cisco-IOS-XE-native:native/ipv6/"

# Headers define our payloads content-type for IOS XE to know how to read it
header = {"Content-Type": "application/yang-data+json"}

# The RESTCONF call is done using PATCH - this makes sure we don't accidentally overwrite
# existing configuration in case IPv6 was already enabled.
# verify = False is being used as the DevNet sandbox uses unverified SSL certificate.
response = requests.patch(url, headers=header,
                          auth=(USERNAME, PASSWORD),
                          json=payload, verify=False)

# Every REST API call returns a status code: if the code starts with 2, everything is fine,
# otherwise an error occurred.
print(f"Status code of the request: {response.status_code}")
