r"""
Environment variable management for SuperClaude
Loads .env files and makes environment variables available

Cross-platform support:
- Unix/Linux/macOS: Standard POSIX paths
- Windows: Supports drive letters (C:\, D:\), UNC paths (\\server\share)
- Handles symbolic links and junctions correctly
"""

import os
import sys
from pathlib import Path
from typing import Optional


def find_env_file() -> Optional[Path]:
    r"""
    Find .env file by searching from current directory upwards

    Search strategy:
    1. Start from current working directory
    2. Search upwards through parent directories until root
    3. Check project root (where this module is installed)

    Windows-specific behavior:
    - Searches within current drive only (doesn't cross from D:\ to C:\)
    - Correctly handles drive roots (C:\, D:\, etc.)
    - Supports UNC paths (\\server\share)
    - Handles long paths (>260 chars) on Windows 10+

    Returns:
        Path to .env file if found, None otherwise
    """
    # Start from current working directory
    current = Path.cwd().resolve()  # resolve() handles symlinks

    # Search upwards until we find .env or reach root
    max_depth = 50  # Safety limit to prevent infinite loops
    depth = 0

    while depth < max_depth:
        env_file = current / ".env"
        if env_file.exists() and env_file.is_file():
            return env_file

        # Check parent directory
        parent = current.parent

        # Reached root (works for Windows C:\, Unix /, and UNC \\server\share)
        if parent == current:
            break

        current = parent
        depth += 1

    # Also check project root (where this file is located)
    try:
        project_root = Path(__file__).parent.parent.resolve()
        env_file = project_root / ".env"
        if env_file.exists() and env_file.is_file():
            return env_file
    except Exception:
        # If we can't determine project root, that's OK
        pass

    return None


def load_env() -> bool:
    """
    Load environment variables from .env file

    Features:
    - Automatically finds .env file in current or parent directories
    - Override=True: .env values take precedence over existing env vars
    - Gracefully handles missing .env files (not an error)
    - Silent failure if python-dotenv not installed

    Returns:
        True if .env file was loaded, False otherwise
    """
    try:
        from dotenv import load_dotenv

        # Find .env file
        env_file = find_env_file()

        if env_file:
            # Load the .env file
            # override=True means .env values override existing environment variables
            success = load_dotenv(dotenv_path=env_file, override=True)

            # Only log if verbose mode or debug
            if os.getenv("SUPERCLAUDE_DEBUG"):
                print(f"[SuperClaude] Loaded .env from: {env_file}", file=sys.stderr)

            return bool(success)
        else:
            # No .env file found - this is OK, not an error
            if os.getenv("SUPERCLAUDE_DEBUG"):
                print("[SuperClaude] No .env file found", file=sys.stderr)
            return False

    except ImportError:
        # python-dotenv not installed - this is OK during development
        if os.getenv("SUPERCLAUDE_DEBUG"):
            print("[SuperClaude] python-dotenv not installed, skipping .env", file=sys.stderr)
        return False
    except Exception as e:
        # Log error but don't fail - environment loading shouldn't break the app
        import warnings
        warnings.warn(
            f"Failed to load .env file: {e}\n"
            f"This is not critical, but API keys may not be available.",
            RuntimeWarning,
            stacklevel=2
        )
        return False


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get environment variable with optional default

    Note: On Windows, environment variables are case-insensitive at the OS level,
    but Python's os.getenv() is case-sensitive. Always use the exact case.

    Args:
        key: Environment variable name (case-sensitive)
        default: Default value if variable is not set

    Returns:
        Environment variable value or default

    Example:
        >>> api_key = get_env("MORPH_API_KEY", "default_key")
    """
    return os.getenv(key, default)


def require_env(key: str) -> str:
    """
    Get required environment variable, raise error if not set

    Args:
        key: Environment variable name (case-sensitive)

    Returns:
        Environment variable value

    Raises:
        ValueError: If environment variable is not set

    Example:
        >>> api_key = require_env("MORPH_API_KEY")  # Raises if not set
    """
    value = os.getenv(key)
    if value is None:
        raise ValueError(
            f"Required environment variable '{key}' is not set.\n"
            f"Please set it in your .env file or system environment.\n\n"
            f"Example .env file:\n"
            f"  {key}=your_value_here\n"
        )
    return value


def list_env_vars(prefix: Optional[str] = None) -> dict[str, str]:
    """
    List all environment variables, optionally filtered by prefix

    Args:
        prefix: Optional prefix to filter variables (e.g., "MORPH_")

    Returns:
        Dictionary of environment variables

    Example:
        >>> morph_vars = list_env_vars("MORPH_")
        >>> print(morph_vars)
        {'MORPH_API_KEY': 'xxx...', 'MORPH_DEBUG': 'true'}
    """
    if prefix:
        return {k: v for k, v in os.environ.items() if k.startswith(prefix)}
    return dict(os.environ)


def is_env_set(key: str) -> bool:
    """
    Check if environment variable is set (even if empty string)

    Args:
        key: Environment variable name

    Returns:
        True if variable exists, False otherwise

    Example:
        >>> if is_env_set("MORPH_API_KEY"):
        ...     print("API key is configured")
    """
    return key in os.environ


def get_platform_info() -> dict[str, str]:
    """
    Get platform-specific information for debugging

    Returns:
        Dictionary with platform information

    Example:
        >>> info = get_platform_info()
        >>> print(f"Running on {info['system']} {info['release']}")
    """
    import platform

    return {
        "system": platform.system(),  # Windows, Linux, Darwin
        "release": platform.release(),  # 10, 11, etc.
        "version": platform.version(),
        "machine": platform.machine(),  # AMD64, x86_64, etc.
        "python": platform.python_version(),
        "cwd": str(Path.cwd()),
        "home": str(Path.home()),
    }


# Auto-load .env on module import
load_env()

