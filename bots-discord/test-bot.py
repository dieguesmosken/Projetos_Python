import os
import discord
import datetime
from discord.ext import commands
from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True  # Adicione esta linha

bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = DISCORD_TOKEN
message = "DSM Fatec Registro"


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord! está pronto!')
    print("-="*10)
    #await bot.change_presence(activity=discord.Game(name=message)) #padrão
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name='Dominando o mundo')) #stremando
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Música test')) #ouvindo
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Filmes')) #assistindo
    #await bot.change_presence(activity=discord.Streaming(name=message, url='https://github.com/dieguesmosken')) #transmitindo
    print("-="*10)
    print("escrito por @dieguesmosken")
    print("-="*10)
    print(f"status alterado para {message} !")

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'OI {member.name}, Seja bem vindo ao TEST!')


@bot.command()
async def saudacao(ctx):
    hora_atual = datetime.datetime.now().time()
    mensagem = ""

    if hora_atual < datetime.time(12):
        mensagem = f"Bom dia {ctx.author.name}, como vai você?"
    elif hora_atual < datetime.time(18):
        mensagem = f"Boa tarde {ctx.author.name}, como vai você?"
    else:
        mensagem = f"Boa noite {ctx.author.name}, como vai você?"

    await ctx.send(mensagem)

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


bot.run(TOKEN)