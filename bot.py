import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

CATEGORY = "Tournament"
ADMIN_ROLE = "TO"

def snake_case(s):
    return s.lower().replace(" ", "_").replace(".", "")

BOXES = [
    ["Liter", "Charger"],
    ["Squiffer", "Bamboozler", "Goo Tuber", "Pencil"],
    ["Heavy", "Hydra", "Ballpoint", "Bow"],
    ["Pro Shot", ".96 Gal", "Jet Squelcher", "Nova", "H3",
        "Squeezer", "Mini", "Nautilus", "Gloogas", "Squelchies", "ReefLux"],
    ["Sploosh", "Junior", "Splash", "Aerospray", "VShot", ".52 Gal",
        "NZap", "L3", "Dapples", "Dualies", "Tetras"],
    ["Range Blaster", "Rapid", "Rapid Pro", "Bloblobber", "Explosher"],
    ["Luna", "Blaster", "Clash Blaster", "Bucket", "TriSlosher", "Machine"],
    ["Dynamo", "Flingza", "Big Swig", "Tenta Brella", "Stamper"],
    ["Carbon", "Splat Roller", "Inkbrush", "Octobrush", "Brella", "Undercover", "Wiper"]
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
    # Check if user has the required role
    if not any(r.name == ADMIN_ROLE for r in interaction.user.roles):
        await interaction.response.send_message(f"You need the '{ADMIN_ROLE}' role to use this command.", ephemeral=True)
        return

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

    # Always use the same category
    category_name = CATEGORY
    category = discord.utils.get(guild.categories, name=category_name)
    if category is None:
        await interaction.response.send_message(f"Category '{category_name}' not found.", ephemeral=True)
        return

    channel = await guild.create_text_channel(channel_name, overwrites=overwrites, category=category)
    await interaction.response.send_message(
        f"Channel '{channel.mention}' created in {category.mention} and restricted to {role1.mention} and {role2.mention}!",
        ephemeral=True
    )

@bot.tree.command(name="removeround", description="Remove the channel from the current round")
@discord.app_commands.describe(
    prefix="First letters of the channel",
)
async def removeround(interaction: discord.Interaction, prefix: str):
    # Check if user has the required role
    if not any(r.name == ADMIN_ROLE for r in interaction.user.roles):
        await interaction.response.send_message(f"You need the '{ADMIN_ROLE}' role to use this command.", ephemeral=True)
        return

    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
        return

    category_name = CATEGORY
    category = discord.utils.get(guild.categories, name=category_name)
    if category is None:
        await interaction.response.send_message(f"Category '{category_name}' not found.", ephemeral=True)
        return

    channels_to_delete = [ch for ch in category.channels if ch.name.startswith(prefix.lower())]
    if not channels_to_delete:
        await interaction.response.send_message(f"No channels found in '{category_name}' starting with '{prefix}'.", ephemeral=True)
        return

    for channel in channels_to_delete:
        await channel.delete(reason=f"Removed by removeround command with prefix '{prefix}'")

    await interaction.response.send_message(
        f"Removed {len(channels_to_delete)} channel(s) in '{category_name}' starting with '{prefix}'.",
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

    # Add emotes using snake_case for each weapon name
    picks_with_emotes = []
    for pick in picks:
        if "**" in pick:
            # Extract weapon name between **
            weapon_name = pick.split("**")[1]
            emote_name = snake_case(weapon_name)
            # Try to find a custom emoji in the guild
            emote = None
            if interaction.guild:
                for emoji in interaction.guild.emojis:
                    if emoji.name == emote_name:
                        emote = str(emoji)
                        break
            if not emote:
                emote = f":{emote_name}:"  # fallback to :name:
            pick = pick.replace(f"**{weapon_name}**", f"{emote} **{weapon_name}**")
        picks_with_emotes.append(pick)

    await interaction.response.send_message("Your picks:\n" + "\n".join(picks_with_emotes))

@bot.tree.command(name="listweapons", description="List all available weapons in boxes")
async def listweapons(interaction: discord.Interaction):
    lines = []
    for i, weapons in enumerate(BOXES):
        weapon_emotes = []
        for weapon in weapons:
            emote_name = snake_case(weapon)
            emote = None
            if interaction.guild:
                for emoji in interaction.guild.emojis:
                    if emoji.name == emote_name:
                        emote = str(emoji)
                        break
            if not emote:
                emote = f":{emote_name}:"
            weapon_emotes.append(f"{emote} {weapon}")
        lines.append(f"Box {i + 1}: " + ", ".join(weapon_emotes))
    embed = discord.Embed(
        title="Available Weapons",
        description="\n".join(lines),
        color=discord.Color.blurple()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Display help information")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Help - Available Commands",
        description="List of all available commands:",
        color=discord.Color.blurple()
    )
    embed.add_field(name="/pickweapon", value="Pick weapons from boxes by specifying box numbers.", inline=False)
    embed.add_field(name="/listweapons", value="List all available weapons in boxes.", inline=False)
    embed.add_field(name="/help", value="Display this help information.", inline=False)
    await interaction.response.send_message(embed=embed)

if __name__ == '__main__':
    bot.run(TOKEN)
