import discord, base64
from discord.ext.commands.errors import CommandInvokeError, CommandNotFound
from cricbotlib2 import cricbotlib2 as cb2
from discord.ext import commands, tasks
from embedder import embedder, reaction_listener, help_embed
from config import config
from discord import FFmpegPCMAudio

id_container = {}
ids4updater = []

bot=commands.Bot(command_prefix=config.bot_prefix)
bot.remove_command('help')

@tasks.loop(seconds=config.STATUS_REFRESH_TIME)
async def activity_changer():
    schedules, ids, sids = cb2.get_schedules(1, 40, searchby=config.TRACK_MATCH)
    if len(schedules) == 0:
        schedules, ids, _ = cb2.get_schedules(2, 5, searchby=None)
        if len(schedules) == 0:data = "No Live match available."
        else:data = cb2.get_activity(ids[0][0], ids[0][1])
    else:data = cb2.get_activity(sids[0], sids[1])
    await bot.change_presence(activity=discord.Game(name=data), status=discord.Status.idle)

@tasks.loop(seconds=config.STATUS_REFRESH_TIME)
async def auto_updater():
    if len(ids4updater) > 0:
        for ids in ids4updater:
            channelId, messageId = ids
            channel = await bot.fetch_channel(channel_id=channelId)
            msg = await channel.fetch_message(messageId)
            try:
                if "NUA" not in msg.embeds[0].footer.text\
                    and "UA" in msg.embeds[0].footer.text:
                    await msg.add_reaction(config.arrows_emojis[4])
            except Exception as e:print(e)

@bot.event
async def on_ready():
    activity_changer.start()
    auto_updater.start()
    print('bot is online.')

@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    if not user.bot and message.author == bot.user:
        await message.remove_reaction(str(reaction), user)
        channel = message.channel
        reaction = str(reaction)
        sessionid = message.embeds[0].footer.text.split('-')
        if sessionid[0] == "SCH":
            schedule_type = int(sessionid[2])
            limit = int(sessionid[3])
            module_name = sessionid[1]
            if reaction in config.arrows_emojis:
                if reaction == config.arrows_emojis[0]:limit -= 5
                if reaction == config.arrows_emojis[1]:limit += 5
                if limit < 5:limit = 5
                data, ids = cb2.get_schedules(schedule_type, limit, None)
                id_container[channel.id] = ids
                embed = embedder.schedule_embed(data, schedule_type, limit, module_name)
                await message.edit(embed=embed)               
            if reaction in config.num_emojis:
                matchindex = config.num_emojis.index(reaction)
                sessionid.pop(0)
                sid, mid, igs = id_container[channel.id][matchindex-1]
                embed = reaction_listener.on_schedule_select(sessionid, sid, mid)
                await message.edit(embed=embed)
                try:
                    for i in range(1, 6):
                        await message.remove_reaction(config.num_emojis[i], bot.user)
                except Exception:pass
                try:
                    for i in range(0, 2):
                        await message.remove_reaction(config.arrows_emojis[i], bot.user)
                except Exception:pass
                try:
                    if "NUA" not in embed.footer.text and "UA" in embed.footer.text:
                        await message.add_reaction(config.arrows_emojis[5])
                        await message.add_reaction(config.arrows_emojis[6])
                    if igs != None and "INN" in embed.footer.text:    
                        for i in range(1, int(igs)+1):    
                            await message.add_reaction(config.num_emojis[i])
                except Exception:pass                
        if sessionid[0] == "INN":
            if reaction in config.num_emojis:
                sessionid.pop(0)
                sid, mid = int(sessionid[1]), int(sessionid[2])
                inning_index = config.num_emojis.index(reaction)
                try:
                    embed = reaction_listener.on_inning_select(sessionid, sid, mid, inning_index-1)
                    try:
                        for i in range(1, 5):
                            await message.remove_reaction(config.num_emojis[i], bot.user)
                    except Exception:pass
                    try:
                        for i in range(0, 2):
                            await message.remove_reaction(config.arrows_emojis[i], bot.user)
                    except Exception:pass
                    
                    if len(embed) == 2:
                        try:await message.delete()
                        except Exception:pass
                        message = await channel.send(embed=embed[0], file=embed[1])
                    else: 
                        await message.edit(embed=embed)
                        if "NUA" not in embed.footer.text and "UA" in embed.footer.text:
                            await message.add_reaction(config.arrows_emojis[5])
                            await message.add_reaction(config.arrows_emojis[6])
                except IndexError:pass
        if reaction == config.arrows_emojis[5]:
            ids4updater.append((channel.id, message.id))
        if reaction == config.arrows_emojis[6]:
            for i in ids4updater:
                if i[1] == message.id:
                    ids4updater.remove(i)
    if user.bot and message.author == bot.user:
        channel = message.channel
        reaction = str(reaction)
        sessionid = message.embeds[0].footer.text.split('-')
        if reaction == config.arrows_emojis[4]:
            await message.remove_reaction(str(reaction), user)
            embed = reaction_listener.refresher(sessionid)
            try:
                for i in range(1, 5):
                    await message.remove_reaction(config.num_emojis[i], bot.user)
            except Exception:pass
            try:
                for i in range(0, 2):
                    await message.remove_reaction(config.arrows_emojis[i], bot.user)
            except Exception:pass
            if len(embed) == 2:
                try:await message.delete()
                except Exception:pass
                await channel.send(embed=embed[0], file=embed[1])
            else:
                await message.edit(embed=embed)
                if "NUA" not in embed.footer.text and "UA" in embed.footer.text:
                    await message.add_reaction(config.arrows_emojis[5])
                    await message.add_reaction(config.arrows_emojis[6])

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('`Unknown command` \n Please use right command to operate. `help` for commands details.')
    if isinstance(error, CommandInvokeError):
        return

@bot.command(aliases=['hlp', 'h'])
async def help(ctx):
    await ctx.send(embed=help_embed.embed())

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
    embed.add_field(name='API Disclaim: ', value="This API is owned by ESPNsports cricket and radio garden. It is an unofficial use of this API which is not public.", inline=False)    
    embed.add_field(name='Developed by:', value='0x0is1', inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=['scor', 'ms', 'miniscore', 'msc'])
async def score(ctx, schedule_type=1):
    channel_id = ctx.message.channel.id
    data, ids , _ = cb2.get_schedules(schedule_type, 5, None)
    id_container[channel_id] = ids
    embed = embedder.schedule_embed(data, schedule_type, 5, "SC")
    message = await ctx.send(embed=embed)
    await message.add_reaction(config.arrows_emojis[0])
    for i in range(1, 6):
        await message.add_reaction(config.num_emojis[i])
    await message.add_reaction(config.arrows_emojis[1])

@bot.command(aliases=['scd', 'scrd', 'scoreard', 'sd'])
async def scorecard(ctx, schedule_type=1):
    channel_id = ctx.message.channel.id
    data, ids , _ = cb2.get_schedules(schedule_type, 5, None)
    id_container[channel_id] = ids
    embed = embedder.schedule_embed(data, schedule_type, 5, "SCRD")
    message = await ctx.send(embed=embed)
    await message.add_reaction(config.arrows_emojis[0])
    for i in range(1, 6):
        await message.add_reaction(config.num_emojis[i])
    await message.add_reaction(config.arrows_emojis[1])

@bot.command(aliases=['commentary', 'comm', 'comment', 'commentry'])
async def comments(ctx, schedule_type=1):
    channel_id = ctx.message.channel.id
    data, ids , _ = cb2.get_schedules(schedule_type, 5, None)
    id_container[channel_id] = ids
    embed = embedder.schedule_embed(data, schedule_type, 5, "CMTRY")
    message = await ctx.send(embed=embed)
    await message.add_reaction(config.arrows_emojis[0])
    for i in range(1, 6):await message.add_reaction(config.num_emojis[i])
    await message.add_reaction(config.arrows_emojis[1])

@bot.command(aliases=['pship', 'partner', 'psp', 'synergy'])
async def partnership(ctx, schedule_type=1):
    channel_id = ctx.message.channel.id
    data, ids , _ = cb2.get_schedules(schedule_type, 5, None)
    id_container[channel_id] = ids
    embed = embedder.schedule_embed(data,schedule_type, 5, "PSP")
    message = await ctx.send(embed=embed)
    await message.add_reaction(config.arrows_emojis[0])
    for i in range(1, 6):await message.add_reaction(config.num_emojis[i])
    await message.add_reaction(config.arrows_emojis[1])

@bot.command(aliases=['pshipg', 'pgraph', 'pspgraph', 'partnership-graph'])
async def partnershipgraph(ctx, schedule_type=1):
    channel_id = ctx.message.channel.id
    data, ids , _ = cb2.get_schedules(schedule_type, 5, None)
    id_container[channel_id] = ids
    embed = embedder.schedule_embed(data, schedule_type, 5, "PSPG")
    message = await ctx.send(embed=embed)
    await message.add_reaction(config.arrows_emojis[0])
    for i in range(1, 6):
        await message.add_reaction(config.num_emojis[i])
    await message.add_reaction(config.arrows_emojis[1])

@bot.command(aliases=['fow', 'fall', 'fowgraph', 'out-graph'])
async def fallofwicket(ctx, schedule_type=1):
    channel_id = ctx.message.channel.id
    data, ids , _ = cb2.get_schedules(schedule_type, 5, None)
    id_container[channel_id] = ids
    embed = embedder.schedule_embed(data, schedule_type, 5, "FOW")
    message = await ctx.send(embed=embed)
    await message.add_reaction(config.arrows_emojis[0])
    for i in range(1, 6):
        await message.add_reaction(config.num_emojis[i])
    await message.add_reaction(config.arrows_emojis[1])

@bot.command(aliases=['bestbatsman', 'batsmen', 'bestbatter', 'batter'])
async def bestbatsmen(ctx, schedule_type=1):
    channel_id = ctx.message.channel.id
    data, ids , _ = cb2.get_schedules(schedule_type, 5, None)
    id_container[channel_id] = ids
    embed = embedder.schedule_embed(data, schedule_type, 5, "BBT")
    message = await ctx.send(embed=embed)
    await message.add_reaction(config.arrows_emojis[0])
    for i in range(1, 6):await message.add_reaction(config.num_emojis[i])
    await message.add_reaction(config.arrows_emojis[1])

@bot.command(aliases=['bestbowler', 'bowlers', 'bestballer', 'bestballers'])
async def bestbowlers(ctx, schedule_type=1):
    channel_id = ctx.message.channel.id
    data, ids , _ = cb2.get_schedules(schedule_type, 5, None)
    id_container[channel_id] = ids
    embed = embedder.schedule_embed(data, schedule_type, 5, "BBL")
    message = await ctx.send(embed=embed)
    await message.add_reaction(config.arrows_emojis[0])
    for i in range(1, 6):await message.add_reaction(config.num_emojis[i])
    await message.add_reaction(config.arrows_emojis[1])

@bot.command(aliases=['listen'])
async def radio(ctx, cmd="start"):
    URL = base64.b64decode("aHR0cHM6Ly9henVyYS5zaG91dGNhLnN0L3JhZGlvLzg2MjAvcmFkaW8ubXAz")
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    if ctx.message.author.voice == None:
        await ctx.send("No Voice Channel", "You need to be in a voice channel to use this command!")
        return
    starter_channel = ctx.message.author.voice.channel
    if cmd=="start":
        vc = await starter_channel.connect()
        source = FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)
        vc.play(source)
    else:
        await ctx.guild.voice_client.disconnect()

bot.run(config.auth_token)
