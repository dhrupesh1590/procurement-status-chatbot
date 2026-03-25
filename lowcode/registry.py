"""Registry for configuration, prompts, and MCP servers."""
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class GroupKind(str, Enum):
    """Configuration group kinds."""
    BASICS = "basics"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class ConfigEntry:
    """Configuration entry."""
    key: str
    label: str
    description: str
    func: Callable
    group: GroupKind
    order: int


@dataclass
class PromptEntry:
    """Prompt entry."""
    key: str
    label: str
    description: str
    func: Callable
    group: GroupKind
    order: int


@dataclass
class MCPServerEntry:
    """MCP Server entry."""
    key: str
    label: str
    description: str
    command: str
    args: List[str]
    env: Dict[str, str]
    func: Callable


class ConfigRegistry:
    """Registry for configuration values."""
    _entries: Dict[str, ConfigEntry] = {}
    
    @classmethod
    def register(
        cls,
        key: str,
        label: str,
        description: str,
        func: Callable,
        group: GroupKind,
        order: int
    ) -> None:
        """Register a configuration entry."""
        cls._entries[key] = ConfigEntry(
            key=key,
            label=label,
            description=description,
            func=func,
            group=group,
            order=order
        )
    
    @classmethod
    def get_all(cls) -> Dict[str, ConfigEntry]:
        """Get all registered configurations."""
        return cls._entries
    
    @classmethod
    def get(cls, key: str) -> Optional[ConfigEntry]:
        """Get a specific configuration entry."""
        return cls._entries.get(key)


class PromptRegistry:
    """Registry for prompt sections."""
    _entries: Dict[str, PromptEntry] = {}
    
    @classmethod
    def register(
        cls,
        key: str,
        label: str,
        description: str,
        func: Callable,
        group: GroupKind,
        order: int
    ) -> None:
        """Register a prompt entry."""
        cls._entries[key] = PromptEntry(
            key=key,
            label=label,
            description=description,
            func=func,
            group=group,
            order=order
        )
    
    @classmethod
    def get_all(cls) -> Dict[str, PromptEntry]:
        """Get all registered prompts."""
        return cls._entries
    
    @classmethod
    def get(cls, key: str) -> Optional[PromptEntry]:
        """Get a specific prompt entry."""
        return cls._entries.get(key)


class MCPServerRegistry:
    """Registry for MCP servers."""
    _entries: Dict[str, MCPServerEntry] = {}
    
    @classmethod
    def register(
        cls,
        key: str,
        label: str,
        description: str,
        command: str,
        args: List[str],
        env: Dict[str, str],
        func: Callable
    ) -> None:
        """Register an MCP server entry."""
        cls._entries[key] = MCPServerEntry(
            key=key,
            label=label,
            description=description,
            command=command,
            args=args,
            env=env,
            func=func
        )
    
    @classmethod
    def get_all(cls) -> Dict[str, MCPServerEntry]:
        """Get all registered MCP servers."""
        return cls._entries
    
    @classmethod
    def get(cls, key: str) -> Optional[MCPServerEntry]:
        """Get a specific MCP server entry."""
        return cls._entries.get(key)
