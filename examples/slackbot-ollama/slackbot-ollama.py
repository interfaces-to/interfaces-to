# 1️⃣ import `into`
import interfaces_to as into

# 2️⃣ import the OpenAI client and set the base_url to ollama
from openai import OpenAI
client = OpenAI(
  base_url="http://localhost:11434/v1"
)

# 3️⃣ add your favourite tools and read mesaages from Slack
agent = into.Agent().add_tools(['Slack','OpenAI']).add_messages(["Slack"])

# 4️⃣ start the agent loop, with an OpenAI completion
while agent:
  agent.completion = client.chat.completions.create(
    model="llama3.1:8b",
    messages=agent.messages,
    tools=agent.tools,
    tool_choice="auto"
  )

# 5️⃣ watch the magic happen! 🎩✨