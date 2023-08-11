import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command()
async def add_role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'{member.name} has been given the {role.name} role.')

@bot.command()
async def add_color(ctx, role: discord.Role, color: discord.Color):
    await role.edit(color=color)
    await ctx.send(f'The {role.name} role has been given the {color} color.')

bot.run('ea6b895ff09eeaa6d76b80012de35fe1b9fc67b186380afb341abe2f5b28df66')
