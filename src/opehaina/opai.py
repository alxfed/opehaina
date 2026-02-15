# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
import openai

api_key             = environ.get("OPENAI_API_KEY", '')
default_model       = environ.get("OPENAI_DEFAULT_MODEL", 'gpt-5.2')

client = openai.OpenAI()


def stream(messages=None, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    accumulated_output = ""
    accumulated_reasoning = ""
    response_status = None
    accumulated_reasoning_summary=""
    reasoning = {
        "effort": "xhigh",
        "summary": "detailed"
    }
    try:
        with (client.responses.stream(
                model=kwargs.get("model", default_model),
                instructions=kwargs.get("system", "answer concisely"),
                input=messages,
                max_output_tokens=kwargs.get("max_tokens", 10000),
                reasoning=kwargs.get("output_config", reasoning)
        ) as stream):
            for event in stream:
                # Handle output text deltas
                if event.type == "response.created":
                    if hasattr(event, 'delta') and event.delta:
                        accumulated_output += event.delta
                elif event.type == "response.output_item.added":
                    if hasattr(event, 'delta') and event.delta:
                        accumulated_output += event.delta
                elif event.type == "response.output_text.delta":
                    if hasattr(event, 'delta') and event.delta:
                        accumulated_output += event.delta

                # Handle reasoning text deltas (for reasoning models)
                elif event.type == "response.reasoning_summary_text.delta":
                    if hasattr(event, 'delta') and event.delta:
                        accumulated_reasoning += event.delta

                # Handle completion event
                elif event.type == "response.completed":
                    response_status = "completed"
                    # Extract usage information if available
                    if hasattr(event, 'usage') and event.usage:
                        usage_info = {
                            'input_tokens': getattr(event.usage, 'input_tokens', None),
                            'output_tokens': getattr(event.usage, 'output_tokens', None),
                            'total_tokens': getattr(event.usage, 'total_tokens', None),
                        }
                        # Add reasoning tokens if available
                        if hasattr(event.usage, 'reasoning_tokens'):
                            usage_info['reasoning_tokens'] = event.usage.reasoning_tokens

                # Handle failed event
                elif event.type == "response.failed":
                    response_status = "failed"
            ...
        return accumulated_output, accumulated_reasoning

    except Exception as e:
        print("Unable to stream the response")
        print(f"Exception: {e}")
        return ['','']


if __name__ == "__main__":
    messages = [{"role": "user", "content": "Are Language Models seeking the Truth?"}]
    text, thoughts = stream(messages)
    ...
