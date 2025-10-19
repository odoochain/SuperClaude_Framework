"""
Environment variable management for SuperClaude
Loads .env files and makes environment variables available
"""

import os
from pathlib import Path
from typing import Optional


def find_env_file() -> Optional[Path]:
    """
    Find .env file by searching from current directory upwards

    Returns:
        Path to .env file if found, None otherwise
    """
    # Start from current working directory
    current = Path.cwd()

    # Search upwards until we find .env or reach root
    while True:
        env_file = current / ".env"
        if env_file.exists():
            return env_file

        # Check parent directory
        parent = current.parent
        if parent == current:  # Reached root
            break
        current = parent

    # Also check project root (where this file is located)
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        return env_file

    return None


def load_env() -> bool:
    """
    Load environment variables from .env file

    Returns:
        True if .env file was loaded, False otherwise
    """
    try:
        from dotenv import load_dotenv

        # Find .env file
        env_file = find_env_file()

        if env_file:
            # Load the .env file
            load_dotenv(dotenv_path=env_file, override=True)
            return True
        else:
            # No .env file found - this is OK, not an error
            return False

    except ImportError:
        # python-dotenv not installed - this is OK during development
        return False
    except Exception as e:
        # Log error but don't fail
        import warnings
        warnings.warn(f"Failed to load .env file: {e}")
        return False


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get environment variable with optional default

    Args:
        key: Environment variable name
        default: Default value if variable is not set

    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)


def require_env(key: str) -> str:
    """
    Get required environment variable, raise error if not set

    Args:
        key: Environment variable name

    Returns:
        Environment variable value

    Raises:
        ValueError: If environment variable is not set
    """
    value = os.getenv(key)
    if value is None:
        raise ValueError(
            f"Required environment variable '{key}' is not set. "
            f"Please set it in your .env file or system environment."
        )
    return value


# Auto-load .env on module import
load_env()
