import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

BOXES = [
    ["E-Liter", "Charger", "Pencil"],
    ["Shot", "Splash-O", "52. Gal"],
    ["Bucket", "Squeezer", "Stamper"]
]

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot with command prefix
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} slash commands.')
    except Exception as e:
        print(f'Error syncing commands: {e}')

@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello from a slash command!")

@bot.tree.command(name="createchannel", description="Create a new text channel with restricted roles")
@discord.app_commands.describe(
    prefix="First letters of the channel",
    role1="First role to restrict access",
    role2="Second role to restrict access"
)
async def createchannel(
    interaction: discord.Interaction,
    prefix: str,
    role1: discord.Role,
    role2: discord.Role
):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
        return

    if role1 == role2:
        await interaction.response.send_message("Roles must be different.", ephemeral=True)
        return

    channel_name = f"{prefix}-{role1.name}-{role2.name}".replace(" ", "-").lower()
    existing = discord.utils.get(guild.channels, name=channel_name)
    if existing:
        await interaction.response.send_message(f"Channel '{channel_name}' already exists.", ephemeral=True)
        return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        role1: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        role2: discord.PermissionOverwrite(view_channel=True, send_messages=True),
    }

    # Always use the same category (change the name as needed)
    category_name = "Tournament"  # <-- Change this to your category name
    category = discord.utils.get(guild.categories, name=category_name)
    if category is None:
        await interaction.response.send_message(f"Category '{category_name}' not found.", ephemeral=True)
        return

    channel = await guild.create_text_channel(channel_name, overwrites=overwrites, category=category)
    await interaction.response.send_message(
        f"Channel '{channel.mention}' created in {category.mention} and restricted to {role1.mention} and {role2.mention}!",
        ephemeral=True
    )

@bot.tree.command(name="pickweapon", description="Pick weapons from boxes by specifying box numbers (e.g., /pickweapon 1 3 2 3)")
@discord.app_commands.describe(
    boxes="Box numbers to pick from, separated by spaces (e.g., 1 3 2 3, up to 4 numbers)"
)
async def pickweapon(interaction: discord.Interaction, *, boxes: str):
    # Parse input: split by spaces, convert to int, max 4
    try:
        box_indices = [int(b) for b in boxes.strip().split()]
    except ValueError:
        await interaction.response.send_message("Please provide box numbers as integers separated by spaces.", ephemeral=True)
        return

    if not (1 <= len(box_indices) <= 4):
        await interaction.response.send_message("You must specify between 1 and 4 box numbers.", ephemeral=True)
        return

    # Validate each box number
    for idx in box_indices:
        if not (1 <= idx <= len(BOXES)):
            await interaction.response.send_message(f"Box numbers must be between 1 and {len(BOXES)}.", ephemeral=True)
            return

    # Pick a random weapon from each specified box
    picks = []
    for idx in box_indices:
        weapons = BOXES[idx - 1]
        if not weapons:
            picks.append(f"Box {idx}: *(empty)*")
        else:
            weapon = random.choice(weapons)
            picks.append(f"Box {idx}: **{weapon}**")

    await interaction.response.send_message("Your picks:\n" + "\n".join(picks))

if __name__ == '__main__':
    bot.run(TOKEN)
