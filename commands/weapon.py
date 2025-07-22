"""Weapon-related commands for the Soul Cup Bot."""

import discord
from discord.ext import commands
import random
from data.weapons import BOXES
from utils import snake_case


class WeaponCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="pickweapon", description="Pick weapons from boxes by specifying box numbers (e.g., /pickweapon 1 3 2 3)")
    @discord.app_commands.describe(
        boxes="Box numbers to pick from, separated by spaces (e.g., 1 3 2 3, up to 4 numbers)"
    )
    async def pickweapon(self, interaction: discord.Interaction, *, boxes: str):
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
                # Try to find a custom emoji in the application
                emote = discord.utils.get(interaction.client.emojis, name=emote_name)
                if not emote:
                    emote = ""  # fallback to nothing
                pick = pick.replace(f"**{weapon_name}**", f"{emote} **{weapon_name}**")
            picks_with_emotes.append(pick)

        await interaction.response.send_message("Your picks:\n" + "\n".join(picks_with_emotes))

    @discord.app_commands.command(name="listweapons", description="List all available weapons in boxes")
    async def listweapons(self, interaction: discord.Interaction):
        lines = []
        for i, weapons in enumerate(BOXES):
            weapon_emotes = []
            for weapon in weapons:
                emote_name = snake_case(weapon)
                emote = discord.utils.get(interaction.client.emojis, name=emote_name)
                if not emote:
                    emote = ""  # fallback to nothing
                weapon_emotes.append(f"{emote} {weapon}")
            lines.append(f"Box {i + 1}: " + ", ".join(weapon_emotes))
        embed = discord.Embed(
            title="Available Weapons",
            description="\n".join(lines),
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(WeaponCommands(bot))
