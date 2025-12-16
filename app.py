import os
from flask import Flask, jsonify
import discord
from discord.ext import commands
import threading

# Flask App setup
app = Flask(__name__)

# Discord Bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Bot event for on_ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Example Discord Bot Command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# This function runs the bot
def run_bot():
    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)

# Flask route to trigger when someone visits the page
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Flask and Discord Bot integration!"})

if __name__ == '__main__':
    # Run the Discord bot in a separate thread
    threading.Thread(target=run_bot).start()
    app.run(debug=True, host='0.0.0.0', port=5000)
