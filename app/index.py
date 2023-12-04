import os
import asyncio

from dataset import dataset

from voz import speak_this
from changes import change_audio_or_text

import discord
from brain import responda, treine
from dotenv import load_dotenv
import aiohttp
import random

from pre_processing import preprocess_input, replace_named_entities

import speech_recognition as sr


load_dotenv()

token = os.getenv('MYTOKEN')

bot_name = "poeta urbano"
bot_nickname = 'poeta'
should_respond = False


class MyClient(discord.Client):
    channels = list()
    
    async def on_ready(self):
        print('Logged on as', self.user)

    async def must_time_without_msg(self):
        global should_respond
        await asyncio.sleep(12 * 60 * 60)
        await self.channels[-1].send('@everyone, esqueceram de mim?')
        should_respond = True
        await self.reset_should_respond()
    
    async def reset_should_respond(self):
        print('contando 10mmin')
        global should_respond
        await asyncio.sleep(10 * 60)  # espera 10 minutos
        print('TIME OUT: call again bot with "poeta urbano" or "poeta"')
        should_respond = False
        await self.must_time_without_msg()
        
    async def on_message(self, message):
        global should_respond
        ctnt = message.content
        #print(message.type)

        # don't respond to ourselves
        if message.author == self.user:
            return
        
        elif str(message.channel) == 'memes':
            print('caiu aqui')
            print(message.attachments)
            if message.attachments:
                for attachment in message.attachments:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as resp:
                            if resp.status != 200:
                                return await message.channel.send('Deu merda, baixei nn...')
                            else:
                                with open(os.path.join('./app/memes', attachment.filename), 'wb') as f:
                                    f.write(await resp.read())
                                    await message.channel.send('Baixei, chapa!')

        elif not should_respond:
            if bot_name in ctnt.lower() or bot_nickname in ctnt.lower():
                #print('responder a msg')
                should_respond = True
                with message.channel.typing():
                    await asyncio.sleep(1)
                    await message.reply('Opa, parceiro!', mention_author=True)

                await self.reset_should_respond()
            else:
                print('ta recebendo a msg')
                if bot_name in ctnt:
                    ctnt = ctnt.replace(bot_name, '')
                if bot_nickname in ctnt:
                    ctnt = ctnt.replace(bot_nickname, '')
                ctnt = preprocess_input(ctnt)
                ctnt = replace_named_entities(ctnt)
                with open ('./dataset.txt', 'a', encoding='utf-8') as file:
                    file.write(f'\n{message.content}')

        elif should_respond:
            if not message.channel in self.channels:
                self.channels.append(message.channel)
                 
            if ctnt == 'desligar':
                await message.channel.send('desligando...')
                quit()

            elif ctnt == 'ping':
                await message.channel.send('pong')

            elif ctnt.lower() == 'dorme poeta':
                await message.channel.send('ui, mó soninho')
                await message.channel.send('qualquer coisa me chama, samurai')
                should_respond = False
                await self.must_time_without_msg()

            #elif 'meu' in ctnt.lower() and 'nome' in ctnt.lower() and '?' in ctnt.lower():
            #   await message.reply(f'teu nome é {message.author.name}')

            elif 'treine' in ctnt.lower():
                async with message.channel.typing():
                    file = ''
                    asyncio.sleep(1)
                    await message.reply(f'treinando com os seguintes dados')
                    file = open('dataset.txt', 'r', encoding='utf-8')
                    try:
                        await message.channel.send(f'{dataset} {[row for row in file]}')
                        treine()
                        await message.channel.send(f'treinamento concluido')
                    except: 
                        treine()
                        await message.channel.send(f'não consegui mandar os dados, mas treinamento foi feito com *SUCESSO*')
            
            else:
                if bot_name in ctnt:
                    ctnt = ctnt.replace(bot_name, '')
                if bot_nickname in ctnt:
                    ctnt = ctnt.replace(bot_nickname, '')
                ctnt = preprocess_input(ctnt)
                ctnt = replace_named_entities(ctnt)
                response = responda(ctnt)
                print(
                    f'{message.author}: {message.content}', 
                      f'ctnt: {ctnt}', 
                     f'response: {response}'
                )
                if change_audio_or_text() == 23:
                    await speak_this(response)
                    await message.channel.send(file=discord.File(open('audio.mp3', 'rb'), f'{response}.mp3'))
                elif change_audio_or_text() == 20:
                    files = os.listdir('./app/memes')
                    random_file = random.choice(files)
                    await message.channel.send(file=discord.File(open(f'./app/memes/{random_file}', 'rb'), f'{random_file}'))
                else:
                    async with message.channel.typing():
                        await asyncio.sleep(1)
                        await message.channel.send(response)
                


intents = discord.Intents.all()
client = MyClient(intents=intents)
client.run(token)

