# Scripts for Chapter 1

All the scripts have been tested against the DevNet reservable sandbox on May 2023: **[IOS XE on Cat 8kv Latest Code](https://devnetsandbox.cisco.com/RM/Diagram/Index/a5823504-3391-47cc-93a4-8bcadc701839?diagramType=Topology)** (Requires login with DevNet credentials)

The scripts use RESTCONF together with an IOS XE native YANG model. The YANG model using IOS XE native model looks like the following when IPv6 is enabled:
```
{
    'Cisco-IOS-XE-native:ipv6': {
        'unicast-routing': [None]
    }
}
```

## Enable IPv6

In this directory you can find two scripts, `enable_ipv6.py` and `enable_ipv6_simple.py`, that you can use to enable IPv6 on network device(s).

The **simple version of the script (`enable_ipv6_simple.py`)** only configures one device, doesn't utilize functions, and doesn't include any error handling. It is a great place to start if you are just getting started with your automation journey.

Example of running the script:
```bash
$ python enable_ipv6_simple.py
Status code of the request: 204
```

The **main script `enable_ipv6.py`** configures all the network devices whose IP address are included in the list in the end of the file. It defines the functionality in a reusable function, and also has a little error handling included to check whether the API call was successful or not.

Example of running the script:
```bash
$ python enable_ipv6.py
Enabling IPv6 on device 10.10.20.48... Success!
```

## Review current IPv6 configuration

Script `view_ipv6.py` includes a function to retrieve the current IPv6 configuration from the list of devices. If the response code is 204, it means the actual API call was successful, but there was nothing to return from the device. This means IPv6 is not enabled and there is no IPv6 configuration present.

Example of running the script:
```bash
$ python view_ipv6.py
Retrieving IPv6 configuration from device 10.10.20.48... No IPv6 configuration present!

$ python enable_ipv6.py
Enabling IPv6 on device 10.10.20.48... Success!

$ python view_ipv6.py
Retrieving IPv6 configuration from device 10.10.20.48... IPv6 configured!
Configuration:
{'Cisco-IOS-XE-native:ipv6': {'unicast-routing': [None]}}
```

> **Note**
> The YANG payload above means IPv6 is configured. As the older NETCONF supports only XML, the YANG model in JSON format sometimes includes only a key pointing to an empty list to identify that that exists in the device configuration.

## Work with IP address library

Python comes with a library `ipaddress` for IPv4/IPv6 manipulation. The documentation provides details on all of the supported functionalities: https://docs.python.org/3/library/ipaddress.html

To use the library in your code, you simply need to import it:
```python
import ipaddress
```

To see examples of how the library could be used, please look through the `ipaddress_examples.py` script.