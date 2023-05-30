# Scripts for Chapter 2

All the scripts have been tested against the DevNet reservable sandbox on May 2023: **[IOS XE on Cat 8kv Latest Code](https://devnetsandbox.cisco.com/RM/Diagram/Index/a5823504-3391-47cc-93a4-8bcadc701839?diagramType=Topology)** (Requires login with DevNet credentials)

The scripts use RESTCONF together with an IOS XE native YANG model. The YANG model using IOS XE native model looks like the following when interface IPv6 address is configured:
```
{
    "Cisco-IOS-XE-native:interface": {
        "GigabitEthernet": [
            {
                "name": 2,
                "description": "IPv6 address automation is fun!",
                    "ipv6": {
                        "address": {
                            "prefix-list": [
                                {
                                    "prefix": "2001:db8:2200:001::10/64"
                                }
                            ]
                        },
                    "enable": [None]
                }
            }
        ]
    }
}
```

> **Note**: There are many more settings that can be configured using the Cisco IOS XE native module's `interface` container. For the purpose of this technical seminar's use case, only IPv6 configuration is addressed. When working with RESTCONF `PATCH` method, the existing other interface configuration won't be affected even if they are not included in the payload.

## Update interfaces

In this directory you can find two scripts, `update_interface_config.py` and `update_interface_config_simple.py`, that you can use to configure IPv6 address on your network device(s)'s interface(s).

The **simple version of the script (`update_interface_config_simple.py`)** only configures one interface on one device, doesn't utilize functions, and doesn't include any error handling. It is a great place to start if you are just getting started with your automation journey.

Example of running the script:
```bash
$ python update_interface_config_simple.py
Status code of the request: 204
```

The **main script `update_interface_config.py`** configures all the network devices whose IP address are included in the list `devices` in the end of the file. The targeted interfaces and their details are defined in the list `interfaces` a bit further down after `devices` list. Note to include only interfaces that exist on your device - this specific script has been tested against the DevNet reservable Catalyst 8Kv, but if you are using some other platform, the interfaces might be named differently. If unsure of the correct interface namings for your platform, run first the `view_interface_config.py` (as instructed below) to learn the namings of your device's interfaces.

Compared to the simple version of this script, the main script defines the functionality in a reusable function, and also has a little error handling included to check whether the API call was successful or not.

Example of running the script:
```bash
$ python update_interface_config.py
Configuring interfaces on 10.10.20.48... Success!
```

## Review current interface IP configuration

Script `view_interface_config.py` includes a function to retrieve the current GigabitEthernet interface configuration from the list of devices. If the response code is 200, it means that the API call was successful and GigabitEthernet interfaces have been returned.

To make the outcome more nicely structured on the terminal window, a `for` loop has been included to loop through all the returned interfaces and to check if they have IPv4 and/or IPv6 configured. If the configuration is present, the YANG configuration is printed out in the terminal window.
- If they key `ip` is present in the returned interface configuration, that means that IPv4 address is configured on the device.
- If the key `ipv6` is present in the returned interface configuration, that means that IPv6 address is configured on the device.

Example of running the script:
```bash
$ python view_interface_config.py
Retrieving interface configuration from device 10.10.20.48... Success!

GigabitEthernet 1 ('MANAGEMENT INTERFACE - DON'T TOUCH ME')
- IPv4 address present!
  - Configured: {'primary': {'address': '10.10.20.48', 'mask': '255.255.255.0'}}
  - Actual: 10.10.20.48
- No IPv6 address configured!

GigabitEthernet 2 ('Network Interface')
- No IPv4 address configured!
- No IPv6 address configured!

GigabitEthernet 3 ('Network Interface')
- No IPv4 address configured!
- No IPv6 address configured!
```

After configuring the interfaces, the `view_interface_config.py` shows how the IPv6 interfaces are now present.
```bash
$ python update_interface_config.py
Configuring interfaces on 10.10.20.48... Success!

$ python view_interface_config.py
Retrieving interface configuration from device 10.10.20.48... Success!

GigabitEthernet 1 ('Towards Internet')
- IPv4 address present!
  - Configured: {'primary': {'address': '10.10.20.48', 'mask': '255.255.255.0'}}
  - Actual: 10.10.20.48
- IPv6 address present!
  - Configured: [{'prefix': '2001:db8:2200:001::01/64'}]
  - Actual: fe80::250:56ff:febf:f710, 2001:db8:2200:1::1

GigabitEthernet 2 ('Towards LAN')
- No IPv4 address configured!
- IPv6 address present!
  - Configured: [{'prefix': '2001:db8:2200:001::10/64'}]
  - Actual: None

GigabitEthernet 3 ('Network Interface')
- No IPv4 address configured!
- No IPv6 address configured!
```

## For testing purposes - script to remove IPv6 addresses from interfaces

If during the testing of the script you want to clean up the state of your switch by removing IPv6 addresses from the interfaces, you can use the `remove_ipv6_configuration_from_interface.py` script. It has now been hardcoded to remove the IPv6 configuration from all the interfaces available on the DevNet reservable Catalyst 8Kv switch. If working with another platform or if wanting to remove the configuration only from selected interfaces, update the details in the end of the script (`devices`, `credentials`, and `interfaces`)

Example of running the script:
```bash
$ python remove_ipv6_configuration_from_interface.py 
Removing IPv6 configuration from interface {'type': 'GigabitEthernet', 'number': 1} on device 10.10.20.48... Success!
Removing IPv6 configuration from interface {'type': 'GigabitEthernet', 'number': 2} on device 10.10.20.48... Success!
Removing IPv6 configuration from interface {'type': 'GigabitEthernet', 'number': 3} on device 10.10.20.48... Success!
```
