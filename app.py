import os
import discord
from discord.ext import commands
from flask import Flask, jsonify
import asyncio

# Initialize Flask app
app = Flask(__name__)

# Initialize the bot (without running it immediately)
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

# Vercel's handler function (this is what Vercel expects)
def handler(request):
    # Setup new event loop for running bot asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Run bot during the HTTP request
    loop.run_until_complete(run_bot())

    # Handle the Flask request
    with app.request_context(request):
        response = app.full_dispatch_request()
    return response
