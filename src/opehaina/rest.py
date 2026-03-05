# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import requests
from os import environ

api_key             = environ.get("OPENAI_API_KEY", '')
default_model       = environ.get("OPENAI_DEFAULT_MODEL", 'gpt-5.2')
api_base            = environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key,
}


def respond(messages=None, instructions=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    accumulated_output = ""
    accumulated_reasoning = ""
    instruction = kwargs.get("system_instruction", instructions),
    json_data = {
        "model":            kwargs.get("model", default_model),
        "instructions":     instruction,
        "input":            messages,
        "max_output_tokens": kwargs.get("max_tokens", 10000),
        "reasoning": {
            "effort": "xhigh",
            "summary": "detailed"
        }
    }
    try:
        response = requests.post(
            f"{api_base}/responses",
            headers=headers,
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            for part in response.json()['output']:
                if part['type'] == 'message':
                    for chunk in part['content']:
                        accumulated_output += chunk['text']
                elif part['type'] == 'reasoning':
                    for chunk in part['summary']:
                        accumulated_reasoning += chunk['text']
        else:
            print(f"API Request status code: {response.status_code}")

        return accumulated_reasoning, accumulated_output

    except Exception as e:
        print("Unable to generate Response")
        print(f"Exception: {e}")

        return accumulated_reasoning, accumulated_output


if __name__ == "__main__":
    messages = [{"role": "user", "content": "Are Language Models seeking the Truth?"}]
    thoughts, text = respond(messages)
    ...
