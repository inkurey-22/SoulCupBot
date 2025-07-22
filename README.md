# Soul Cup Bot

A Discord bot for managing Soul Cup tournaments with weapon selection and channel management features.

## Features

- **Weapon Selection**: Pick random weapons from predefined boxes
- **Channel Management**: Create and manage private channels for tournament rounds
- **Role-based Access**: Admin-only commands for tournament organization

## Project Structure

```
SoulCupBot/
├── bot.py                          # Main bot file - entry point
├── config.py                       # Configuration and environment variables
├── utils.py                        # Utility functions
├── requirements.txt                # Python dependencies
├── commands/                       # Command modules
│   ├── __init__.py
│   ├── channel.py                  # Channel creation and management
│   ├── weapon.py                   # Weapon selection commands
│   └── general.py                  # Help and utility commands
└── data/
    ├── __init__.py
    └── weapons.py                  # Weapon data definitions
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your configuration:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   CATEGORY_NAME=your_category_name
   TO_ROLE=your_admin_role_name
   ```

3. Run the bot:
   ```bash
   python bot.py
   ```

## Commands

### Public Commands
- `/pickweapon <boxes>` - Pick random weapons from specified boxes (e.g., "1 3 2 3")
- `/listweapons` - Display all available weapons in each box
- `/help` - Show help information

### Admin Commands (requires configured role)
- `/createchannel <prefix> <role1> <role2>` - Create a private channel for two roles
- `/removeround <prefix>` - Remove all channels starting with the given prefix

## Environment Variables

- `DISCORD_TOKEN`: Your Discord bot token
- `CATEGORY_NAME`: The category where channels will be created
- `TO_ROLE`: The role name required for admin commands