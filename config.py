import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
CATEGORY = os.getenv('CATEGORY_NAME')
ADMIN_ROLE = os.getenv('TO_ROLE')

# Validate required environment variables
if TOKEN is None:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set.")
if CATEGORY is None:
    raise RuntimeError("CATEGORY_NAME environment variable is not set.")
if ADMIN_ROLE is None:
    raise RuntimeError("TO_ROLE environment variable is not set.")
