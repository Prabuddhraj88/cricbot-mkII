import discord
from config import config

def embed():
    embed = discord.Embed(title="Cricbot-2.0", color=0x03f8fc, description="All cricket info on Discord.")
    embed.add_field(name="Commands:", value="All commands requires match type:\n`0` for `schedule`\n`1` for `live`\n`2` for `ended` matches", inline=False)
    embed.add_field(name="Score:", value='`score [0/1/2]`', inline=True)
    embed.add_field(name="Scorecard:", value='`scorecard [0/1/2]`', inline=True)
    embed.add_field(name="Partnership:", value='`partnership [0/1/2]`', inline=True)
    embed.add_field(name="Partnership Graphs:", value='`pgraph [0/1/2]`', inline=True)
    embed.add_field(name="Fall of wickets:", value='`fow [0/1/2]`', inline=True)
    embed.add_field(name="Commentary:", value='`commentary [0/1/2]`', inline=True)
    embed.add_field(name="Best Batsmen:", value='`batsmen [0/1/2]`', inline=True)
    embed.add_field(name="Best Bowlers:", value='`bowlers [0/1/2]`', inline=True)
    embed.add_field(name="Rankings:", value='`rank`', inline=True)
    embed.add_field(name="Radio:", value='`radio [start/stop]`', inline=True)
    embed.add_field(name="Invite bot:", value='`inv`', inline=True)
    embed.add_field(name="Join server:", value='`join`', inline=True)
    embed.add_field(name="Source code:", value='`source`', inline=True)
    embed.add_field(name="Credits:", value='`credits`', inline=True)
    embed.add_field(name="help:", value='`help`', inline=True)
    embed.add_field(name="Emote Description:", value=f'{config.arrows_emojis[5]} to turn on Auto-update\n\
        {config.arrows_emojis[6]} to turn off Auto-update.', inline=True)
    return embed

