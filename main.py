from datetime import datetime
from ollama import chat
from ollama import ChatResponse

current_date = datetime.today()

prefix = 'SYSTEM """Current time is: ' + str(current_date.strftime('%A')) + ', ' + str(current_date) + '""" '

response: ChatResponse = chat(model='personal-assistant', messages=[
  {
    'role': 'user',
    'content': prefix + 'Kannst du mir die aktuelle Zeit, Datum und Wochentag nennen?',
  },
])
print(response.message.content)