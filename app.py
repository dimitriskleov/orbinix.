import os
import discord
from discord.ext import commands
from flask import Flask, jsonify
import asyncio

# Initialize Flask app
app = Flask(__name__)

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot event when it's ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Example command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Function to run the bot asynchronously
async def run_bot():
    token = os.getenv("DISCORD_TOKEN")
    await bot.start(token)

# A simple index route
@app.route('/')
def index():
    return jsonify({"message": "Welcome to your Flask app!"})

# Handler to be used by Vercel (serverless function)
def handler(request):
    # Setup a new event loop to run the bot
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Run the bot asynchronously and handle the request
    loop.run_until_complete(run_bot())

    # Handle the HTTP request using Flask's request context
    with app.request_context(request):
        response = app.full_dispatch_request()
    return response
