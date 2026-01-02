---
name: openai-sdk
description: Guides the use of OpenAI SDK for integrating AI capabilities into applications, including chat, text generation, and embeddings.
---

# OpenAI SDK

## Instructions
1. Set up the OpenAI SDK with your API key and environment.
2. Choose the appropriate model (e.g., GPT-4, GPT-5-mini) for the task.
3. Send prompts or tasks to the model using SDK methods.
4. Handle responses, errors, and rate limits effectively.
5. Integrate AI outputs with backend systems, databases, or front-end applications.
6. Monitor usage, latency, and output quality.
7. Ensure compliance with privacy, security, and ethical guidelines.
8. Document integration, API endpoints, and workflows.

## Examples
- Initializing OpenAI SDK:
  ```python
  from openai import OpenAI
  client = OpenAI(api_key="YOUR_API_KEY")
  ```

- Creating a chat completion:
  ```python
  response = client.chat.completions.create(
      model="gpt-5-mini",
      messages=[{"role":"user","content":"Summarize this article"}]
  )
  print(response.choices[0].message.content)
  ```

- Generating embeddings:
  ```python
  embeddings = client.embeddings.create(
      model="text-embedding-3-large",
      input="Text to embed"
  )
  ```