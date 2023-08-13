import os
import discord
import datetime
from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

TOKEN = DISCORD_TOKEN
message = "DSM Fatec Registro"


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord! está pronto!')
    print("-="*10)
    await client.change_presence(activity=discord.Streaming(name=message, url='https://github.com/dieguesmosken')) #transmitindo
    print("-="*10)
    print("escrito por @dieguesmosken")
    print("-="*10)
    print(f"status alterado para {message} !")


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'OI {member.name}, Seja bem vindo ao TEST!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!saudacao'):
        hora_atual = datetime.datetime.now().time()
        mensagem = ""

        if hora_atual < datetime.time(12):
            mensagem = f"Bom dia {message.author.name}, como vai você?"
        elif hora_atual < datetime.time(18):
            mensagem = f"Boa tarde {message.author.name}, como vai você?"
        else:
            mensagem = f"Boa noite {message.author.name}, como vai você?"

        await message.channel.send(mensagem)


@client.event
async def on_raw_message_delete(payload):
    print(f'Mensagem deletada: {payload.message_id}')


@client.event
async def on_raw_reaction_add(payload):
    print(f'Reação adicionada: {payload.emoji}')


@client.event
async def on_raw_reaction_remove(payload):
    print(f'Reação removida: {payload.emoji}')


@client.event
async def on_raw_bulk_message_delete(payload):
    print(f'Várias mensagens deletadas: {payload.message_ids}')


client.run(TOKEN)