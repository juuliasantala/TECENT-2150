#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for retrieving and printing out Catalyst Center
client IPv6 addresses. Note that this API is supported since the
version 2.3.7

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

import requests

requests.urllib3.disable_warnings()

HOST = "https://<YOUR CAT CENTER>"
PASSWORD = "<YOUR PASSWORD>"
USERNAME = "<YOUR USERNAME>"

# Get authentication token

url = f"{HOST}/dna/system/api/v1/auth/token"
response = requests.post(url, auth=(USERNAME, PASSWORD), verify=False)
token = response.json()["Token"]

# Retrieve client data
url = f"{HOST}/dna/data/api/v1/clients"
headers = {"x-auth-token":token}
response = requests.get(url, headers=headers, verify=False)

data = response.json()

for client in data["response"]:
    print(f"Client {client['name']}: IPv6 addresses: {client['ipv6Addresses']}")
