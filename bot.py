from src.player import Player
from src.trueskill_helpers import check_fair, report_match
import numpy as np
from src.spreadsheet_helpers import players_to_spreadsheet, spreadsheet_to_players
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
