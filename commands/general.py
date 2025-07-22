"""General utility commands for the Soul Cup Bot."""

import discord
from discord.ext import commands


class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="help", description="Display help information")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Help - Available Commands",
            description="List of all available commands:",
            color=discord.Color.blurple()
        )
        embed.add_field(name="/pickweapon", value="Pick weapons from boxes by specifying box numbers.", inline=False)
        embed.add_field(name="/listweapons", value="List all available weapons in each boxes.", inline=False)
        embed.add_field(name="/createchannel", value="Create a new text channel with restricted roles (Admin only).", inline=False)
        embed.add_field(name="/removeround", value="Remove channels from the current round (Admin only).", inline=False)
        embed.add_field(name="/help", value="Display this help information.", inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))
