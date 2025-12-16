import os
import discord
from discord.ext import commands
from flask import Flask, jsonify
import asyncio
import threading

# Initialize Flask app
app = Flask(__name__)

# Initialize the bot (without running it immediately)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Example command for the bot
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Function to start the bot asynchronously
async def run_bot():
    token = os.getenv("DISCORD_TOKEN")
    await bot.start(token)

# Vercel expects the handler function, not `app.run()`
def handler(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Run bot asynchronously and return the result
    loop.run_until_complete(run_bot())

    with app.request_context(request):
        response = app.full_dispatch_request()
    return response

# A simple index route
@app.route('/')
def index():
    return jsonify({"message": "Welcome to your Flask app!"})

