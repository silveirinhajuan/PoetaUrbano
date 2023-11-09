import os
import asyncio

import discord
from brain import responda, treine
from dotenv import load_dotenv

from pre_processing import preprocess_input, replace_named_entities


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
        ctnt = message.content
        #print(message.content)

        # don't respond to ourselves
        if message.author == self.user:
            return

        if not should_respond:
            if bot_name in ctnt.lower() or bot_nickname in ctnt.lower():
                #print('responder a msg')
                should_respond = True
                await message.reply('Opa, parceiro!', mention_author=True)

            await self.reset_should_respond()
            #print(should_respond)

        if should_respond:
            #print('variavel ficou true')
            if ctnt == 'desligar':
                await message.channel.send('desligando...')
                quit()

            elif ctnt == 'ping':
                await message.channel.send('pong')

            elif ctnt.lower() == 'stop msgs':
                await message.channel.send('qualquer coisa me chama, samurai')
                should_respond = False

            #elif 'meu' in ctnt.lower() and 'nome' in ctnt.lower() and '?' in ctnt.lower():
            #   await message.reply(f'teu nome é {message.author.name}')

            elif 'treine' in ctnt.lower():
                treine()
            
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
                await message.reply(response)
                
        else:
            with open (os.path.join('./dataset.txt'), 'wb') as file:
                file += f'{message.content}\n'


intents = discord.Intents.all()
client = MyClient(intents=intents)
client.run(token)

