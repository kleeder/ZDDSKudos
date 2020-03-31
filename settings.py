import discord
from discord.ext import commands

# settings and global variables
filename = None
Client = discord.Client()
client = commands.Bot(command_prefix = "!")
client.remove_command('help')
