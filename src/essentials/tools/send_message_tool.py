"""Tool for writing messages to running agent tasks."""

from __future__ import annotations

import logging

from pydantic import BaseModel, Field

from essentials.swarm.registry import get_backend_registry
from essentials.swarm.types import TeammateMessage
from essentials.tasks.manager import get_task_manager
from essentials.tools.base import BaseTool, ToolExecutionContext, ToolResult

logger = logging.getLogger(__name__)


class SendMessageToolInput(BaseModel):
    """Arguments for sending a follow-up message to a task."""

    to: str = Field(description="Target agent/task identifier. Prefer agent_id values such as name@team.")
    message: str = Field(description="Message to write to the task stdin")


class SendMessageTool(BaseTool):
    """Send a message to a running local agent task."""

    name = "send_message"
    description = "Send a follow-up message to a running local agent task."
    input_model = SendMessageToolInput

    async def execute(self, arguments: SendMessageToolInput, context: ToolExecutionContext) -> ToolResult:
        del context
        target = arguments.to.strip()
        # Swarm agents use agent_id format (name@team); legacy tasks use plain task IDs
        if "@" in target:
            return await self._send_swarm_message(target, arguments.message)
        try:
            await get_task_manager().write_to_task(target, arguments.message)
        except ValueError as exc:
            return ToolResult(output=str(exc), is_error=True)
        return ToolResult(output=f"Sent message to task {target}")

    async def _send_swarm_message(self, agent_id: str, message: str) -> ToolResult:
        """Route a message to a swarm agent via the backend."""
        registry = get_backend_registry()
        # Use subprocess backend to match AgentTool's spawn path.
        # The SubprocessBackend tracks agent_id -> task_id mappings so
        # send_message resolves correctly for any agent spawned by AgentTool.
        executor = registry.get_executor("subprocess")

        teammate_msg = TeammateMessage(text=message, from_agent="coordinator")
        try:
            await executor.send_message(agent_id, teammate_msg)
        except ValueError as exc:
            return ToolResult(output=str(exc), is_error=True)
        except Exception as exc:
            logger.error("Failed to send message to %s: %s", agent_id, exc)
            return ToolResult(output=str(exc), is_error=True)
        return ToolResult(output=f"Sent message to agent {agent_id}")
