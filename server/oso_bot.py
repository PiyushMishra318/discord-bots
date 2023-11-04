import discord
from discord.ext import commands
import openai
from discord import Intents

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

intents = Intents.default()
intents.presences = True  # To access presence updates (e.g., online/offline status)
intents.message_content = True

oso_bot = commands.Bot(command_prefix='!', intents=intents)
openai.api_key = os.getenv('OPEN_AI_KEY')

@oso_bot.event
async def on_ready():
    print(f'Logged in as {oso_bot.user.name}')

@oso_bot.command(name="chat", help="Better oso?")
async def chat(ctx, *args):
    # generate response based on the command name.
    message_content = ' '.join(args)
    message = generate_message("chat", message_content)

    # Send the message in the same channel where the command was used
    await ctx.send(message)

@oso_bot.command(name="joke", help="Tells a random joke")
async def joke(ctx):
    # generate response based on the command name.
    message = generate_message("joke", "")

    # Send the message in the same channel where the command was used
    await ctx.send(message)


def generate_message(command, message):
    if command == "chat":
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"system", "content":"""Your name is OSO and always refer to
        yourself as such.
        You are chat bot meant to conversate like you are a friend of the people that interact with you.
        Be funny, kind and helpful whenever you are asked something or if someone is trying to make a conversation with you.
        You are interacting with people on discord servers so please be mindful of the internet lingo such as cool, pog, based etc"""},
                                                                                   {"role": "user", "content": message}])
        return completion.choices[0].message.content

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"system","content":"""You are bot that generates random jokes.
    Make sure to never repeat a joke.
    Your joke topics are as follows: Games, Movies, Horror Movies, Minecraft.
    Just pick one of these topics and generate a joke."""},{"role":"user", "content": "Tell me a joke"}])
    
    return completion.choices[0].message.content;

@oso_bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # This error occurs when an unknown command is invoked.
        # You can choose to ignore it or respond accordingly.
        pass  # You can ignore the error

oso_bot.run(os.getenv('OSO_BOT_ID'))
