"""Tool for creating background tasks."""

from __future__ import annotations

from pydantic import BaseModel, Field

from essentials.tasks.manager import get_task_manager
from essentials.tools.base import BaseTool, ToolExecutionContext, ToolResult


class TaskCreateToolInput(BaseModel):
    """Arguments for task creation."""

    description: str = Field(description="Short task description")
    command: str = Field(description="Shell command to run in the background")


class TaskCreateTool(BaseTool):
    """Create a background task."""

    name = "task_create"
    description = "Create a background shell task."
    input_model = TaskCreateToolInput

    async def execute(self, arguments: TaskCreateToolInput, context: ToolExecutionContext) -> ToolResult:
        manager = get_task_manager()
        task = await manager.create_shell_task(
            command=arguments.command,
            description=arguments.description,
            cwd=context.cwd,
        )

        return ToolResult(output=f"Created task {task.id} ({task.type})")
