"""Decorators for exposing agent configuration to low-code tools."""
from typing import Any, Callable, Optional
from enum import Enum

from .registry import ConfigRegistry, PromptRegistry, MCPServerRegistry, GroupKind


def agent_config(
    key: str,
    label: str,
    description: str = "",
    group: GroupKind = GroupKind.BASICS,
    order: int = 0
) -> Callable:
    """Decorator to expose a configuration value.
    
    Args:
        key: Unique configuration key (e.g., 'agent.model')
        label: Human-readable label
        description: Description of the configuration
        group: Configuration group (BASICS, ADVANCED, etc.)
        order: Display order within the group
    """
    def decorator(func: Callable) -> Callable:
        ConfigRegistry.register(
            key=key,
            label=label,
            description=description,
            func=func,
            group=group,
            order=order
        )
        return func
    return decorator


def prompt_section(
    key: str,
    label: str,
    description: str = "",
    group: GroupKind = GroupKind.BASICS,
    order: int = 0
) -> Callable:
    """Decorator to expose a prompt section.
    
    Args:
        key: Unique prompt key (e.g., 'prompts.system')
        label: Human-readable label
        description: Description of the prompt section
        group: Prompt group (BASICS, ADVANCED, etc.)
        order: Display order within the group
    """
    def decorator(func: Callable) -> Callable:
        PromptRegistry.register(
            key=key,
            label=label,
            description=description,
            func=func,
            group=group,
            order=order
        )
        return func
    return decorator


def mcp_server(
    key: str,
    label: str,
    description: str = "",
    command: str = "",
    args: list[str] = None,
    env: dict[str, str] = None
) -> Callable:
    """Decorator to register an MCP server configuration.
    
    Args:
        key: Unique server key (e.g., 'mcp.filesystem')
        label: Human-readable label
        description: Description of the MCP server
        command: Command to start the server
        args: Command arguments
        env: Environment variables
    """
    def decorator(func: Callable) -> Callable:
        MCPServerRegistry.register(
            key=key,
            label=label,
            description=description,
            command=command,
            args=args or [],
            env=env or {},
            func=func
        )
        return func
    return decorator
