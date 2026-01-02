---
name: openai-agents
description: Guides the creation, configuration, and deployment of OpenAI-powered agents for intelligent system workflows.
---

# OpenAI Agents

## Instructions

1. Determine the task or workflow that requires AI capabilities.
2. Choose the appropriate OpenAI model (e.g., GPT-4, GPT-5) for the agent’s purpose.
3. Configure prompts, instructions, and parameters for the agent to achieve desired outputs.
4. Integrate the agent with backend systems, APIs, or databases.
5. Handle inputs, outputs, and error cases robustly.
6. Monitor agent performance and adjust prompts or configurations as needed.
7. Ensure outputs comply with ethical, security, and privacy standards.
8. Document agent behavior, parameters, and integration details.

## Examples

- Creating a text-generation agent:

  ```python
  from openai import OpenAI
  client = OpenAI(api_key="YOUR_API_KEY")
  
  response = client.chat.completions.create(
      model="gpt-5-mini",
      messages=[{"role":"user","content":"Summarize this document"}]
  )
  print(response.choices[0].message.content)

Integrating agent into backend API:

python
Copy code
@app.post("/generate-summary")
async def generate_summary(text: str):
    return agent.generate(text)
Monitoring agent usage and performance:

lua
Copy code
Track response times, error rates, and output quality
