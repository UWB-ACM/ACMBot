import discord
from discord.ext import commands
import asyncio
# configuration files
import configparser
import sys, traceback

# load configuration to get around hard coded tokens
config = configparser.ConfigParser()
with open('config.ini') as config_file:
    config.read_file(config_file)

# startup stuff
print(f'discordpy version: {discord.__version__}')

client = commands.Bot(command_prefix=';;', description='Utility bot for the UWB ACM Discord server. View source at '
                                                       'github.com/UWB-ACM/ACMBot')

# this is where extensions are added by default
default_extensions = ['cogs.base']


if __name__ == '__main__':
    for extension in default_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@client.event
async def on_ready():
    # print some stuff when the bot goes online
    print(f'Logged in {client.user.name} - {client.user.id}\nVersion {discord.__version__}')
    await client.change_presence(activity=discord.Game(name='Try ;;help'))

# now actually connect the bot
client.run(config.get(section='Configuration', option='connection_token'),
           bot=True, reconnect=True)
