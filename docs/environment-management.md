# Environment Variable Management

SuperClaude Framework provides robust, cross-platform environment variable management through the `superclaude.env` module.

## Features

- **Automatic .env file loading**: Environment variables are automatically loaded when the package is imported
- **Cross-platform support**: Works seamlessly on Windows, Linux, and macOS
- **Smart file discovery**: Searches upward from current directory to find .env files
- **Utility functions**: Helper functions for working with environment variables
- **Debug mode**: Optional verbose logging for troubleshooting

## Quick Start

### 1. Create a `.env` file

Create a `.env` file in your project root:

```bash
# API Keys
MORPH_API_KEY=your_morph_key_here
TAVILY_API_KEY=your_tavily_key_here
TWENTYFIRST_API_KEY=your_21st_key_here

# Optional settings
SUPERCLAUDE_DEBUG=false
```

### 2. Import SuperClaude

Environment variables are loaded automatically when you import the package:

```python
import superclaude

# Environment variables are now available
import os
api_key = os.getenv("MORPH_API_KEY")
```

## Windows Support

SuperClaude has full Windows compatibility with special handling for Windows-specific features:

### Supported Path Types

- **Drive letters**: `C:\`, `D:\`, etc.
- **UNC paths**: `\\server\share`
- **Long paths**: Paths >260 characters (Windows 10+ with long path support enabled)
- **Symbolic links and junctions**: Properly resolved

### Windows-Specific Behavior

1. **Drive-local search**: Searches within the current drive only (doesn't cross from `D:\` to `C:\`)
2. **Case-insensitive environment**: Windows environment variables are case-insensitive at OS level, but Python's `os.getenv()` is case-sensitive - always use exact case
3. **Path separators**: Automatically handles Windows backslashes and Unix forward slashes

### Example: Windows Paths

```python
# Works on Windows
from superclaude.env import find_env_file

# Finds .env in any of these locations:
# D:\projects\myapp\.env
# D:\projects\.env
# D:\.env
# Or in the SuperClaude installation directory

env_file = find_env_file()
print(f"Found .env at: {env_file}")
```

## API Reference

### Environment Loading Functions

#### `load_env() -> bool`

Load environment variables from .env file.

```python
from superclaude.env import load_env

# Manually reload .env file
if load_env():
    print("Environment loaded successfully")
else:
    print("No .env file found (this is OK)")
```

**Returns**: `True` if .env file was loaded, `False` otherwise

**Features**:
- Automatically finds .env file
- Override mode: .env values take precedence over existing env vars
- Gracefully handles missing .env files
- Silent failure if python-dotenv not installed

#### `find_env_file() -> Optional[Path]`

Find .env file by searching from current directory upwards.

```python
from superclaude.env import find_env_file

env_path = find_env_file()
if env_path:
    print(f"Found .env: {env_path}")
else:
    print("No .env file found")
```

**Returns**: Path to .env file if found, None otherwise

**Search Strategy**:
1. Start from current working directory
2. Search upwards through parent directories
3. Stop at filesystem root
4. Check SuperClaude installation directory

### Utility Functions

#### `get_env(key: str, default: Optional[str] = None) -> Optional[str]`

Get environment variable with optional default value.

```python
from superclaude.env import get_env

# With default
api_key = get_env("MORPH_API_KEY", "default_key")

# Without default
api_key = get_env("MORPH_API_KEY")  # Returns None if not set
```

**Note**: On Windows, always use the exact case for variable names.

#### `require_env(key: str) -> str`

Get required environment variable, raises error if not set.

```python
from superclaude.env import require_env

try:
    api_key = require_env("MORPH_API_KEY")
    print(f"API Key: {api_key}")
except ValueError as e:
    print(f"Missing required variable: {e}")
```

**Raises**: `ValueError` if environment variable is not set

#### `is_env_set(key: str) -> bool`

Check if environment variable is set (even if empty string).

```python
from superclaude.env import is_env_set

if is_env_set("MORPH_API_KEY"):
    print("API key is configured")
else:
    print("API key not configured")
```

#### `list_env_vars(prefix: Optional[str] = None) -> dict[str, str]`

List all environment variables, optionally filtered by prefix.

```python
from superclaude.env import list_env_vars

# Get all Morph-related variables
morph_vars = list_env_vars("MORPH_")
for key, value in morph_vars.items():
    print(f"{key}: {value[:10]}...")

# Get all environment variables
all_vars = list_env_vars()
print(f"Total environment variables: {len(all_vars)}")
```

#### `get_platform_info() -> dict[str, str]`

Get platform-specific information for debugging.

```python
from superclaude.env import get_platform_info

info = get_platform_info()
print(f"Running on {info['system']} {info['release']}")
print(f"Python version: {info['python']}")
print(f"Current directory: {info['cwd']}")
```

**Returns**: Dictionary with platform information
- `system`: Operating system (Windows, Linux, Darwin)
- `release`: OS version (10, 11, etc.)
- `version`: Detailed version info
- `machine`: Architecture (AMD64, x86_64, etc.)
- `python`: Python version
- `cwd`: Current working directory
- `home`: User home directory

## Debug Mode

Enable debug mode to see detailed logging of .env file loading:

```bash
# In your .env file or system environment
SUPERCLAUDE_DEBUG=true
```

When enabled, you'll see messages like:
```
[SuperClaude] Loaded .env from: D:\projects\myapp\.env
```

## Testing

SuperClaude includes comprehensive tests for environment loading:

```bash
# Basic test
uv run python test_env.py

# Windows-specific tests
uv run python tests/test_env_windows.py

# Feature tests
uv run python tests/test_env_features.py
```

## Troubleshooting

### .env file not loading

1. **Check file location**: Ensure `.env` is in project root or a parent directory
2. **Check file name**: Must be exactly `.env` (not `env.txt` or `.env.local`)
3. **Enable debug mode**: Set `SUPERCLAUDE_DEBUG=true` to see loading details
4. **Check python-dotenv**: Ensure package is installed: `uv pip install python-dotenv`

### Windows path issues

1. **Use absolute paths**: When in doubt, use absolute paths like `D:\projects\myapp\.env`
2. **Check permissions**: Ensure you have read access to the .env file
3. **Long paths**: On Windows 10+, enable long path support in registry if using paths >260 chars

### Environment variables not visible

1. **Check case**: Use exact case for variable names (e.g., `MORPH_API_KEY` not `morph_api_key`)
2. **Reload module**: If you modify .env, you may need to reload: `importlib.reload(superclaude.env)`
3. **Check override**: .env values override system env vars by default

## Examples

### Example 1: Simple Usage

```python
import superclaude

# Environment variables automatically loaded
import os
api_key = os.getenv("MORPH_API_KEY")
print(f"Using API key: {api_key[:10]}...")
```

### Example 2: Using Utility Functions

```python
from superclaude.env import get_env, require_env, is_env_set

# Get with default
debug_mode = get_env("DEBUG", "false") == "true"

# Require critical variables
api_key = require_env("MORPH_API_KEY")

# Check if optional variable is set
if is_env_set("CUSTOM_SETTING"):
    custom = get_env("CUSTOM_SETTING")
    print(f"Using custom setting: {custom}")
```

### Example 3: Platform Detection

```python
from superclaude.env import get_platform_info

info = get_platform_info()

if info["system"] == "Windows":
    print("Running on Windows")
    if int(info["release"]) >= 10:
        print("Windows 10+ detected - long path support available")
elif info["system"] == "Linux":
    print("Running on Linux")
elif info["system"] == "Darwin":
    print("Running on macOS")
```

### Example 4: Listing Variables by Prefix

```python
from superclaude.env import list_env_vars

# Get all SuperClaude-related variables
sc_vars = list_env_vars("SUPERCLAUDE_")
print(f"Found {len(sc_vars)} SuperClaude configuration variables")

for key, value in sc_vars.items():
    print(f"  {key} = {value}")

# Get all API keys
api_vars = {k: v for k, v in list_env_vars().items() if "API_KEY" in k}
print(f"\nFound {len(api_vars)} API keys configured")
```

## Security Best Practices

1. **Never commit .env files**: Add `.env` to `.gitignore`
2. **Use .env.example**: Provide a template with dummy values
3. **Rotate keys**: Change API keys periodically
4. **Limit permissions**: On Unix systems, use `chmod 600 .env`
5. **Mask in logs**: Never log full API keys (use masking as shown in examples)

## See Also

- [python-dotenv documentation](https://github.com/theskumar/python-dotenv)
- [CLAUDE.md](../CLAUDE.md) - Project-specific instructions
- [Installation Guide](../README.md) - Framework installation
