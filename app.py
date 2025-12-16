import os
import discord
from discord.ext import commands
from flask import Flask, jsonify
import asyncio
import threading

# Initialize Flask app
app = Flask(__name__)

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Example command for the bot
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Function to run the bot asynchronously
async def run_bot():
    token = os.getenv("DISCORD_TOKEN")
    await bot.start(token)

# A simple route to test the Flask app
@app.route('/')
def index():
    return jsonify({"message": "Welcome to your Flask app!"})

# The function that handles the serverless request and runs the bot
def handler(request):
    # Start the bot asynchronously for this request
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

    # Handle the Flask request
    with app.request_context(request):
        response = app.full_dispatch_request()
    return response
