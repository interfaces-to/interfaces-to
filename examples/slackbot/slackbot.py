# 1️⃣ import `into`
import interfaces_to as into

# 2️⃣ import the OpenAI client as normal
from openai import OpenAI
client = OpenAI()

# 3️⃣ add your favourite tools
tools = into.import_tools(['Slack'])

# 4️⃣ read messages dynamically and start the loop
messages = into.read_messages(['Slack'])
while messages := into.running(messages):

  # 5️⃣ create a completion as normal, and run your tools! 🪄
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto"
  )
  messages = into.run(messages, completion, tools)

# 6️⃣ you just built AI's smartest Slack bot in 10 seconds! 🎩✨