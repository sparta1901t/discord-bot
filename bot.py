import discord
import os
import sys
import asyncio
import time
import json

from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
TOKEN = 'OTYzMDY4MTkyNzE1MDQ2OTEy.YlQtJg.zswA0FsQDDss4dv55HMSC3eafQs'

if not os.path.exists('users.json'):
    with open('users.json', 'w') as file:
        file.write('{}')
        file.close()


BADWORDS = ["хуй", "пидор", "еблан", "блядь"]
LINKS = ["https", "http", "://", ".com", ".ru", ".org", ".net"]


@bot.event
async def on_ready():
    print("- Аккаунт бота -")
    print()
    print(f"Имя бота: {bot.user.name}")
    print(f"ID бота: {bot.user.id}")
    print(f"Токен бота: {TOKEN}")
    print()


    for guild in bot.guilds:
        for member in guild.members:
            with open('users.json', 'r') as file:
                data = json.load(file)
                file.close()

            with open('users.json', 'w') as file:
                data[str(member.id)] = {
                    "WARNS": 0,
                    "CAPS": 0
                }

                json.dump(data, file, indent=4)
                file.close()

@bot.event
async def on_message(message):
    WARN = BADWORDS + LINKS

    for i in range(0, len(WARN)):
        if WARN[i] in message.content.lower():
            await message.delete()
            with open('users.json', 'r') as file:
                data = json.load(file)
                file.close()

            with open('users.json', 'w') as file:
                data[str(message.author.id)]['WARNS'] += 1
                json.dump(data, file, indent=4)

                file.close()

            emb = discord.Embed(
                title="Нарушение",
                description=f"*Ранне, у нарушителя уже было {data[str(message.author.id)]['WARNS'] - 1} нарушений после 5 - бан!!!*",
                timestamp=message.created_at
            )

            emb.add_field(name="Канал:", value=message.channel.mention, inline=True)
            emb.add_field(name="Нарушитель:", value=message.author.mention, inline=True)
            emb.add_field(name="Тип нарушения:", value="Ругательства/ссылки", inline=True)

            await get(message.guild.text_channels, id=967358240801325126).send(embed = emb)

            if data[str(message.author.id)]['WARNS'] >= 5:
                await message.author.ban(reason = "Вы привыси кол-во нарушений")

    if message.content.isupper():
        with open('users.json', 'r') as file:
            data = json.load(file)
            file.close()

        with open('users.json', 'w') as file:
            data[str(message.author.id)]["CAPS"] += 1
            json.dump(data, file, indent=4)

        if data[str(message.author.id)]["CAPS"] >= 3:

            with open('usrs.json', 'w') as file:
                data[str(message.author.id)]["CAPS"] = 0
                data[str(message.author.id)]["WARNS"] += 1

                json.dump(data, file, indent=4)
                file.close()

            emb = discord.Embed(
                title="Нарушение",
                description=f"*Ранне, у нарушителя уже было {data[str(message.author.id)]['WARNS'] - 1} нарушений после 5 - бан!!!*",
                timestamp=message.created_at
            )

            emb.add_field(name="Канал:", value=message.channel.mention, inline=True)
            emb.add_field(name="Нарушитель:", value=message.author.mention, inline=True)
            emb.add_field(name="Тип нарушения:", value="CAPS", inline=True)

            await get(message.guild.text_channels, id=967358240801325126).send(embed=emb)

            if data[str(message.author.id)]['WARNS'] >= 5:
                await message.author.ban(reason = "Вы привыси кол-во нарушений")


#приветствие
@bot.event
async def on_member_join(member):
    await member.send('Приветствую на сервере. Напиши !инфо, чтобы узнать мои функции.')

    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member}, спасибо что зашел на сервер. Не забудь просмотреть лс.')


#прощание
@bot.event
async def on_member_remove(member):
    await member.send('Не забудь вернуться.')

    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member}, покинул наши ряды.')

bot.run(TOKEN)
