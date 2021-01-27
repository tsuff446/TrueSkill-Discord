from dotenv import load_dotenv
from discord.ext import commands
import os
from src.spreadsheet_helpers import players_to_spreadsheet, spreadsheet_to_players
from src.player import Player, check_already_exists, find_player
from src.trueskill_helpers import report_match

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

players = spreadsheet_to_players('backups/backups.csv')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="create")
async def create_profile(ctx):
    if len(ctx.message.mentions) > 0:
        mem = ctx.message.mentions[0]
    else:
        mem = ctx.author
    new_player = Player(mem.id, mem.name)

    #checks if player exists
    if check_already_exists(new_player, players):
        await ctx.send("Player already exists")
        return

    #adds player to db
    players.append(new_player)
    players_to_spreadsheet('backups/backups.csv', players)
    await ctx.send("Created profile for " + str(mem.name))

@bot.command(name="report")
async def report(ctx):
    #needs two mentions
    if len(ctx.message.mentions) != 2:
        await ctx.send("Reporting a match requires 2 @s (winner first)")
        return

    winner_id = ctx.message.mentions[0].id
    loser_id = ctx.message.mentions[1].id

    if winner_id == loser_id:
        await ctx.send("Cannot play yourself")
        return

    #find players
    winner = find_player(winner_id, players)
    loser = find_player(loser_id, players)

    if not winner or not loser:
        await ctx.send("One of the players could not be found")
        return
    
    #update ratings
    report_match(winner, loser)
    players_to_spreadsheet('backups/backups.csv', players)
    await ctx.send("Reported Match")
    return

@bot.command(name="profile")
async def display_profile(ctx):
    if len(ctx.message.mentions) == 1:
        mem = ctx.message.mentions[0]
    else:
        mem = ctx.author

    player = find_player(mem.id, players)
    if not player:
        await ctx.send("User not found")
        return

    await ctx.send(str(player.discord_alias) + " | " + "Rating: " + str(player.rating) + " | " + "Wins: " + str(player.wins))
    return

@bot.command(name="backup")
async def backup_data(ctx):
    players_to_spreadsheet('backups/backups.csv', players)
    await ctx.send("Backed up data")
    return

bot.run(TOKEN)
