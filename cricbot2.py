import discord, os
from discord.ext.commands.errors import CommandInvokeError, CommandNotFound
from cricbotlib2 import cricbotlib2 as cb2
from discord.ext import commands, tasks
from embedder import embedder

id_container = {}

bot=commands.Bot(command_prefix='cb ')

@bot.event
async def on_ready():
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
async def schedule(ctx, search_query=None, schedule_type=2, limit=5):
    channel_id = ctx.message.channel.id
    data, ids = cb2.get_schedules(schedule_type-1, limit, search_query)
    id_container[channel_id] = ids
    embed = embedder.schedule_embed(data, limit)
    await ctx.send(embed=embed)

@bot.command(aliases=['scor', 'skor', 'miniscore', 'msc'])
async def score(ctx, match_index=1):
    channel_id = ctx.message.channel.id
    sid, mid = id_container[channel_id][match_index-1]
    data = cb2.get_score(sid, mid)
    embed = embedder.score_embed(data, mid, sid, 2)
    await ctx.send(embed=embed)

@bot.command(aliases=['scd', 'scrd', 'scoreard', 'sd'])
async def scorecard(ctx, match_index=1, inning_index=1):
    channel_id = ctx.message.channel.id
    sid, mid = id_container[channel_id][match_index-1]
    data = cb2.get_scorecard(sid, mid, inning_index-1)
    embed = embedder.scorecard_embed(data, sid, mid, inning_index-1)
    await ctx.send(embed)

auth_token = os.environ.get('EXPERIMENTAL_BOT_TOKEN')
bot.run(auth_token)
