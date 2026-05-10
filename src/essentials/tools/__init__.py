"""Built-in tool registration."""

from essentials.tools.ask_user_question_tool import AskUserQuestionTool
from essentials.tools.agent_tool import AgentTool
from essentials.tools.bash_tool import BashTool
from essentials.tools.base import BaseTool, ToolExecutionContext, ToolRegistry, ToolResult
from essentials.tools.brief_tool import BriefTool
from essentials.tools.config_tool import ConfigTool
from essentials.tools.cron_create_tool import CronCreateTool
from essentials.tools.cron_delete_tool import CronDeleteTool
from essentials.tools.cron_list_tool import CronListTool
from essentials.tools.cron_toggle_tool import CronToggleTool
from essentials.tools.enter_plan_mode_tool import EnterPlanModeTool
from essentials.tools.exit_plan_mode_tool import ExitPlanModeTool
from essentials.tools.file_edit_tool import FileEditTool
from essentials.tools.file_read_tool import FileReadTool
from essentials.tools.file_write_tool import FileWriteTool
from essentials.tools.glob_tool import GlobTool
from essentials.tools.grep_tool import GrepTool
from essentials.tools.list_mcp_resources_tool import ListMcpResourcesTool
from essentials.tools.lsp_tool import LspTool
from essentials.tools.mcp_auth_tool import McpAuthTool
from essentials.tools.mcp_tool import McpToolAdapter
from essentials.tools.notebook_edit_tool import NotebookEditTool
from essentials.tools.read_mcp_resource_tool import ReadMcpResourceTool
from essentials.tools.remote_trigger_tool import RemoteTriggerTool
from essentials.tools.send_message_tool import SendMessageTool
from essentials.tools.skill_tool import SkillTool
from essentials.tools.sleep_tool import SleepTool
from essentials.tools.task_create_tool import TaskCreateTool
from essentials.tools.task_get_tool import TaskGetTool
from essentials.tools.task_list_tool import TaskListTool
from essentials.tools.task_output_tool import TaskOutputTool
from essentials.tools.task_stop_tool import TaskStopTool
from essentials.tools.todo_write_tool import TodoWriteTool
from essentials.tools.tool_search_tool import ToolSearchTool
from essentials.tools.web_fetch_tool import WebFetchTool
from essentials.tools.web_search_tool import WebSearchTool


def create_default_tool_registry(mcp_manager=None) -> ToolRegistry:
    """Return the default built-in tool registry."""
    registry = ToolRegistry()
    for tool in (
        BashTool(),
        AskUserQuestionTool(),
        FileReadTool(),
        FileWriteTool(),
        FileEditTool(),
        NotebookEditTool(),
        LspTool(),
        McpAuthTool(),
        GlobTool(),
        GrepTool(),
        SkillTool(),
        ToolSearchTool(),
        WebFetchTool(),
        WebSearchTool(),
        ConfigTool(),
        BriefTool(),
        SleepTool(),
        TodoWriteTool(),
        EnterPlanModeTool(),
        ExitPlanModeTool(),
        CronCreateTool(),
        CronListTool(),
        CronDeleteTool(),
        CronToggleTool(),
        RemoteTriggerTool(),
        TaskCreateTool(),
        TaskGetTool(),
        TaskListTool(),
        TaskStopTool(),
        TaskOutputTool(),
        AgentTool(),
        SendMessageTool(),
    ):
        registry.register(tool)
    if mcp_manager is not None:
        registry.register(ListMcpResourcesTool(mcp_manager))
        registry.register(ReadMcpResourceTool(mcp_manager))
        for tool_info in mcp_manager.list_tools():
            registry.register(McpToolAdapter(mcp_manager, tool_info))
    return registry


__all__ = [
    "BaseTool",
    "ToolExecutionContext",
    "ToolRegistry",
    "ToolResult",
    "create_default_tool_registry",
]
