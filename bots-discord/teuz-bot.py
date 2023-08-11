import discord
from discord.ext import commands
from config import TOKEN_TEUZ

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
message = "DSM Fatec Registro"
@bot.event
async def on_ready():
    #await bot.change_presence(activity=discord.Game(name=message)) #padrão
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name='Programando')) #stremando
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Música test')) #ouvindo
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Filmes')) #assistindo
    await bot.change_presence(activity=discord.Streaming(name='Live Codificação', url='https://www.twitch.tv/teuzinytbr')) #transmitindo
    #await bot.change_presence()

    print('teuz bot está pronto!')
    print("-="*10)
    print("escrito por @dieguesmosken")
    print(f"jogo alterado para {message} !")

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

bot.run(TOKEN_TEUZ)
