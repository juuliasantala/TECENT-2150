#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for configuring interfaces using YAML SoT and Jinja2 templates
together with NETCONF.

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

from ncclient import manager
import yaml
import jinja2

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2025 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


def read_configuration_template(config_file):
    with open(config_file, encoding="utf-8") as my_values:
        config = yaml.safe_load(my_values.read())
    return config

def render_template(interfaces, template_name):
    with open(template_name, encoding="utf-8") as my_template:
        template = jinja2.Template(my_template.read())

    configuration = template.render(interfaces=interfaces)
    return configuration

def configure_ipv6_on_intf(device_ip,
                           username,
                           password,
                           configuration,
                           port=830,
                           verify=False):

    print(f"\nConnecting to device {device_ip}...", end=" ")

    device = {
        "host": device_ip,
        "port": port,
        "username": username,
        "password": password,
        "hostkey_verify": verify
    }

    payload = configuration

    with manager.connect(**device, device_params={"name":"iosxe"},timeout=10) as connection:
        print("success!")
        response = connection.edit_config(target="running", config=payload)
        print(response)

if __name__ == "__main__":

    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }

    config_values = read_configuration_template("sot.yaml")

    for values in config_values.values():
        config = render_template(values["interfaces"], "interface_template.j2")
        configure_ipv6_on_intf(values["mgmt"], credentials["username"], credentials["password"],
                               config)
