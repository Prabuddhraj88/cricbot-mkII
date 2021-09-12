import discord
from requests.sessions import session

def invite_embed():
    embed = discord.Embed(title='cricbot Invite',
        url='https://discord.com/api/oauth2/authorize?client_id=830809161599025202&permissions=10304&scope=bot',
        description='Invite cricbot on your server.', color=0x03f8fc
    )
    return embed

def source_embed():
    source_code = 'https://github.com/0x0is1/cricbot-mkII'
    embed = discord.Embed(title='cricbot Source code',
        url=source_code,
        description='Visit cricbot source code.', color=0x03f8fc
    )
    return embed

def hex2discolor(hexcolor:str):
    if hexcolor is None: return 0x03f8fc
    r, g, b = tuple(int(hexcolor.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    return discord.Color.from_rgb(r, g, b)

def score_embed(data, mid, sid, colorIndex=1):
    updateStatus = 'NUA'
    if data[5] == 'LIVE': 
        updateStatus = 'UA'
    sessionid = f'SC-{updateStatus}-{mid}-{sid}'
    embed = discord.Embed(title=data[0], color=hex2discolor(data[10][colorIndex-1]))
    embed.set_author(name=data[5], icon_url=data[11][colorIndex-1])
    embed.add_field(name=f'{data[1]} {data[4]}', value=f'**Date**: {data[3]}\n**Venue**: {data[2]}', inline=False)
    embed.add_field(name='Score', value=f'{data[7]}\n{data[6]}', inline=False)
    if data[7+1] is not None:
        embed.add_field(name="Batsmen", value=data[7+1], inline=False)
        embed.add_field(name="Bowlers", value=data[9], inline=False)
    embed.set_footer(text=sessionid, icon_url=data[11][colorIndex-1])
    return embed

def schedule_embed(raw_data, limit):
    sessionid = f"SCH-NUA-{limit}"
    embed = discord.Embed(title="Schedule", color=0x03f8fc)
    for j, i in enumerate(raw_data):
        embed.add_field(name=f"{str(j+1)}. {i[0]} | {i[4]} | {i[5]}", value=f"{i[1]}\n**Date**: {i[3]} |  **Venue**: {i[2]}\n*{i[6]}*", inline=False)
    embed.set_footer(text=sessionid)
    return embed