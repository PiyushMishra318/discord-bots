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

kakashi_bot = commands.Bot(command_prefix='!', intents=intents)
openai.api_key = os.getenv('OPEN_AI_KEY')

@kakashi_bot.event
async def on_ready():
    print(f'Logged in as {kakashi_bot.user.name}')

@kakashi_bot.command(name="support", help="Very helpful in tough situations.")
async def support(ctx, *args):
    # generate response based on the command name.
    message_content = ' '.join(args); 
    msg = generate_message(message_content)

    # Send the message in the same channel where the command was used
    await ctx.send(msg)


def generate_message(message):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"system","content":"""
    You are Kakashi and you can only refer to yourself as such. You task is very simple. 
    Whenever someone asks you anything you just reply with Have you tried turning it on and off again.
    """},{"role":"user", "content": message}])
    
    return completion.choices[0].message.content;

@kakashi_bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # This error occurs when an unknown command is invoked.
        # You can choose to ignore it or respond accordingly.
        pass  # You can ignore the error

kakashi_bot.run(os.getenv('KAKASHI_BOT_ID'))
