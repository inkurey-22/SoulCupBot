"""Channel management commands for the Soul Cup Bot."""

import discord
from discord.ext import commands
from config import CATEGORY, ADMIN_ROLE


async def check_admin_role(interaction: discord.Interaction) -> bool:
    """Check if the user has the required admin role."""
    member = interaction.user
    if not isinstance(member, discord.Member):
        if interaction.guild:
            member = await interaction.guild.fetch_member(interaction.user.id)
        else:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return False
    
    if not any(r.name == ADMIN_ROLE for r in member.roles):
        await interaction.response.send_message(f"You need the '{ADMIN_ROLE}' role to use this command.", ephemeral=True)
        return False
    
    return True


class ChannelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="createchannel", description="Create a new text channel with restricted roles")
    @discord.app_commands.describe(
        prefix="First letters of the channel",
        role1="First role to restrict access",
        role2="Second role to restrict access"
    )
    async def createchannel(
        self,
        interaction: discord.Interaction,
        prefix: str,
        role1: discord.Role,
        role2: discord.Role
    ):
        # Check if user has the required role
        if not await check_admin_role(interaction):
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

    @discord.app_commands.command(name="removeround", description="Remove the channel from the current round")
    @discord.app_commands.describe(
        prefix="First letters of the channel",
    )
    async def removeround(self, interaction: discord.Interaction, prefix: str):
        # Check if user has the required role
        if not await check_admin_role(interaction):
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


async def setup(bot):
    await bot.add_cog(ChannelCommands(bot))
