"""Runtime utilities for accessing configuration at runtime."""
from typing import Any, Optional

from .registry import ConfigRegistry, PromptRegistry


def get_config(key: str, default: Any = None) -> Any:
    """Get a configuration value at runtime.
    
    Args:
        key: Configuration key
        default: Default value if not found
        
    Returns:
        Configuration value or default
    """
    entry = ConfigRegistry.get(key)
    if entry:
        return entry.func()
    return default


def get_prompt(key: str, default: str = "") -> str:
    """Get a prompt section at runtime.
    
    Args:
        key: Prompt key
        default: Default value if not found
        
    Returns:
        Prompt text or default
    """
    entry = PromptRegistry.get(key)
    if entry:
        return entry.func()
    return default
