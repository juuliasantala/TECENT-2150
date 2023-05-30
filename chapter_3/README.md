# Scripts for Chapter 3

All the scripts have been tested against the DevNet reservable sandbox on May 2023: **[IOS XE on Cat 8kv Latest Code](https://devnetsandbox.cisco.com/RM/Diagram/Index/a5823504-3391-47cc-93a4-8bcadc701839?diagramType=Topology)** (Requires login with DevNet credentials)

This chapter includes two topics: 1) decoupling the Python logic from the configuration into template and a source of truth, and 2) an example of test driven automation with pyATS.

## Source of truth

For flexible and scalable automation, your configuration needs to be in an agreed source of truth, from where the automation logic gets the values. A template for the payload is best created in a way that configuration changes need you only to change values in the source of truth, not in the template. The template and values should be decoupled from the actual Python logic.

In this folder, you can find a script `update_interface_config_improved.py` which is otherwise the same as the code in chapter 2, except now with decoupled configuration. In the folder `source of truth` you find the following files:
- `devices.yaml` - here you have the list of devices to be included in the automation, as well as their credentials. **NOTE**: Never push your credentials to GitHub or other remote version control systems!
- `configuration.yaml` - here you have the interface IPv6 configuration for each of the interfaces.
- `template.j2` - here you have a Jinja2 formatted template for the payload to be sent to the devices with the RESTCONF call. Note that it is exactly as the payload you had in Python, just small changes on how the loop and variable syntax is defined. Explanation for the changes:
    - Variables are defined inside two curly brackets `{{variable}}`
    - For loop is defined in curly brackets and % sign: `{% for interface in interfaces %}` and `{% endfor %}`
    - `None` is a Python structure. As the Jinja2 template function returns a JSON string, `null` is used instead

If you want to change any values such as the interface description, make the change in `configuration.yaml` and run the python script:
```bash
$ python update_interface_config_improved.py
Creating configuration from template.j2 and configuration.yaml... Payload created!
Configuring interfaces on 10.10.20.48... Success!
```

## Test Driven Automation

> **Note**: pyATS is supported on Linux, MacOs, and Docker container. If you are working on a Windows system, use the Docker container. pyATS installation documentation can be found [here](https://pubhub.devnetcloud.com/media/pyats-getting-started/docs/install/installpyATS.html).

`ping_test.py` is a simple test case utilizing pyATS test framework as well a pyATS inbuilt `ping` API. When running the test, it reads the `source_of_truth/testbed.yaml` file for the details on how to connect to the device for the testing. In case of the ping test, it would make sense to do the ping from the device where the testscript is stored - therefor pyATS `ping` API connects to the network device based on the details defined in the testbed, and executes the ping from the cli of that device itself.

Testbed is just another source of truth for your network devices. It is slightly more complex looking than the devices.yaml being used on the source of truth part of this chapter - the testbed file follows the model that pyATS is expecting to receive when loading the topology.

Note that by default, there is no default route defined in the DevNet reservable Catalyst 8Kv sandbox. Therefor both the IPv6 and IPv4 ping fail.

Example of running the script:
```bash
$ python ping_test.py 
2023-05-28T14:50:11: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:11: %AETEST-INFO: |                            Starting common setup                             |
2023-05-28T14:50:11: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:11: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:11: %AETEST-INFO: |                         Starting subsection connect                          |
2023-05-28T14:50:11: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:19: %AETEST-INFO: The result of subsection connect is => PASSED
2023-05-28T14:50:19: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:19: %AETEST-INFO: |                  Starting subsection mark_tests_for_looping                  |
2023-05-28T14:50:19: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:19: %AETEST-INFO: The result of subsection mark_tests_for_looping is => PASSED
2023-05-28T14:50:19: %AETEST-INFO: The result of common setup is => PASSED
2023-05-28T14:50:19: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:19: %AETEST-INFO: |      Starting testcase PingTestcase[device=Device_cat8000v,_type_iosxe]      |
2023-05-28T14:50:19: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:19: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:19: %AETEST-INFO: |                            Starting section ping                             |
2023-05-28T14:50:19: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:19: %AETEST-INFO: +..............................................................................+
2023-05-28T14:50:19: %AETEST-INFO: :        Starting STEP 1: Checking Ping from cat8000v to 208.67.222.222        :
2023-05-28T14:50:19: %AETEST-INFO: +..............................................................................+
2023-05-28T14:50:29: %AETEST-ERROR: Failed reason: Ping 208.67.222.222 from device cat8000v unsuccessful
2023-05-28T14:50:29: %AETEST-INFO: The result of STEP 1: Checking Ping from cat8000v to 208.67.222.222 is => FAILED
2023-05-28T14:50:29: %AETEST-INFO: +..............................................................................+
2023-05-28T14:50:29: %AETEST-INFO: :     Starting STEP 2: Checking Ping from cat8000v to 2001:4860:4860::8888     :
2023-05-28T14:50:29: %AETEST-INFO: +..............................................................................+
2023-05-28T14:50:30: %AETEST-ERROR: Failed reason: Ping 2001:4860:4860::8888 from device cat8000v unsuccessful
2023-05-28T14:50:30: %AETEST-INFO: The result of STEP 2: Checking Ping from cat8000v to 2001:4860:4860::8888 is => FAILED
2023-05-28T14:50:30: %AETEST-INFO: +..........................................................+
2023-05-28T14:50:30: %AETEST-INFO: :                       STEPS Report                       :
2023-05-28T14:50:30: %AETEST-INFO: +..........................................................+
2023-05-28T14:50:30: %AETEST-INFO: STEP 1 - Checking Ping from cat8000v to 208.67.222.222Failed    
2023-05-28T14:50:30: %AETEST-INFO: STEP 2 - Checking Ping from cat8000v to 2001:4860:4860::8888Failed    
2023-05-28T14:50:30: %AETEST-INFO: ............................................................
2023-05-28T14:50:30: %AETEST-INFO: The result of section ping is => FAILED
2023-05-28T14:50:30: %AETEST-INFO: The result of testcase PingTestcase[device=Device_cat8000v,_type_iosxe] is => FAILED
2023-05-28T14:50:30: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:30: %AETEST-INFO: |                           Starting common cleanup                            |
2023-05-28T14:50:30: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:30: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:30: %AETEST-INFO: |                        Starting subsection disconnect                        |
2023-05-28T14:50:30: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:41: %AETEST-INFO: The result of subsection disconnect is => PASSED
2023-05-28T14:50:41: %AETEST-INFO: The result of common cleanup is => PASSED
2023-05-28T14:50:41: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:41: %AETEST-INFO: |                               Detailed Results                               |
2023-05-28T14:50:41: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:41: %AETEST-INFO:  SECTIONS/TESTCASES                                                      RESULT   
2023-05-28T14:50:41: %AETEST-INFO: --------------------------------------------------------------------------------
2023-05-28T14:50:41: %AETEST-INFO: .
2023-05-28T14:50:41: %AETEST-INFO: |-- common_setup                                                          PASSED
2023-05-28T14:50:41: %AETEST-INFO: |   |-- connect                                                           PASSED
2023-05-28T14:50:41: %AETEST-INFO: |   `-- mark_tests_for_looping                                            PASSED
2023-05-28T14:50:41: %AETEST-INFO: |-- PingTestcase[device=Device_cat8000v,_type_iosxe]                      FAILED
2023-05-28T14:50:41: %AETEST-INFO: |   `-- ping                                                              FAILED
2023-05-28T14:50:41: %AETEST-INFO: |       |-- Step 1: Checking Ping from cat8000v to 208.67.222.222         FAILED
2023-05-28T14:50:41: %AETEST-INFO: |       `-- Step 2: Checking Ping from cat8000v to 2001:4860:4860::...    FAILED
2023-05-28T14:50:41: %AETEST-INFO: `-- common_cleanup                                                        PASSED
2023-05-28T14:50:41: %AETEST-INFO:     `-- disconnect                                                        PASSED
2023-05-28T14:50:41: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:41: %AETEST-INFO: |                                   Summary                                    |
2023-05-28T14:50:41: %AETEST-INFO: +------------------------------------------------------------------------------+
2023-05-28T14:50:41: %AETEST-INFO:  Number of ABORTED                                                            0 
2023-05-28T14:50:41: %AETEST-INFO:  Number of BLOCKED                                                            0 
2023-05-28T14:50:41: %AETEST-INFO:  Number of ERRORED                                                            0 
2023-05-28T14:50:41: %AETEST-INFO:  Number of FAILED                                                             1 
2023-05-28T14:50:41: %AETEST-INFO:  Number of PASSED                                                             2 
2023-05-28T14:50:41: %AETEST-INFO:  Number of PASSX                                                              0 
2023-05-28T14:50:41: %AETEST-INFO:  Number of SKIPPED                                                            0 
2023-05-28T14:50:41: %AETEST-INFO:  Total Number                                                                 3 
2023-05-28T14:50:41: %AETEST-INFO:  Success Rate                                                             66.7% 
2023-05-28T14:50:41: %AETEST-INFO: --------------------------------------------------------------------------------
```
