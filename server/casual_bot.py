import discord
from discord.ext import commands
import openai
import requests
from discord import Intents
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# giphy api

# Your Giphy API key
api_key = os.getenv('GIPHY_API_KEY')

# URL for Giphy's Random API endpoint
base_url = "https://api.giphy.com/v1/gifs/random"

# Parameters for the API request
params = {
    "api_key": api_key,
    "tag": "meme",  # You can specify tags to filter results if needed
}

intents = Intents.default()
intents.presences = True  # To access presence updates (e.g., online/offline status)
intents.message_content = True

casual_bot = commands.Bot(command_prefix='!', intents=intents)

@casual_bot.event
async def on_ready():
    print(f'Logged in as {casual_bot.user.name}')

@casual_bot.command(name="meme", help="Sends random memes just like old casual used to. We miss him.")
async def meme(ctx):
    # generate response based on the command name.
    message = generate_message()

    embed = discord.Embed()
    embed.set_image(url=message);

    # Send the message in the same channel where the command was used
    await ctx.send(embed=embed)

def generate_message():
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            meme_url = data["data"]["images"]["original"]["url"]
            return meme_url;
        else:
            return "No meme found."
    else:
        return "Failed to fetch a meme"

@casual_bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # This error occurs when an unknown command is invoked.
        # You can choose to ignore it or respond accordingly.
        pass  # You can ignore the error

casual_bot.run(os.getenv('CASUAL_BOT_ID'))
    
