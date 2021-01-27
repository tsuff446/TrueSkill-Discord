from dotenv import load_dotenv
from discord.ext import tasks, commands
import os
from src import matchmaking
from src.spreadsheet_helpers import players_to_spreadsheet, spreadsheet_to_players
from src.player import Player, check_already_exists, find_player
from src.trueskill_helpers import report_match
from src.matchmaking import PlayerQueue

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

players = spreadsheet_to_players('backups/backups.csv')
matchmaking_queue = PlayerQueue()

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    auto_prune_queue.start()

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

#enter queue
#ex. !queue 5 (Enter queue for next 5 minutes)
@bot.command(name="queue")
async def backup_data(ctx):
    message = ctx.message.content.strip().split()
    if len(message) == 1:
        #default queue time
        message = "30"
    else:
        message = message[1]

    if not message.isnumeric():
        await ctx.send("Must be in queue for a whole number amount of minutes")
        return

    queue_time = int(message)

    if queue_time > 180:
        await ctx.send("You cannot queue for longer than 3 hours")
        return
    
    if queue_time <= 0:
        await ctx.send("Must queue for at least 1 minute")
        return

    player = find_player(ctx.author.id, players)
    if not player:
        await ctx.send("You have not created a profile yet. Type !create to make a profile")
        return

    if matchmaking_queue.check_in_queue(player):
        await ctx.send("Already in queue!")
        return

    matchmaking_queue.enqueue_player(player, queue_time)
    await ctx.send("Successfully queued for " + str(queue_time) + " minutes")
    return


#leaves queue
@bot.command(name="leave")
async def backup_data(ctx):
    player = find_player(ctx.author.id, players)

    if not player:
        await ctx.send("You have not created a profile yet. Type !create to make a profile")
        return

    if matchmaking_queue.remove_player(player):
        await ctx.send("Successfully removed from queue")
    else:
        await ctx.send("You were not in queue")
    return

#displays queue
@bot.command(name="show_queue")
async def backup_data(ctx):
    message = matchmaking_queue.display_queue()
    if len(message) > 0:
        await ctx.send(message)
    else:
        await ctx.send("Queue is currently empty")
    return

# updates queue
@tasks.loop(seconds=15.0)
async def auto_prune_queue():
    matchmaking_queue.prune_queue()

bot.run(TOKEN)
