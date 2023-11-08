import os

from brain import responda, treine
from dotenv import load_dotenv

import discord

import asyncio

load_dotenv()

token = os.getenv('MYTOKEN')

bot_name = "poeta urbano"
bot_nickname = 'poeta'
should_respond = False


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def reset_should_respond(self):
        print('contando 10mmin')
        global should_respond
        await asyncio.sleep(10 * 60)  # espera 10 minutos
        print('TIME OUT: call again bot with "poeta urbano" or "poeta"')
        should_respond = False

    async def on_message(self, message):
        global should_respond
        #print(message.content)

        # don't respond to ourselves
        if message.author == self.user:
            return
        


        if bot_name in message.content.lower() or bot_nickname in message.content.lower():
            #print('responder a msg')
            should_respond = True
            await message.reply('Opa, parceiro!', mention_author=True)

            await self.reset_should_respond()
            #print(should_respond)

        if should_respond:
            #print('variavel ficou true')
            if message.content == 'desligar':
                await message.channel.send('desligando...')
                quit()

            elif message.content == 'ping':
                await message.channel.send('pong')

            elif message.content.lower() == 'qual teu nome?' or message.content.lower() == 'qual seu nome?':
                await message.channel.send('LUANA COMEDORA DE XERECA')

            elif message.content.lower() == 'stop msgs':
                await message.channel.send('qualquer coisa me chama, samurai')
                should_respond = False

            elif 'meu' in message.content.lower() and 'nome' in message.content.lower() and '?' in message.content.lower():
                await message.reply(f'teu nome é {message.author.name}')

            elif 'treine' in message.content.lower():
                treine()
            
            else:
                response = responda(message.content)
                await message.reply(response)
                
        else:
            responda(message.content)


intents = discord.Intents.all()
client = MyClient(intents=intents)
client.run(token)