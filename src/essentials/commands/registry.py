"""Slash command registry for the essentials build."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Awaitable, Callable, Iterable, Protocol

from essentials.plugins.types import PluginCommandDefinition
from essentials.skills.loader import load_skill_registry

if TYPE_CHECKING:
    from essentials.engine.messages import ConversationMessage
    from essentials.engine.query_engine import QueryEngine
    from essentials.services.session_backend import SessionBackend
    from essentials.state import AppStateStore
    from essentials.tools.base import ToolRegistry


CommandHandler = Callable[[str, "CommandContext"], Awaitable["CommandResult"]]


class MemoryCommandBackend(Protocol):
    """Optional memory backend passed through runtime command context."""


@dataclass(slots=True)
class CommandResult:
    """Result returned by a slash command handler."""

    message: str = ""
    clear_screen: bool = False
    replay_messages: list[ConversationMessage] | None = None
    refresh_runtime: bool = False
    submit_prompt: str | None = None
    submit_model: str | None = None
    continue_pending: bool = False
    continue_turns: int | None = None
    should_exit: bool = False


@dataclass(slots=True)
class CommandContext:
    """Runtime state exposed to slash command handlers."""

    engine: QueryEngine
    hooks_summary: str
    mcp_summary: str
    plugin_summary: str
    cwd: str
    tool_registry: ToolRegistry
    app_state: AppStateStore
    session_backend: SessionBackend
    session_id: str
    extra_skill_dirs: tuple[str, ...] = ()
    extra_plugin_roots: tuple[str, ...] = ()
    memory_backend: MemoryCommandBackend | None = None
    include_project_memory: bool = True


@dataclass(slots=True)
class SlashCommand:
    """A registered slash command."""

    name: str
    description: str
    handler: CommandHandler
    aliases: tuple[str, ...] = ()
    remote_invocable: bool = False
    remote_admin_opt_in: bool = False


@dataclass(slots=True)
class CommandRegistry:
    """Name-based slash command registry."""

    _commands: dict[str, SlashCommand] = field(default_factory=dict)
    _lookup: dict[str, SlashCommand] = field(default_factory=dict)

    def register(self, command: SlashCommand) -> None:
        self._commands[command.name] = command
        self._lookup[command.name] = command
        for alias in command.aliases:
            self._lookup[alias] = command

    def list_commands(self) -> list[SlashCommand]:
        return [self._commands[name] for name in sorted(self._commands)]

    def lookup(self, raw_input: str) -> tuple[SlashCommand, str] | None:
        text = raw_input.strip()
        if not text.startswith("/"):
            return None
        body = text[1:].strip()
        if not body:
            return None
        name, _, args = body.partition(" ")
        command = self._lookup.get(name)
        if command is None:
            return None
        return command, args.strip()


async def _help_handler(_: str, context: CommandContext) -> CommandResult:
    del context
    lines = [
        "Available slash commands:",
        "/help - Show available slash commands",
        "/clear - Clear the current conversation",
        "/pwd - Show current working directory",
        "/hooks - Show active hooks summary",
        "/mcp - Show configured MCP servers",
        "/plugins - Show loaded plugins",
        "/memory - Show project memory status",
        "/continue - Continue a pending tool loop",
        "/exit - Exit the session",
        "",
        "User-invocable skills are also available as `/<skill-name>`.",
    ]
    return CommandResult(message="\n".join(lines))


async def _clear_handler(_: str, context: CommandContext) -> CommandResult:
    context.engine.clear()
    return CommandResult(message="Conversation cleared.", clear_screen=True)


async def _pwd_handler(_: str, context: CommandContext) -> CommandResult:
    return CommandResult(message=context.cwd)


async def _hooks_handler(_: str, context: CommandContext) -> CommandResult:
    return CommandResult(message=context.hooks_summary)


async def _mcp_handler(_: str, context: CommandContext) -> CommandResult:
    return CommandResult(message=context.mcp_summary)


async def _plugins_handler(_: str, context: CommandContext) -> CommandResult:
    return CommandResult(message=context.plugin_summary)


async def _memory_handler(_: str, context: CommandContext) -> CommandResult:
    state = "enabled" if context.include_project_memory else "disabled"
    return CommandResult(message=f"Project memory is {state}.")


async def _continue_handler(args: str, context: CommandContext) -> CommandResult:
    if not context.engine.has_pending_continuation():
        return CommandResult(message="No pending tool loop to continue.")
    turn_count: int | None = None
    raw = args.strip()
    if raw:
        try:
            turn_count = int(raw)
        except ValueError:
            return CommandResult(message="Usage: /continue [COUNT]")
        if turn_count <= 0:
            return CommandResult(message="Usage: /continue [COUNT]")
    return CommandResult(continue_pending=True, continue_turns=turn_count)


async def _exit_handler(_: str, context: CommandContext) -> CommandResult:
    del context
    return CommandResult(message="Goodbye.", should_exit=True)


def _strip_frontmatter(content: str) -> str:
    if content.startswith("---\n"):
        end_index = content.find("\n---\n", 4)
        if end_index != -1:
            return content[end_index + 5 :].lstrip()
    return content.strip()


def _build_prompt(content: str, args: str) -> str:
    body = _strip_frontmatter(content)
    if args:
        return f"{body}\n\nAdditional user input:\n{args}"
    return body


def _plugin_handler(command: PluginCommandDefinition) -> CommandHandler:
    async def _handle(args: str, context: CommandContext) -> CommandResult:
        del context
        return CommandResult(
            submit_prompt=_build_prompt(command.content, args),
            submit_model=command.model,
        )

    return _handle


def _builtin_commands() -> list[SlashCommand]:
    return [
        SlashCommand(name="help", description="Show available slash commands.", handler=_help_handler),
        SlashCommand(name="clear", description="Clear the current conversation.", handler=_clear_handler),
        SlashCommand(name="pwd", description="Show the current working directory.", handler=_pwd_handler),
        SlashCommand(name="hooks", description="Show active hooks summary.", handler=_hooks_handler),
        SlashCommand(name="mcp", description="Show configured MCP servers.", handler=_mcp_handler),
        SlashCommand(name="plugins", description="Show loaded plugins.", handler=_plugins_handler),
        SlashCommand(name="memory", description="Show project memory status.", handler=_memory_handler),
        SlashCommand(name="continue", description="Continue a pending tool loop.", handler=_continue_handler),
        SlashCommand(name="exit", description="Exit the current session.", handler=_exit_handler, aliases=("quit",)),
    ]


def create_default_command_registry(
    *,
    plugin_commands: Iterable[PluginCommandDefinition] = (),
) -> CommandRegistry:
    """Create the default slash command registry."""
    registry = CommandRegistry()
    for command in _builtin_commands():
        registry.register(command)
    for command in plugin_commands:
        if not command.user_invocable:
            continue
        registry.register(
            SlashCommand(
                name=command.name,
                description=command.description,
                handler=_plugin_handler(command),
                remote_invocable=True,
                remote_admin_opt_in=False,
            )
        )
    return registry


def lookup_skill_slash_command(
    raw_input: str,
    context: CommandContext,
) -> tuple[SlashCommand, str] | None:
    """Resolve `/<skill-name>` shortcuts for user-invocable skills."""
    text = raw_input.strip()
    if not text.startswith("/"):
        return None
    body = text[1:].strip()
    if not body:
        return None
    name, _, args = body.partition(" ")
    registry = load_skill_registry(
        context.cwd,
        extra_skill_dirs=context.extra_skill_dirs,
        extra_plugin_roots=context.extra_plugin_roots,
    )
    skill = registry.get(name)
    if skill is None or not skill.user_invocable:
        return None

    async def _handle(skill_args: str, inner_context: CommandContext) -> CommandResult:
        del inner_context
        return CommandResult(
            submit_prompt=_build_prompt(skill.content, skill_args),
            submit_model=skill.model,
        )

    command_name = skill.command_name or skill.name
    return (
        SlashCommand(
            name=command_name,
            description=skill.description,
            handler=_handle,
            remote_invocable=True,
            remote_admin_opt_in=False,
        ),
        args.strip(),
    )
