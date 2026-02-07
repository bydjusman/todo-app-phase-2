"""API Router for MCP Tools"""
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from typing import Dict, Any
from ..database.session import get_session
from ..tools.todo_tools import (
    MCPTools, AddTaskInput, ListTasksInput, UpdateTaskInput,
    DeleteTaskInput, CompleteTaskInput
)

router = APIRouter(prefix="/mcp-tools", tags=["mcp-tools"])


@router.post("/add-task")
async def tool_add_task(input_data: AddTaskInput, session: Session = Depends(get_session)):
    """MCP tool for adding a task"""
    result = MCPTools.addtask01(input_data)
    return result.dict()


@router.post("/list-tasks")
async def tool_list_tasks(input_data: ListTasksInput, session: Session = Depends(get_session)):
    """MCP tool for listing tasks"""
    result = MCPTools.listtask2(input_data)
    return result.dict()


@router.post("/update-task")
async def tool_update_task(input_data: UpdateTaskInput, session: Session = Depends(get_session)):
    """MCP tool for updating a task"""
    result = MCPTools.updatetsk(input_data)
    return result.dict()


@router.post("/complete-task")
async def tool_complete_task(input_data: CompleteTaskInput, session: Session = Depends(get_session)):
    """MCP tool for completing a task"""
    result = MCPTools.complet01(input_data)
    return result.dict()


@router.post("/delete-task")
async def tool_delete_task(input_data: DeleteTaskInput, session: Session = Depends(get_session)):
    """MCP tool for deleting a task"""
    result = MCPTools.deletetsk(input_data)
    return result.dict()


# Unified tool handler that accepts any tool call
@router.post("/execute-tool")
async def execute_tool(tool_name: str, tool_input: Dict[str, Any], session: Session = Depends(get_session)):
    """Generic tool execution endpoint"""
    try:
        if tool_name == "addtask01":
            input_obj = AddTaskInput(**tool_input)
            result = MCPTools.addtask01(input_obj)
        elif tool_name == "listtask2":
            input_obj = ListTasksInput(**tool_input)
            result = MCPTools.listtask2(input_obj)
        elif tool_name == "updatetsk":
            input_obj = UpdateTaskInput(**tool_input)
            result = MCPTools.updatetsk(input_obj)
        elif tool_name == "complet01":
            input_obj = CompleteTaskInput(**tool_input)
            result = MCPTools.complet01(input_obj)
        elif tool_name == "deletetsk":
            input_obj = DeleteTaskInput(**tool_input)
            result = MCPTools.deletetsk(input_obj)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")

        return result.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))