import discord
from discord.ext import commands
from discord_slash import SlashCommand

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print('teuz bot esta pronto!')
    print("-="*10)
    print("escrito por @dieguesmosken")

@slash.slash(name="add_role", description="Adiciona um cargo a um membro")
async def add_role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'{member.name} has been given the {role.name} role.')
    print(f'{member.name} has been given the {role.name} role.')

@slash.slash(name="add_color", description="Altera a cor de um cargo")
async def add_color(ctx, role: discord.Role, color: discord.Color):
    await role.edit(color=color)
    await ctx.send(f'The {role.name} role has been given the {color} color.')
    print(f'The {role.name} role has been given the {color} color.')

@slash.slash(name="greet", description="Cumprimenta o bot")
async def greet(ctx):
    await ctx.send("Olá! Como posso ajudar?")

@slash.slash(name="clear", description="Limpa mensagens no canal")
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)

bot.run('MTEzOTYwOTAzMjA5NzgwNDM4OQ.GTpEqf.67NZa7mmqLGMB1wcv8fY9Qa8G2xhW98WJLF1AE')