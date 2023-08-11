import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Estudando na Fatec Registro"))
    print('teuz bot está pronto!')
    print("-="*10)
    print("escrito por @dieguesmosken")

@bot.command()
async def add_role(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'{member.name} recebeu o cargo {role.name}.')

@bot.command()
async def add_color(ctx, role: discord.Role, color: discord.Color):
    await role.edit(color=color)
    await ctx.send(f'O cargo {role.name} recebeu a cor {color}.')

@bot.command()
async def greet(ctx):
    await ctx.send('Olá! Em que posso ajudar?')

@bot.command()
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)

bot.run('MTEzOTYwOTAzMjA5NzgwNDM4OQ.G-Wnpo.qqAsiTYV1ppk5VOys0qUUWXbN1Vyj3dZXTFG_4')