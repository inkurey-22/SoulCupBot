import discord
from discord.ext import commands
from config import TOKEN

# Set up bot with command prefix
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    if bot.user is not None:
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    else:
        print('Logged in, but bot.user is None.')
    print('------')
    
    # Load command modules
    try:
        await bot.load_extension('commands.channel')
        await bot.load_extension('commands.weapon')
        await bot.load_extension('commands.general')
        print('Successfully loaded all command modules')
    except Exception as e:
        print(f'Error loading command modules: {e}')
    
    # Sync commands
    try:
        await bot.tree.sync()
        print('Successfully synced commands')
    except Exception as e:
        print(f'Error syncing commands: {e}')

if __name__ == '__main__':
    bot.run(TOKEN)
