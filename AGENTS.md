# AGENT.md - Python Discord Bot Template

## Project Overview

This is a Discord bot template built with Python and discord.py 2.6.4. It provides a solid foundation for creating personalized Discord bots with a modular cog architecture.

- **Version**: 6.5.0
- **Python**: 3.12.12
- **discord.py**: 2.6.4
- **License**: Apache License 2.0

## Design Philosophy

### 1. Learning-Oriented Template
- Stated in README: "Not the best template, but a good template to start learning"
- Keeps simplicity while demonstrating practical patterns
- Provides `template.py` as a starting point for new cogs

### 2. Modular Architecture (Cog Separation)
- Each feature domain is isolated in its own cog
- Cogs can be loaded/unloaded/reloaded independently at runtime
- Clear separation: general, moderation, fun, owner

### 3. Hybrid Commands First
- Slash commands and prefix commands both supported via `@commands.hybrid_command()`
- Slash commands are the primary interface (message_content intent disabled by default)
- Prefix commands available as fallback when enabled

### 4. Async-First Design
- All I/O operations are asynchronous (aiosqlite, aiohttp)
- Non-blocking design prevents bot from freezing during API calls
- Follows discord.py best practices for web requests

### 5. Owner Privilege Separation
- Bot owner has exclusive access to sensitive commands (sync, shutdown, cog management)
- Uses `@commands.is_owner()` decorator for protection
- Owner commands hidden from non-owners in help menu

## Architecture

```
active-time/
├── bot.py              # Main entry point, DiscordBot class definition
├── cogs/               # Modular command groups
│   ├── general.py      # General commands (help, ping, botinfo, etc.)
│   ├── moderation.py   # Moderation commands (kick, ban, warn, etc.)
│   ├── fun.py          # Fun commands (coinflip, rps, randomfact)
│   ├── owner.py        # Owner-only commands (sync, load, shutdown)
│   └── template.py     # Template for creating new cogs
├── database/           # Database layer
│   ├── __init__.py     # DatabaseManager class
│   └── schema.sql      # SQLite schema definition
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Docker orchestration
└── Dockerfile          # Docker image definition
```

## Key Components

### DiscordBot Class (bot.py)

Custom bot class extending `commands.Bot` with:
- Custom logger with colored console output
- SQLite database initialization
- Automatic cog loading
- Status task for bot presence
- Error handling for commands

### Database Manager (database/__init__.py)

Handles all database operations:
- `add_warn()`: Add warning to user
- `remove_warn()`: Remove warning from user
- `get_warnings()`: Get all warnings for a user

### Cogs Structure

Each cog follows this pattern:
```python
class CogName(commands.Cog, name="cogname"):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    # Commands defined here

async def setup(bot) -> None:
    await bot.add_cog(CogName(bot))
```

## Commands Summary

### General Commands
| Command | Description |
|---------|-------------|
| `/help` | List all commands |
| `/botinfo` | Bot information |
| `/serverinfo` | Server information |
| `/ping` | Check bot latency |
| `/invite` | Get bot invite link |
| `/server` | Get support server link |
| `/8ball` | Ask the magic 8-ball |
| `/bitcoin` | Get Bitcoin price |
| `/feedback` | Submit feedback via modal |

### Moderation Commands
| Command | Description |
|---------|-------------|
| `/kick` | Kick a user |
| `/ban` | Ban a user |
| `/nick` | Change user nickname |
| `/hackban` | Ban user by ID |
| `/purge` | Delete messages |
| `/archive` | Archive channel messages |
| `/warning add` | Add warning to user |
| `/warning remove` | Remove warning |
| `/warning list` | List user warnings |

### Fun Commands
| Command | Description |
|---------|-------------|
| `/randomfact` | Get random fact |
| `/coinflip` | Coin flip game |
| `/rps` | Rock paper scissors |

### Owner Commands (Bot owner only)
| Command | Description |
|---------|-------------|
| `/sync` | Sync slash commands |
| `/unsync` | Unsync slash commands |
| `/load` | Load a cog |
| `/unload` | Unload a cog |
| `/reload` | Reload a cog |
| `/shutdown` | Shutdown the bot |
| `/say` | Bot repeats message |
| `/embed` | Bot sends embed |

## Configuration

Environment variables (via `.env` file):
- `TOKEN`: Discord bot token (required)
- `PREFIX`: Command prefix for normal commands
- `INVITE_LINK`: Bot invite link

## Running the Bot

### Standard
```bash
python -m pip install -r requirements.txt
python bot.py
```

### Docker
```bash
docker compose up -d --build
```

## Database Design

### Current Schema: Single Table

The project uses a minimal SQLite database with a single `warns` table:

```sql
CREATE TABLE warns (
  id int(11) NOT NULL,
  user_id varchar(20) NOT NULL,
  server_id varchar(20) NOT NULL,
  moderator_id varchar(20) NOT NULL,
  reason varchar(255) NOT NULL,
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Table Structure

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Sequential warn ID per (user_id, server_id) |
| `user_id` | varchar(20) | Discord user ID being warned |
| `server_id` | varchar(20) | Discord guild ID |
| `moderator_id` | varchar(20) | Discord ID of moderator who issued warning |
| `reason` | varchar(255) | Reason for the warning |
| `created_at` | timestamp | Auto-generated timestamp |

### Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Server Isolation** | `server_id` enables multi-guild support with independent warning histories |
| **Sequential IDs** | IDs are sequential per (user, server), not global - easier for moderators to reference |
| **No User Data Storage** | Usernames etc. fetched from Discord API on demand - avoids stale data |
| **KISS Principle** | Single table for warnings only - minimal complexity |
| **Audit Trail** | `moderator_id` tracks who issued each warning |

### Database Manager Methods

```python
async def add_warn(user_id, server_id, moderator_id, reason) -> int
async def remove_warn(warn_id, user_id, server_id) -> int
async def get_warnings(user_id, server_id) -> list
```

### Potential Improvements

- Add index on `(user_id, server_id)` for faster lookups
- Consider soft delete instead of hard delete for audit purposes
- Add foreign key constraints if migrating to PostgreSQL/MySQL

## Dependencies

- `discord.py==2.6.4` - Discord API wrapper
- `aiosqlite` - Async SQLite support
- `aiohttp` - Async HTTP client
- `python-dotenv` - Environment variable loader

## Code Style

- Black code formatter
- Conventional Commits
- Type hints on all functions
- Async/await patterns throughout

## Important Notes

1. **Hybrid Commands**: Most commands work as both slash commands and prefix commands
2. **Intents**: `intents.message_content` is commented out by default; enable if using prefix commands
3. **Permissions**: Moderation commands require appropriate bot permissions
4. **Error Handling**: Comprehensive error handling in `on_command_error`
5. **Logging**: Logs to both console (colored) and file (discord.log)

## Creating New Features

1. Copy `cogs/template.py` as a starting point
2. Implement commands using `@commands.hybrid_command()` decorator
3. Use `self.bot` to access bot instance
4. Add new cog to `cogs/` directory (auto-loaded on startup)
5. For database features, extend `DatabaseManager` class

## API Integrations Used

- Coindesk API (Bitcoin price)
- Useless Facts API (Random facts)
