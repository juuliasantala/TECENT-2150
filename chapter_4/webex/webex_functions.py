#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Webex sample function to send and retrieve messages using a bot.

This script is out of scope in the technical seminar. The purpose of the
script is to inspire with further possibilities in you automation
journey.

This script is highly customized to answer to one specific use case. Keep
that in mind when utilizing it to setup your own Webex cards.

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

import json
import requests
import jinja2

from . import webex_config

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

CARD = """
{
    "contentType": "application/vnd.microsoft.card.adaptive",
    "content": {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.2",
        "body": [
            {
                "type": "TextBlock",
                "text": "Cisco Live US 2023",
                "weight": "Bolder",
                "size": "Medium"
            },
            {
                "type": "ColumnSet",
                "columns": [
                    {
                        "type": "Column",
                        "width": "stretch",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "{{ data.topic }}",
                                "weight": "Bolder",
                                "wrap": true,
                                "color": "Good"
                            },
                            {
                                "type": "TextBlock",
                                "spacing": "None",
                                "text": "{{ data.subtopic}}",
                                "isSubtle": true,
                                "wrap": true
                            }
                        ]
                    }
                ]
            },
            {
                "type": "FactSet",
                "facts": [
                    {
                        "title": "{{ data.pre_test.title }}",
                        "value": "{{ data.pre_test.value }}"
                    }
                ]
            },
            {% for description in data.pre_test.description %}
            {
                "type": "TextBlock",
                "text": "{{ description }}",
                "wrap": true
            },
            {% endfor %}
            {
                "type": "FactSet",
                "facts": [
                    {
                        "title": "{{ data.post_test.title }}",
                        "value": "{{ data.post_test.value }}"
                    }
                ]
            }{% for description in data.post_test.description%},
            {
                "type": "TextBlock",
                "text": "{{ description }}",
                "wrap": true
            }{% endfor %}
        ]
    }
}
"""

def send_summary_card(pre_test:dict,
                      post_test:dict,
                      template:str=CARD
                      )->bool:
    '''
    Function to call after the configuration change and tests are completed in main.py.
    '''
    if not webex_config.send_webex_message:
        print("Not sending a Webex message!")
        return False
    
    token = webex_config.webex_token
    email = webex_config.my_email
    try:
        card_payload = _create_card_payload(card_template=template, pre_test=pre_test, post_test=post_test)
        _send_card(token=token, email=email, card=card_payload)
        return True
    except Exception as e:
        print(f"Error occurred while sending the card :\n{e}")
        return False


def _send_card(token:str, email:str, card:dict)->None:
    '''
    Function to send a Webex message 1:1 based on an email address.
    '''
    print(f"Sending a card to {email}")
    url = "https://webexapis.com/v1/messages"
    headers = {"authorization":f"Bearer {token}", "Content-Type":"application/json"}
    payload = {
        "toPersonEmail":email,
        "text": "This is a card",
        "attachments":[card]
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f"Status code of sending the Webex message: {response.status_code}")

    if str(response.status_code)[0] != "2":
        raise Exception(f"Error: {response.text}")


def _create_card_payload(card_template:str, pre_test:dict, post_test:dict):
    '''Create a card payload from Jinja2 template and values from YAML file.'''

    pre_test_description = [f"- **Ping test** on {router} (**Passed**: {', '.join(results['Passed']) or 'None'}, **Failed**: {', '.join(results['Failed']) or 'None'})"
                            for router, results in pre_test["details"].items()]
    # pre_test_description = '\n'.join(pre_test_description)

    post_test_description = [f"- **Ping test** on {router} (**Passed**: {', '.join(results['Passed']) or 'None'}, **Failed**: {', '.join(results['Failed']) or 'None'})"
                             for router, results in post_test["details"].items()]
    # post_test_description = '\n'.join(post_test_description)

    card_data = {
        "topic": "Configuration change completed",
        "subtopic": "IPv6 static route update",
        "pre_test": {
            "title": "Pre-test",
            "value":pre_test['overall_result'],
            "description":pre_test_description
        },
        "post_test": {
            "title": "Post-test",
            "value":post_test['overall_result'],
            "description":post_test_description
        }
    }

    template = jinja2.Template(card_template)
    try:
        card = template.render(data=card_data)
        return json.loads(card)
    except:
        raise Exception("Card creation failed.")


