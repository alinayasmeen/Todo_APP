---
name: chat-kit
description: Guides the creation and integration of chat interfaces and components using Chat Kit for AI-driven conversations.
---

# Chat Kit

## Instructions

1. Set up the Chat Kit framework or SDK in your frontend or backend project.
2. Design conversation flows, message types, and UI components for chat interactions.
3. Integrate AI agents (e.g., OpenAI) with Chat Kit for real-time responses.
4. Handle user input validation, formatting, and session management.
5. Implement features like message history, typing indicators, and notifications.
6. Ensure responsive and accessible UI for all devices.
7. Monitor chat performance and debug issues with message delivery or AI responses.
8. Document chat workflows, API endpoints, and configuration settings.

## Examples

- Initializing a Chat Kit interface:

  ```javascript
  import { Chat } from "chat-kit";

  const chat = new Chat({
      container: "#chat-container",
      userId: "user123",
      agent: aiAgent
  });
  ```

- Sending a message and receiving AI response:

  ```javascript
  const response = await agent.run("Summarize this document in 3 sentences.");
  console.log(response.output);
  ```

- Sending a task to the agent:

  ```javascript
  const response = await agent.run("Summarize this document in 3 sentences.");
  console.log(response.output);
  ```
