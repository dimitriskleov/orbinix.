import os
import discord
from discord.ext import commands
from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot event for when it's ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Simple ping command for the bot
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Function to start the bot within a serverless request context
async def run_bot():
    token = os.getenv("DISCORD_TOKEN")
    await bot.start(token)

# Vercel serverless function to handle requests and run the bot
@app.route('/')
def index():
    # Start the bot for this request (use async/await)
    from asyncio import run
    run(run_bot())  # Run the bot asynchronously
    return jsonify({"message": "Bot is now running and online!"})

# Vercel expects the handler function, not `app.run()`
def handler(request):
    # Call the Flask app's request handling
    with app.request_context(request):
        response = app.full_dispatch_request()
    return response
