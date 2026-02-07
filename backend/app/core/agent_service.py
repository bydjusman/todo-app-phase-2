from typing import Dict, Any, List
from sqlmodel import Session, select
from datetime import datetime
import json
import re
from ..tools.add_task import AddTaskTool
from ..tools.list_tasks import ListTasksTool
from ..models.conversation_entry import ConversationEntry


class TodoAgentService:
    """
    Service class to handle AI agent interactions and tool invocation.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        # Initialize tools
        self.tools = {
            "add_task": AddTaskTool(),
            "list_tasks": ListTasksTool()
        }

        # Lazy load other tools to avoid import errors if they don't exist yet
        try:
            from ..tools.update_task import UpdateTaskTool
            self.tools["update_task"] = UpdateTaskTool()
        except ImportError:
            pass

        try:
            from ..tools.complete_task import CompleteTaskTool
            self.tools["complete_task"] = CompleteTaskTool()
        except ImportError:
            pass

        try:
            from ..tools.delete_task import DeleteTaskTool
            self.tools["delete_task"] = DeleteTaskTool()
        except ImportError:
            pass

    async def process_message(self, user_id: int, message: str, conversation_id: int) -> str:
        """
        Process a user message and return an appropriate response.
        This is a simplified implementation that maps natural language to tool calls.
        In a real implementation, this would use an AI agent like OpenAI's Functions.
        """
        # First, get conversation history to provide context
        conversation_history = await self._get_conversation_history(conversation_id)

        # Simple natural language processing to determine intent
        message_lower = message.lower().strip()

        # Intent detection logic
        if any(word in message_lower for word in ["add", "create", "new task", "make"]):
            return await self._handle_add_task_intent(user_id, message)
        elif any(word in message_lower for word in ["list", "show", "view", "pending", "completed", "all"]):
            return await self._handle_list_tasks_intent(user_id, message)
        elif any(word in message_lower for word in ["update", "change", "edit", "modify"]):
            return await self._handle_update_task_intent(user_id, message)
        elif any(word in message_lower for word in ["complete", "finish", "done", "mark as"]):
            return await self._handle_complete_task_intent(user_id, message)
        elif any(word in message_lower for word in ["delete", "remove", "erase", "cancel"]):
            return await self._handle_delete_task_intent(user_id, message)
        elif any(word in message_lower for word in ["what have", "which have", "tell me about", "show completed"]):
            # Handle ambiguous requests for completed tasks
            if any(word in message_lower for word in ["completed", "done", "finished"]):
                return await self._handle_list_tasks_intent(user_id, "list completed tasks")
            else:
                return await self._handle_ambiguous_request(user_id, message)
        else:
            # Default response for unrecognized commands
            return f"I understand you said: '{message}'. For task management, you can ask me to add tasks, list tasks, update tasks, mark tasks as complete, or delete tasks."

    async def _get_conversation_history(self, conversation_id: int) -> List[Dict[str, str]]:
        """
        Retrieve conversation history for context.
        """
        stmt = (
            select(ConversationEntry)
            .where(ConversationEntry.conversation_id == conversation_id)
            .order_by(ConversationEntry.timestamp)
        )
        entries = self.db_session.exec(stmt).all()

        history = []
        for entry in entries:
            history.append({
                "role": entry.role,
                "content": entry.content,
                "timestamp": entry.timestamp.isoformat()
            })

        return history

    async def _handle_add_task_intent(self, user_id: int, message: str) -> str:
        """
        Handle intent to add a task.
        """
        # Extract task title from message (simple parsing)
        # Look for phrases like "add task to buy groceries" or "create task X"
        import re

        # Try to extract the task title from the message
        # Look for patterns like "add task to X" or "create task X" or "add X task"
        patterns = [
            r"add\s+(?:a\s+|)\w*\s*to\s+(.+)",
            r"create\s+(?:a\s+|)\w*\s*(?:to\s+|for\s+|)(.+)",
            r"add\s+(.+)"
        ]

        task_title = None
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                task_title = match.group(1).strip()
                break

        if not task_title:
            # If we can't extract the title, ask for clarification
            return "I heard you wanted to add a task, but I couldn't determine what task to add. Could you please specify what task you'd like to add?"

        # Call the add_task tool
        tool_result = await self.tools["add_task"].run(
            session=self.db_session,
            user_id=user_id,
            title=task_title,
            description=message
        )

        if tool_result.get("success"):
            task = tool_result["task"]
            return f"Great! I've added the task '{task['title']}' to your list. Task ID is {task['id']}."
        else:
            error_msg = tool_result.get("error", "Unknown error occurred")
            return f"Sorry, I couldn't add the task. Error: {error_msg}"

    async def _handle_list_tasks_intent(self, user_id: int, message: str) -> str:
        """
        Handle intent to list tasks.
        """
        # Determine what kind of tasks to list based on the message
        status_filter = "all"  # default
        if "pending" in message.lower():
            status_filter = "pending"
        elif "completed" in message.lower():
            status_filter = "completed"

        # Call the list_tasks tool
        tool_result = await self.tools["list_tasks"].run(
            session=self.db_session,
            user_id=user_id,
            status=status_filter
        )

        if tool_result.get("success"):
            tasks = tool_result["tasks"]

            if not tasks:
                if status_filter == "pending":
                    return "You don't have any pending tasks right now."
                elif status_filter == "completed":
                    return "You don't have any completed tasks right now."
                else:
                    return "You don't have any tasks in your list."

            # Format the response
            if status_filter == "all":
                response = f"You have {len(tasks)} tasks in total:\n"
            elif status_filter == "pending":
                response = f"You have {len(tasks)} pending tasks:\n"
            elif status_filter == "completed":
                response = f"You have {len(tasks)} completed tasks:\n"

            for i, task in enumerate(tasks, 1):
                status_emoji = "✅" if task["status"] == "completed" else "📝"
                response += f"{i}. {status_emoji} [{task['id']}] {task['title']}\n"

            return response.strip()
        else:
            error_msg = tool_result.get("error", "Unknown error occurred")
            return f"Sorry, I couldn't retrieve your tasks. Error: {error_msg}"

    async def _handle_update_task_intent(self, user_id: int, message: str) -> str:
        """
        Handle intent to update a task.
        """
        # Extract task ID and new details from message
        import re

        # Pattern to match "update task [ID] to [NEW DETAILS]"
        pattern = r"(?:update|change|edit|modify)\s+task\s+(\d+)\s+(?:to|with|as)\s+(.+)"
        match = re.search(pattern, message.lower())

        if not match:
            # Alternative pattern for "change task [ID] to [NEW DETAILS]"
            pattern = r"(?:change|modify|edit)\s+task\s+(\d+)\s+(?:to|with|as)\s+(.+)"
            match = re.search(pattern, message.lower())

        if match:
            task_id = int(match.group(1))
            new_details = match.group(2).strip()

            # Check if the update_task tool is available
            if "update_task" in self.tools:
                tool_result = await self.tools["update_task"].run(
                    session=self.db_session,
                    user_id=user_id,
                    task_id=task_id,
                    title=new_details
                )

                if tool_result.get("success"):
                    task = tool_result["task"]
                    return f"I've updated task {task['id']} to '{task['title']}'."
                else:
                    error_msg = tool_result.get("error", "Unknown error occurred")
                    return f"Sorry, I couldn't update the task. Error: {error_msg}"
            else:
                return "I understand you want to update a task, but the update feature is not available yet."

        return "I heard you wanted to update a task, but I couldn't understand the format. Please say something like 'update task 1 to buy groceries'."

    async def _handle_complete_task_intent(self, user_id: int, message: str) -> str:
        """
        Handle intent to complete a task.
        """
        # Extract task ID from message
        import re

        # Pattern to match "complete task [ID]" or "mark task [ID] as complete"
        pattern = r"(?:complete|finish|done|completed|mark as complete|mark complete|mark as done)\s+task\s+(\d+)"
        match = re.search(pattern, message.lower())

        if not match:
            # Alternative pattern for just numbers after certain words
            pattern = r"(?:complete|finish|done|completed|mark as complete|mark complete|mark as done).*(\d+)"
            match = re.search(pattern, message.lower())

        if match:
            task_id = int(match.group(1))

            # Check if the complete_task tool is available
            if "complete_task" in self.tools:
                tool_result = await self.tools["complete_task"].run(
                    session=self.db_session,
                    user_id=user_id,
                    task_id=task_id
                )

                if tool_result.get("success"):
                    task = tool_result["task"]
                    return f"I've marked task {task['id']} '{task['title']}' as completed."
                else:
                    error_msg = tool_result.get("error", "Unknown error occurred")
                    return f"Sorry, I couldn't complete the task. Error: {error_msg}"
            else:
                return "I understand you want to complete a task, but the complete feature is not available yet."

        return "I heard you wanted to complete a task, but I couldn't identify which task. Please say something like 'complete task 1' or 'mark task 2 as complete'."

    async def _handle_delete_task_intent(self, user_id: int, message: str) -> str:
        """
        Handle intent to delete a task.
        """
        # Extract task ID from message
        import re

        # Pattern to match "delete task [ID]" or "remove task [ID]"
        pattern = r"(?:delete|remove|erase|cancel)\s+task\s+(\d+)"
        match = re.search(pattern, message.lower())

        if not match:
            # Alternative pattern for just numbers after delete/remove words
            pattern = r"(?:delete|remove|erase|cancel).*(\d+)"
            match = re.search(pattern, message.lower())

        if match:
            task_id = int(match.group(1))

            # Check if the delete_task tool is available
            if "delete_task" in self.tools:
                tool_result = await self.tools["delete_task"].run(
                    session=self.db_session,
                    user_id=user_id,
                    task_id=task_id
                )

                if tool_result.get("success"):
                    return f"I've deleted task {task_id}."
                else:
                    error_msg = tool_result.get("error", "Unknown error occurred")
                    return f"Sorry, I couldn't delete the task. Error: {error_msg}"
            else:
                return "I understand you want to delete a task, but the delete feature is not available yet."

        return "I heard you wanted to delete a task, but I couldn't identify which task. Please say something like 'delete task 1' or 'remove task 2'."

    async def _handle_ambiguous_request(self, user_id: int, message: str) -> str:
        """
        Handle ambiguous commands by listing relevant tasks and asking for clarification.
        """
        # For now, list all pending tasks as a way to handle ambiguous requests
        # Call the list_tasks tool to get pending tasks
        tool_result = await self.tools["list_tasks"].run(
            session=self.db_session,
            user_id=user_id,
            status="pending"
        )

        if tool_result.get("success"):
            tasks = tool_result["tasks"]

            if not tasks:
                return "You don't have any pending tasks right now. What would you like to do?"

            # Format the response to list tasks and ask for clarification
            response = f"I found {len(tasks)} pending tasks. Which one did you mean?\n"
            for i, task in enumerate(tasks, 1):
                response += f"{i}. [{task['id']}] {task['title']}\n"

            response += "\nPlease specify which task by mentioning its number or name."
            return response.strip()
        else:
            error_msg = tool_result.get("error", "Unknown error occurred")
            return f"Sorry, I couldn't retrieve your tasks to clarify. Error: {error_msg}"

    async def invoke_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Invoke a specific tool by name with the given arguments.
        """
        if tool_name not in self.tools:
            return {"success": False, "error": f"Tool '{tool_name}' not found"}

        tool = self.tools[tool_name]
        return await tool.run(session=self.db_session, **kwargs)

    async def process_message_with_tools(self, user_id: int, message: str, conversation_id: int, conversation_history: List[Dict[str, str]]) -> tuple[str, List[Dict[str, Any]]]:
        """
        Process a user message with full tool integration and return both response and tool calls.
        This method implements the stateless request cycle as specified in Phase 3.
        """
        # Simple natural language processing to determine intent
        message_lower = message.lower().strip()

        # Track tool calls made during processing
        tool_calls = []

        # Intent detection logic with tool invocation
        if any(word in message_lower for word in ["add", "create", "new task", "make"]):
            result = await self._handle_add_task_intent_with_tools(user_id, message)
            tool_calls.append({"name": "add_task", "arguments": {"message": message}})
            return result, tool_calls
        elif any(word in message_lower for word in ["list", "show", "view", "pending", "completed", "all"]):
            result = await self._handle_list_tasks_intent_with_tools(user_id, message)
            status_filter = "all"
            if "pending" in message_lower:
                status_filter = "pending"
            elif "completed" in message_lower:
                status_filter = "completed"
            tool_calls.append({"name": "list_tasks", "arguments": {"status": status_filter}})
            return result, tool_calls
        elif any(word in message_lower for word in ["update", "change", "edit", "modify"]):
            result = await self._handle_update_task_intent_with_tools(user_id, message)
            tool_calls.append({"name": "update_task", "arguments": {"message": message}})
            return result, tool_calls
        elif any(word in message_lower for word in ["complete", "finish", "done", "mark as"]):
            result = await self._handle_complete_task_intent_with_tools(user_id, message)
            tool_calls.append({"name": "complete_task", "arguments": {"message": message}})
            return result, tool_calls
        elif any(word in message_lower for word in ["delete", "remove", "erase", "cancel"]):
            result = await self._handle_delete_task_intent_with_tools(user_id, message)
            tool_calls.append({"name": "delete_task", "arguments": {"message": message}})
            return result, tool_calls
        elif any(word in message_lower for word in ["what have", "which have", "tell me about", "show completed"]):
            # Handle ambiguous requests for completed tasks
            if any(word in message_lower for word in ["completed", "done", "finished"]):
                result = await self._handle_list_tasks_intent_with_tools(user_id, "list completed tasks")
                tool_calls.append({"name": "list_tasks", "arguments": {"status": "completed"}})
                return result, tool_calls
            else:
                result = await self._handle_ambiguous_request_with_tools(user_id, message)
                return result, tool_calls
        else:
            # Default response for unrecognized commands
            result = f"I understand you said: '{message}'. For task management, you can ask me to add tasks, list tasks, update tasks, mark tasks as complete, or delete tasks."
            return result, tool_calls

    async def _handle_add_task_intent_with_tools(self, user_id: int, message: str) -> str:
        """
        Handle intent to add a task with proper tool invocation.
        """
        # Extract task title from message (simple parsing)
        import re

        # Try to extract the task title from the message
        # Look for patterns like "add task to buy groceries" or "create task X"
        patterns = [
            r"add\s+(?:a\s+|)\w*\s*to\s+(.+)",
            r"create\s+(?:a\s+|)\w*\s*(?:to\s+|for\s+|)(.+)",
            r"add\s+(.+)"
        ]

        task_title = None
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                task_title = match.group(1).strip()
                break

        if not task_title:
            # If we can't extract the title, ask for clarification
            return "I heard you wanted to add a task, but I couldn't determine what task to add. Could you please specify what task you'd like to add?"

        # Call the add_task tool
        tool_result = await self.tools["add_task"].run(
            session=self.db_session,
            user_id=user_id,
            title=task_title,
            description=message
        )

        if tool_result.get("success"):
            task = tool_result["task"]
            return f"Great! I've added the task '{task['title']}' to your list. Task ID is {task['id']}."
        else:
            error_msg = tool_result.get("error", "Unknown error occurred")
            return f"Sorry, I couldn't add the task. Error: {error_msg}"

    async def _handle_list_tasks_intent_with_tools(self, user_id: int, message: str) -> str:
        """
        Handle intent to list tasks with proper tool invocation.
        """
        # Determine what kind of tasks to list based on the message
        status_filter = "all"  # default
        if "pending" in message.lower():
            status_filter = "pending"
        elif "completed" in message.lower():
            status_filter = "completed"

        # Call the list_tasks tool
        tool_result = await self.tools["list_tasks"].run(
            session=self.db_session,
            user_id=user_id,
            status=status_filter
        )

        if tool_result.get("success"):
            tasks = tool_result["tasks"]

            if not tasks:
                if status_filter == "pending":
                    return "You don't have any pending tasks right now."
                elif status_filter == "completed":
                    return "You don't have any completed tasks right now."
                else:
                    return "You don't have any tasks in your list."

            # Format the response
            if status_filter == "all":
                response = f"You have {len(tasks)} tasks in total:\n"
            elif status_filter == "pending":
                response = f"You have {len(tasks)} pending tasks:\n"
            elif status_filter == "completed":
                response = f"You have {len(tasks)} completed tasks:\n"

            for i, task in enumerate(tasks, 1):
                status_emoji = "✅" if task["status"] == "completed" else "📝"
                response += f"{i}. {status_emoji} [{task['id']}] {task['title']}\n"

            return response.strip()
        else:
            error_msg = tool_result.get("error", "Unknown error occurred")
            return f"Sorry, I couldn't retrieve your tasks. Error: {error_msg}"

    async def _handle_update_task_intent_with_tools(self, user_id: int, message: str) -> str:
        """
        Handle intent to update a task with proper tool invocation.
        """
        # Extract task ID and new details from message
        import re

        # Pattern to match "update task [ID] to [NEW DETAILS]"
        pattern = r"(?:update|change|edit|modify)\s+task\s+(\d+)\s+(?:to|with|as)\s+(.+)"
        match = re.search(pattern, message.lower())

        if not match:
            # Alternative pattern for "change task [ID] to [NEW DETAILS]"
            pattern = r"(?:change|modify|edit)\s+task\s+(\d+)\s+(?:to|with|as)\s+(.+)"
            match = re.search(pattern, message.lower())

        if match:
            task_id = int(match.group(1))
            new_details = match.group(2).strip()

            # Check if the update_task tool is available
            if "update_task" in self.tools:
                tool_result = await self.tools["update_task"].run(
                    session=self.db_session,
                    user_id=user_id,
                    task_id=task_id,
                    title=new_details
                )

                if tool_result.get("success"):
                    task = tool_result["task"]
                    return f"I've updated task {task['id']} to '{task['title']}'."
                else:
                    error_msg = tool_result.get("error", "Unknown error occurred")
                    return f"Sorry, I couldn't update the task. Error: {error_msg}"
            else:
                return "I understand you want to update a task, but the update feature is not available yet."

        return "I heard you wanted to update a task, but I couldn't understand the format. Please say something like 'update task 1 to buy groceries'."

    async def _handle_complete_task_intent_with_tools(self, user_id: int, message: str) -> str:
        """
        Handle intent to complete a task with proper tool invocation.
        """
        # Extract task ID from message
        import re

        # Pattern to match "complete task [ID]" or "mark task [ID] as complete"
        pattern = r"(?:complete|finish|done|completed|mark as complete|mark complete|mark as done)\s+task\s+(\d+)"
        match = re.search(pattern, message.lower())

        if not match:
            # Alternative pattern for just numbers after certain words
            pattern = r"(?:complete|finish|done|completed|mark as complete|mark complete|mark as done).*(\d+)"
            match = re.search(pattern, message.lower())

        if match:
            task_id = int(match.group(1))

            # Check if the complete_task tool is available
            if "complete_task" in self.tools:
                tool_result = await self.tools["complete_task"].run(
                    session=self.db_session,
                    user_id=user_id,
                    task_id=task_id
                )

                if tool_result.get("success"):
                    task = tool_result["task"]
                    return f"I've marked task {task['id']} '{task['title']}' as completed."
                else:
                    error_msg = tool_result.get("error", "Unknown error occurred")
                    return f"Sorry, I couldn't complete the task. Error: {error_msg}"
            else:
                return "I understand you want to complete a task, but the complete feature is not available yet."

        return "I heard you wanted to complete a task, but I couldn't identify which task. Please say something like 'complete task 1' or 'mark task 2 as complete'."

    async def _handle_delete_task_intent_with_tools(self, user_id: int, message: str) -> str:
        """
        Handle intent to delete a task with proper tool invocation.
        """
        # Extract task ID from message
        import re

        # Pattern to match "delete task [ID]" or "remove task [ID]"
        pattern = r"(?:delete|remove|erase|cancel)\s+task\s+(\d+)"
        match = re.search(pattern, message.lower())

        if not match:
            # Alternative pattern for just numbers after delete/remove words
            pattern = r"(?:delete|remove|erase|cancel).*(\d+)"
            match = re.search(pattern, message.lower())

        if match:
            task_id = int(match.group(1))

            # Check if the delete_task tool is available
            if "delete_task" in self.tools:
                tool_result = await self.tools["delete_task"].run(
                    session=self.db_session,
                    user_id=user_id,
                    task_id=task_id
                )

                if tool_result.get("success"):
                    return f"I've deleted task {task_id}."
                else:
                    error_msg = tool_result.get("error", "Unknown error occurred")
                    return f"Sorry, I couldn't delete the task. Error: {error_msg}"
            else:
                return "I understand you want to delete a task, but the delete feature is not available yet."

        return "I heard you wanted to delete a task, but I couldn't identify which task. Please say something like 'delete task 1' or 'remove task 2'."

    async def _handle_ambiguous_request_with_tools(self, user_id: int, message: str) -> str:
        """
        Handle ambiguous commands by listing relevant tasks and asking for clarification.
        """
        # For now, list all pending tasks as a way to handle ambiguous requests
        # Call the list_tasks tool to get pending tasks
        tool_result = await self.tools["list_tasks"].run(
            session=self.db_session,
            user_id=user_id,
            status="pending"
        )

        if tool_result.get("success"):
            tasks = tool_result["tasks"]

            if not tasks:
                return "You don't have any pending tasks right now. What would you like to do?"

            # Format the response to list tasks and ask for clarification
            response = f"I found {len(tasks)} pending tasks. Which one did you mean?\n"
            for i, task in enumerate(tasks, 1):
                response += f"{i}. [{task['id']}] {task['title']}\n"

            response += "\nPlease specify which task by mentioning its number or name."
            return response.strip()
        else:
            error_msg = tool_result.get("error", "Unknown error occurred")
            return f"Sorry, I couldn't retrieve your tasks to clarify. Error: {error_msg}"