import discord
from discord.ext.commands.errors import CommandInvokeError, CommandNotFound
from cricbotlib2 import cricbotlib2 as cb2
from discord.ext import commands, tasks
from embedder import embedder
from config import config

id_container = {}

bot=commands.Bot(command_prefix=config.bot_prefix)

@tasks.loop(seconds=config.STATUS_REFRESH_TIME)
async def activity_changer():
    schedules, ids = cb2.get_schedules(2, 15, searchby=config.TRACK_MATCH)
    if len(schedules) == 0:
        schedules, ids = cb2.get_schedules(2, 5, searchby=None)
        if len(schedules) == 0:data = "No Live match available."
        else:data = cb2.get_activity(ids[0][0], ids[0][1])
    else:data = cb2.get_activity(ids[0][0], ids[0][1])
    await bot.change_presence(activity=discord.Game(name=data), status=discord.Status.idle)

@bot.event
async def on_ready():
    activity_changer.start()
    print('bot is online.')

@bot.command(aliases=['inv', 'invit'])
async def invite(ctx):
    await ctx.send(embed=embedder.invite_embed())

@bot.command(aliases=['jn'])
async def join(ctx):
    link='https://discord.gg/PyzaTzs2cF'
    await ctx.send('Join cricbot development server for any help or feedback/bug report.'+link)

@bot.command(aliases=['source', 'source-code'])
async def code(ctx):
    await ctx.send(embed=embedder.source_embed())

@bot.command(aliases=['credit', 'cred', 'creds'])
async def credits(ctx):
    embed = discord.Embed(title="Cricbot-2.0 : Your own cricket bot", color=0x03f8fc)
    embed.add_field(name='API Disclaim: ', value="I don't own cricbot API. it is owned by Yahoo! cricket. This is an unofficial use of this API which is not public.", inline=False)    
    embed.add_field(name='Developed by:', value='0x0is1', inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['sch', 'routine', 'list'])
async def schedule(ctx, schedule_type=2, limit=5):
    channel_id = ctx.message.channel.id
    search_query = None
    data, ids = cb2.get_schedules(schedule_type-1, limit, search_query)
    id_container[channel_id] = ids
    embed = embedder.schedule_embed(data, limit)
    await ctx.send(embed=embed)

@bot.command(aliases=['scor', 'ms', 'miniscore', 'msc'])
async def score(ctx, match_index=1):
    channel_id = ctx.message.channel.id
    sid, mid, igs = id_container[channel_id][match_index-1]
    data = cb2.get_score(sid, mid)
    embed = embedder.score_embed(data, mid, sid, igs, 2)
    await ctx.send(embed=embed)

@bot.command(aliases=['scd', 'scrd', 'scoreard', 'sd'])
async def scorecard(ctx, match_index=1, inning_index=1):
    channel_id = ctx.message.channel.id
    sid, mid, igs = id_container[channel_id][match_index-1]
    data = cb2.get_scorecard(sid, mid, inning_index-1)
    embed = embedder.scorecard_embed(data, sid, mid, inning_index-1, igs)
    await ctx.send(embed=embed)

@bot.command(aliases=['commentary', 'comm', 'comment', 'commentry'])
async def comments(ctx, match_index=1, limit=5):
    channel_id = ctx.message.channel.id
    sid, mid, igs = id_container[channel_id][match_index-1]
    data = cb2.get_comments(sid, mid, limit)
    embed = embedder.comments_embed(data, sid, mid, limit, igs)
    await ctx.send(embed=embed)

@bot.command(aliases=['pship', 'partner', 'psp', 'synergy'])
async def partnership(ctx, match_index=1, inning_index=1):
    channel_id = ctx.message.channel.id
    sid, mid, igs = id_container[channel_id][match_index-1]
    data = cb2.get_partnership(sid, mid, inning_index-1)
    embed = embedder.partnership_embed(data, sid, mid, inning_index-1, igs)
    await ctx.send(embed=embed)

@bot.command(aliases=['pshipg', 'pgraph', 'pspgraph', 'partnership-graph'])
async def partnershipgraph(ctx, match_index=1, inning_index=1):
    channel_id = ctx.message.channel.id
    sid, mid, igs = id_container[channel_id][match_index-1]
    data = cb2.get_partnershipGraph(sid, mid, inning_index-1)
    embed = embedder.partnershipGraph_embed(data, sid, mid, inning_index-1, igs)
    await ctx.send(file=embed[1], embed=embed[0])

@bot.command(aliases=['fow', 'fall', 'fowgraph', 'out-graph'])
async def fallofwicket(ctx, match_index=1, inning_index=1):
    channel_id = ctx.message.channel.id
    sid, mid, igs = id_container[channel_id][match_index-1]
    data = cb2.get_fallofwicketsGraph(sid, mid, inning_index-1)
    embed = embedder.fallofwicketsGraph_embed(data, sid, mid, inning_index-1, igs)
    await ctx.send(file=embed[1], embed=embed[0])

@bot.command(aliases=['bestbatsman', 'batsman', 'bestbatter', 'batter'])
async def bestbatsmen(ctx, match_index=1, inning_index=1):
    channel_id = ctx.message.channel.id
    sid, mid = id_container[channel_id][match_index-1]
    data = cb2.get_bestbatsmen(sid, mid, inning_index-1)
    embed = embedder.bestbatsmen_embed(data)
    await ctx.send(embed=embed)

@bot.command(aliases=['bestbowler', 'bowlers', 'bestballer', 'bestballers'])
async def bestbowlers(ctx, match_index=1, inning_index=1):
    channel_id = ctx.message.channel.id
    sid, mid = id_container[channel_id][match_index-1]
    data = cb2.get_bestbowlers(sid, mid, inning_index-1)
    embed = embedder.bestbowlers_embed(data)
    await ctx.send(embed=embed)

bot.run(config.auth_token)
