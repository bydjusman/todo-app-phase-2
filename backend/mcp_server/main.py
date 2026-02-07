"""
MCP Server for the AI-Powered Todo Chatbot
This server exposes task operations as MCP tools
"""
import asyncio
import json
from typing import Any, Dict, List
from pydantic import BaseModel
from mcp.server import Server
from mcp.types import Tool
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the tools
from app.tools.add_task import AddTaskTool
from app.tools.list_tasks import ListTasksTool
from app.tools.update_task import UpdateTaskTool
from app.tools.complete_task import CompleteTaskTool
from app.tools.delete_task import DeleteTaskTool
from app.database.session import get_session

# Import config directly
import importlib.util
config_spec = importlib.util.spec_from_file_location("config", os.path.join(os.path.dirname(__file__), "config.py"))
config_module = importlib.util.module_from_spec(config_spec)
config_spec.loader.exec_module(config_module)
config = config_module.config


class MCPServer:
    def __init__(self):
        self.server = Server("todo-chatbot-mcp-server")
        self.add_task_tool = AddTaskTool()
        self.list_tasks_tool = ListTasksTool()
        self.update_task_tool = UpdateTaskTool()
        self.complete_task_tool = CompleteTaskTool()
        self.delete_task_tool = DeleteTaskTool()

        # Register tools with the server
        self._register_tools()

    def _register_tools(self):
        """Register all MCP tools with the server."""

        # Define tools for the server
        tools = [
            Tool(
                name="add_task",
                description="Create a new task for the user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "The ID of the user creating the task"},
                        "title": {"type": "string", "description": "The title of the task"},
                        "description": {"type": "string", "description": "Optional description of the task"},
                        "due_date": {"type": "string", "format": "date-time", "description": "Optional due date for the task in ISO 8601 format"}
                    },
                    "required": ["user_id", "title"]
                }
            ),
            Tool(
                name="list_tasks",
                description="Retrieve tasks for the user with optional filtering",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "The ID of the user whose tasks to retrieve"},
                        "status": {"type": "string", "enum": ["pending", "completed", "all"], "description": "Filter tasks by status. Default is 'all'"},
                        "limit": {"type": "integer", "description": "Maximum number of tasks to return. Default is 50"},
                        "offset": {"type": "integer", "description": "Number of tasks to skip. Default is 0"}
                    },
                    "required": ["user_id"]
                }
            ),
            Tool(
                name="update_task",
                description="Update an existing task for the user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "The ID of the user who owns the task"},
                        "task_id": {"type": "integer", "description": "The ID of the task to update"},
                        "title": {"type": "string", "description": "New title for the task (optional)"},
                        "description": {"type": "string", "description": "New description for the task (optional)"},
                        "due_date": {"type": "string", "format": "date-time", "description": "New due date for the task in ISO 8601 format (optional)"}
                    },
                    "required": ["user_id", "task_id"]
                }
            ),
            Tool(
                name="complete_task",
                description="Mark a task as completed",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "The ID of the user who owns the task"},
                        "task_id": {"type": "integer", "description": "The ID of the task to mark as completed"}
                    },
                    "required": ["user_id", "task_id"]
                }
            ),
            Tool(
                name="delete_task",
                description="Delete a task from the user's list",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "The ID of the user who owns the task"},
                        "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            )
        ]

        # Register the tools
        async def list_tools_handler(params):
            return {"tools": [t.model_dump() for t in tools]}

        # Handler for calling tools
        async def call_tool_handler(params):
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            # Call the appropriate tool based on the name
            if tool_name == "add_task":
                with get_session() as db_session:
                    result = await self.add_task_tool.run(
                        session=db_session,
                        **arguments
                    )
            elif tool_name == "list_tasks":
                with get_session() as db_session:
                    result = await self.list_tasks_tool.run(
                        session=db_session,
                        **arguments
                    )
            elif tool_name == "update_task":
                with get_session() as db_session:
                    result = await self.update_task_tool.run(
                        session=db_session,
                        **arguments
                    )
            elif tool_name == "complete_task":
                with get_session() as db_session:
                    result = await self.complete_task_tool.run(
                        session=db_session,
                        **arguments
                    )
            elif tool_name == "delete_task":
                with get_session() as db_session:
                    result = await self.delete_task_tool.run(
                        session=db_session,
                        **arguments
                    )
            else:
                return {"error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}}

            return {"result": result}

        # Add handlers to the server
        self.server.request_handlers["mcp/tool/list"] = list_tools_handler
        self.server.request_handlers["mcp/tool/call"] = call_tool_handler

    async def run(self):
        """Run the MCP server."""
        print("Starting MCP server over stdio...")

        # Use the mcp.stdio_server function to handle stdio communication
        from mcp import stdio_server

        # Create a session with the server
        async with stdio_server() as (read_stream, write_stream):
            # Create initialization options
            initialization_options = self.server.create_initialization_options(
                {"serverInfo": {"name": "todo-chatbot-mcp-server", "version": "1.0.0"}}
            )

            # Run the server
            await self.server.run(
                read_stream,
                write_stream,
                initialization_options,
                raise_exceptions=False
            )


# Main execution
async def main():
    server = MCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())