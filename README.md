# Opehaina
Opehaina
<pre>
  pip install opehaina
</pre>
Then:
```Python
  # Python
from yaml import safe_load as yl
from opehaina.responses import respond


def get_weather(location):
    # print(f"Executing weather tool for location: {location}")
    return {"temperature": "72F", "condition": "Sunny"}

kwargs = """  # this is a string in YAML format
  max_tokens:   64000
  temperature:  1.0
"""

multilogue = "Compare the weather in Oakland, CA and weather in Paris, France. Use the tool for learning both."

get_weather_tool_str = """  # tool definition (new template)
  type: function
  name: get_weather
  description: Determine weather in a location
  parameters:
    type: object
    properties:
      location:
        type: string
        description: The city and state, e.g. San Francisco, CA
    additionalProperties: false
    required:
      - location
"""

tools = [yl(get_weather_tool_str)]

instructions = """
You are a helpful assistant.
Rubric: respond in plain text without any markdown, emphasis or lists;
all paragraphs except the first one should begin with a newline and a tab.
"""

thoughts, text = respond(
    messages=multilogue,
    instructions=instructions,
    tools=tools,
    **yl(kwargs)
)
```
or
```Python
from yaml import safe_load as yl
from opehaina.chat import chat_complete as cc


kwargs = """  # this is a string in YAML format
  max_tokens:   32000
  stop_sequences:
    - STOP
    - "\nTitle"
  temperature:  1.0
  top_k:        10
  top_p:        0.5
  # thinking:     24576  # thinking tokens budget. 24576
  reasoning_effort: high
"""

instruction = 'You are a helpful assistant. Important: Do not use markdown or lists in your responses.'

get_weather_tool_str = """ # tool description (old)
  type: function
  function:
    name: get_weather
    description: Determine weather in a location
    parameters:
      type: object
      properties:
        location:
          type: string
          description: The city and state, e.g. San Francisco, CA
      additionalProperties: false
      required:
        - location
"""

tools = [yl(get_weather_tool_str)]

msg = [{'role': 'user', 'content': 'What is the weather like in Chicago, IL and Paris, France?'}]

thoughts, text = cc(
    messages=msg,
    instructions=instruction,
    tools=tools,
    **yl(kwargs)
)
```
