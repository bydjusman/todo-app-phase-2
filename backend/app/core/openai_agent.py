"""
OpenAI Agent Integration for Todo Chatbot
This module integrates the OpenAI Agents SDK with the MCP tools
"""
import os
from typing import Dict, Any, List
from openai import OpenAI
from openai.types.beta.threads.runs.run_step import RunStep
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
import json

class OpenAIAgentService:
    """
    Service class to handle OpenAI Agent interactions and MCP tool integration.
    """

    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Create or get the assistant with MCP tools
        self.assistant = self._create_assistant()

    def _create_assistant(self) -> Assistant:
        """
        Create an OpenAI assistant configured with MCP tools.
        """
        # Define the tools for the assistant
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "The ID of the user creating the task"
                            },
                            "title": {
                                "type": "string",
                                "description": "The title of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional description of the task"
                            }
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve tasks for the user with optional filtering",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "The ID of the user whose tasks to retrieve"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "completed", "all"],
                                "description": "Filter tasks by status. Default is 'all'"
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "The ID of the user who owns the task"
                            },
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to mark as completed"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task from the user's list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "The ID of the user who owns the task"
                            },
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to delete"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "integer",
                                "description": "The ID of the user who owns the task"
                            },
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title for the task (optional)"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description for the task (optional)"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

        # Create or retrieve the assistant
        assistant = self.client.beta.assistants.create(
            name="Todo Chatbot Assistant",
            description="An AI assistant that helps manage todo tasks using natural language",
            model="gpt-4-turbo-preview",  # or gpt-3.5-turbo if preferred
            tools=tools,
            instructions=(
                "You are a helpful assistant for managing todo tasks. "
                "Use the available tools to add, list, update, complete, or delete tasks. "
                "Always confirm actions with the user before performing them. "
                "Be friendly and concise in your responses. "
                "If the user asks for tasks, use the list_tasks tool. "
                "If the user wants to add a task, use the add_task tool. "
                "If the user wants to complete a task, use the complete_task tool. "
                "If the user wants to delete a task, use the delete_task tool. "
                "If the user wants to update a task, use the update_task tool."
            )
        )

        return assistant

    def create_thread(self) -> Thread:
        """
        Create a new thread for a conversation.
        """
        thread = self.client.beta.threads.create()
        return thread

    def process_message(self, thread_id: str, user_message: str, user_id: int) -> str:
        """
        Process a user message in the context of a thread.
        """
        # Add the user's message to the thread
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )

        # Create a run to process the message
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant.id,
            # Pass user_id as metadata or handle it separately
            additional_instructions=f"The current user ID is {user_id}. Use this ID in all tool calls."
        )

        # Wait for the run to complete
        run = self._wait_for_run_completion(thread_id, run.id)

        # Handle any required tool calls
        if run.status == "requires_action" and run.required_action.type == "submit_tool_outputs":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls

            # Execute the required tool calls
            tool_outputs = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Add user_id to function arguments if not present
                if "user_id" not in function_args:
                    function_args["user_id"] = user_id

                # Execute the tool call
                result = self._execute_tool_call(function_name, function_args)

                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": json.dumps(result)
                })

            # Submit the tool outputs
            run = self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

            # Wait for the run to complete again
            run = self._wait_for_run_completion(thread_id, run.id)

        # Get the assistant's response
        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id,
            order="asc"
        )

        # Find the latest assistant message
        assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]
        if assistant_messages:
            last_message = assistant_messages[-1]
            # Extract text content
            text_content = ""
            for content_block in last_message.content:
                if hasattr(content_block, 'text') and content_block.text:
                    text_content += content_block.text.value
            return text_content

        return "I processed your request but couldn't generate a response. Please try again."

    def _wait_for_run_completion(self, thread_id: str, run_id: str) -> Any:
        """
        Wait for a run to complete or require action.
        """
        import time
        while True:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )

            if run.status in ["completed", "failed", "cancelled", "expired", "requires_action"]:
                return run

            time.sleep(0.5)  # Wait 0.5 seconds before checking again

    def _execute_tool_call(self, function_name: str, function_args: Dict[str, Any]) -> Any:
        """
        Execute a tool call locally since we're simulating MCP integration.
        In a real implementation, this would call the MCP server.
        """
        # In a real implementation, this would call the MCP server
        # For now, we'll simulate by calling the appropriate backend function
        from .agent_service import TodoAgentService
        from ..database.session import get_session

        with get_session() as session:
            agent_service = TodoAgentService(session)

            # Map function names to actual tool calls
            if function_name == "add_task":
                return agent_service.tools["add_task"].run(session=session, **function_args)
            elif function_name == "list_tasks":
                return agent_service.tools["list_tasks"].run(session=session, **function_args)
            elif function_name == "complete_task":
                return agent_service.tools["complete_task"].run(session=session, **function_args)
            elif function_name == "delete_task":
                return agent_service.tools["delete_task"].run(session=session, **function_args)
            elif function_name == "update_task":
                return agent_service.tools["update_task"].run(session=session, **function_args)
            else:
                return {"error": f"Unknown function: {function_name}"}

# Singleton instance
openai_agent_service = OpenAIAgentService()