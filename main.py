import asyncio
import requests

import ollama
from ollama import ChatResponse
from datetime import datetime

# own
from src.utils.Math import *

# prefix = 'SYSTEM """Current time is: ' + str(current_date.strftime('%A')) + ', ' + str(current_date) + '""" '

# # response: ChatResponse = chat(model='personal-assistant', messages=[
# #   {
# #     'role': 'user',
# #     'content': prefix + 'Kannst du mir die aktuelle Zeit, Datum und Wochentag nennen?',
# #     'stream': True,
# #   },
# # ])
# # print(response.message.content)

# stream = chat(
#     model='personal-assistant',
#     messages=[{'role': 'user', 'content': prefix + 'Kannst du mir die aktuelle Zeit, Datum und Wochentag nennen?'}],
#     stream=True,
# )

# for chunk in stream:
#   print(chunk['message']['content'], end='', flush=True)

def get_todays_date() -> str:
  """
  Get todays weekday, date and time

  Returns:
    str: The current weekday, date and time
  """
  current_date = datetime.now()
  return f'{current_date.strftime("%A")}, {current_date.strftime("%d.%m.%Y")} {current_date.strftime("%H:%M:%S")}'

def get_genshin_redeem_codes():
  """
  Get the html contents of a website that contains all the current active and expired redeem codes for Genshin Impact

  Args:
    None

  Returns:
    str: The html contents of the website
  """
  response = requests.get('https://www.gamesradar.com/genshin-impact-codes-redeem/')
  return response.text


# Tools can still be manually defined and passed into chat
subtract_two_numbers_tool = {
  'type': 'function',
  'function': {
    'name': 'subtract_two_numbers',
    'description': 'Subtract two numbers',
    'parameters': {
      'type': 'object',
      'required': ['a', 'b'],
      'properties': {
        'a': {'type': 'integer', 'description': 'The first number'},
        'b': {'type': 'integer', 'description': 'The second number'},
      },
    },
  },
}

# messages = [{'role': 'user', 'content': 'What is three plus one?'}]
# messages = [{'role': 'user', 'content': 'Was ist heute für ein Wochentag?'}]
messages = [{'role': 'user', 'content': 'Gib mir alle aktuellen Genshin Impact redeem codes'}]
print('Prompt:', messages[0]['content'])

available_functions = {
  'add_two_numbers': add_two_numbers,
  'subtract_two_numbers': subtract_two_numbers,
  'get_todays_date': get_todays_date,
  'get_genshin_redeem_codes': get_genshin_redeem_codes,
}


async def main():
  client = ollama.AsyncClient()

  response: ChatResponse = await client.chat(
    'llama3.1:8b',
    messages=messages,
    tools=[add_two_numbers, subtract_two_numbers_tool, get_todays_date, get_genshin_redeem_codes],
  )

  if response.message.tool_calls:
    # There may be multiple tool calls in the response
    for tool in response.message.tool_calls:
      # Ensure the function is available, and then call it
      if function_to_call := available_functions.get(tool.function.name):
        print('Calling function:', tool.function.name)
        print('Arguments:', tool.function.arguments)
        output = function_to_call(**tool.function.arguments)
        print('Function output:', output)
      else:
        print('Function', tool.function.name, 'not found')

  # Only needed to chat with the model using the tool call results
  if response.message.tool_calls:
    # Add the function response to messages for the model to use
    messages.append(response.message)
    messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

    # Get final response from model with function outputs
    final_response = await client.chat('llama3.1:8b', messages=messages)
    print('Final response:', final_response.message.content)

  else:
    print('No tool calls returned from model')


if __name__ == '__main__':
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print('\nGoodbye!')