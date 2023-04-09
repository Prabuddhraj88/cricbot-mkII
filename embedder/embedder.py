import discord

def invite_embed():
    embed = discord.Embed(title="cricbot Invite",
                          url="https://discord.com/api/oauth2/authorize?client_id=830809161599025202&permissions=10304&scope=bot",
                          description="Invite cricbot on your server.", color=0x03f8fc
                          )
    return embed

def source_embed():
    source_code = "https://github.com/0x0is1/cricbot-mkII"
    embed = discord.Embed(title="cricbot Source code",
                          url=source_code,
                          description="Visit cricbot source code.", color=0x03f8fc
                          )
    return embed

def hex2discolor(hexcolor: str):
    if hexcolor is None:
        return 0x03f8fc
    r, g, b = tuple(int(hexcolor.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    return discord.Color.from_rgb(r, g, b)

def string_validator(string: str, limit: int):
    chars = list("ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ")
    default_chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    new_string = ""
    string = str(string)[:limit]
    for i in string.upper():
        if i not in default_chars:new_string += i;continue
        new_string += chars[default_chars.index(i)]
    spaces = limit-len(new_string)
    return new_string + "　"*spaces

def score_embed(data, mid, sid, colorIndex=1):
    updateStatus = "NUA"
    if data[5] == "LIVE" or data[5] == "PRE":
        updateStatus = "UA"
    sessionid = f"SC-{updateStatus}-{sid}-{mid}-{colorIndex}"
    embed = discord.Embed(
        title=data[0], color=hex2discolor(data[10][colorIndex-1]))
    embed.set_author(name=data[5], icon_url=data[11][colorIndex-1])
    embed.add_field(name=f"{data[1]} {data[4]}",
                    value=f"**Date**: {data[3]}\n**Venue**: {data[2]}", inline=False)
    embed.add_field(name="Score", value=f"{data[7]}\n{data[6]}", inline=False)
    if data[7+1] is not None:
        embed.add_field(name="Batsmen", value=data[7+1], inline=False)
        embed.add_field(name="Bowlers", value=data[9], inline=False)
    embed.set_footer(text=sessionid, icon_url=data[11][colorIndex-1])
    return embed

def schedule_embed(data, matchtype, limit, module_name):
    sessionid = f"SCH-{module_name}-{matchtype}-{limit}"
    embed = discord.Embed(title=f"Schedule | {matchtype}", color=0x03f8fc)
    for j, i in enumerate(data):
        embed.add_field(name=f"{str(j+1)}. {i[0]} | {i[4]} | {i[5]}",
                        value=f"{i[1]}\n**Date**: {i[3]} |  **Venue**: {i[2]}\n*{i[6]}*", inline=False)
    embed.set_footer(text=sessionid)
    return embed

def scorecard_embed(data, sid, mid, inning_index):
    updateStatus = "NUA"
    team_details, scorecardBat, scorecardBowl = data
    if team_details[6] == "LIVE" or data[6] == "PRE": updateStatus = "UA"
    sessionid = f"SCRD-{updateStatus}-{sid}-{mid}-{inning_index}"
    embed = discord.Embed(title=f"{team_details[0]} | {team_details[6]}", color=hex2discolor(team_details[1]))
    embed.set_author(name="Scorecard", icon_url=team_details[2])
    embed.set_thumbnail(url=team_details[2])
    embed.add_field(name="Score:", value=f" {team_details[3]}/{team_details[4]} ({team_details[5]})", inline=True)
    embed_data = "```py\n"
    embed_data += string_validator("Name", 7) + " "
    embed_data += "Run　Ball　4s　6s　S.R\n"
    embed_data += "```"
    embed_data += "```py\n"
    for i in scorecardBat:    
        embed_data += string_validator(i[0].split(" ")[0], 7) + " "
        embed_data += f"{i[1]:03}　{i[2]:03}　{i[3]:02}　{i[4]:02}　{i[5]:.0f}\n"
    embed_data += "```\n"
    embed.add_field(name="Batting", value=embed_data, inline=False)
    embed_data = "```py\n"
    embed_data += string_validator("Name", 7) + " "
    embed_data += "Run　Ovrs　Wt　Md　E.R\n"
    embed_data += "```"
    embed_data += "```py\n"
    for i in scorecardBowl:
        embed_data += string_validator(i[0].split(" ")[0].split("-")[0], 7) + " "
        embed_data += f"{i[1]:03}　{i[2]:4.1f}　{i[3]:02}　{i[4]:02}　{i[5]:.1f}\n"
    embed_data += "```"
    embed.add_field(name="Bowling", value=embed_data, inline=False)
    embed.set_footer(text=sessionid, icon_url=team_details[2])
    return embed

def comments_embed(data, sid, mid, limit):
    updateStatus = "NUA"
    if data[1] == "LIVE": updateStatus = "UA"
    sessionid = f"CMTRY-{updateStatus}-{sid}-{mid}-{limit}"
    embed = discord.Embed(title=f"Commentary | {data[1]}", color=hex2discolor(None))
    if data[0] == []:
        embed.add_field(name="Note:", value="No commentary available", inline=True)
        return embed
    for i in data[0]:
        embed.add_field(name=f"[{i[0]}] {i[1]}", value=i[2], inline=False)
    embed.set_footer(text=sessionid)
    return embed

def partnership_embed(data, sid, mid, inning_index):
    if data == None:
        embed = discord.Embed()
        embed.add_field(name="Note", value="Partnership data not avaliable as of now.", inline=False)
        return embed
    updateStatus = "NUA"
    if data[0][0] == "LIVE": updateStatus = "UA"
    sessionid = f"PSP-{updateStatus}-{sid}-{mid}-{inning_index}"
    embed = discord.Embed(title=f"Partnership | {data[0][0]}", color=hex2discolor(data[0][2]))
    embed.set_author(name=data[0][1], icon_url=data[0][3])
    embed.set_thumbnail(url=data[0][3])
    for j, i in enumerate(data[1]):
        embed.add_field(name=f"{str(j+1)}. {i[2]} x {i[5]} ({i[0]} in {i[1]} ov.)",
            value=f"*{i[2]}: {i[3]} in {i[4]} balls*\n*{i[5]}: {i[6]} in {i[7]} balls*",
            inline=False)
    embed.set_footer(text=sessionid, icon_url=data[0][3])
    return embed

def partnershipGraph_embed(data, sid, mid, inning_index):
    if data == None:
        embed = discord.Embed()
        embed.add_field(name="Note", value="**Partnership** data not avaliable as of now.", inline=False)
        return embed, None
    updateStatus = "NUA"
    if data[1] == "LIVE": updateStatus = "UA"
    sessionid = f"PSPG-{updateStatus}-{sid}-{mid}-{inning_index}"
    embed = discord.Embed(title=f"Partnership Graph | {data[1]}", color=hex2discolor(data[3]))
    embed.set_author(name=data[2], icon_url=data[4])
    embed.set_thumbnail(url=data[4])
    file = discord.File(fp=data[0], filename=f"{sid}{mid}.png")
    embed.set_image(url=f"attachment://{sid}{mid}.png")
    embed.set_footer(text=sessionid, icon_url=data[4])
    return embed, file

def fallofwicketsGraph_embed(data, sid, mid, inning_index):
    if data == None:
        embed = discord.Embed()
        embed.add_field(name="Note", value="**Fall of wickets** data not avaliable as of now.", inline=False)
        return embed, None
    updateStatus = "NUA"
    if data[1] == "LIVE": updateStatus = "UA"
    sessionid = f"FOW-{updateStatus}-{sid}-{mid}-{inning_index}"
    embed = discord.Embed(title=f"Fall of wicket Graph | {data[1]}", color=hex2discolor(data[3]))
    embed.set_author(name=data[2], icon_url=data[4])
    embed.set_thumbnail(url=data[4])
    file = discord.File(fp=data[0], filename=f"{sid}{mid}.png")
    embed.set_image(url=f"attachment://{sid}{mid}.png")
    embed.set_footer(text=sessionid, icon_url=data[4])
    return embed, file

def bestbatsmen_embed(data):
    embed = discord.Embed(title=f"Best Batsman of the Inning", color=hex2discolor(data[2]))
    embed.set_author(name=data[1], icon_url=data[0][0][1])
    embed.set_thumbnail(url=data[3])
    for i in data[0]:
        embed.add_field(name=i[0], 
        value=f"*Matches*: {i[2]} | *Runs*: {i[3]} | *Innings*: {i[4]}\n\
        *Average*: {i[5]} | *NotOuts*: {i[6]} | *Strikerate*: {i[7]}", inline=False)
    embed.set_footer(text=".", icon_url=data[0][-1][1])
    return embed

def bestbowlers_embed(data):
    embed = discord.Embed(title=f"Best Bowler of the Inning", color=hex2discolor(data[2]))
    embed.set_author(name=data[1], icon_url=data[0][0][1])
    embed.set_thumbnail(url=data[3])
    for i in data[0]:
        embed.add_field(name=i[0], 
        value=f"*Matches*: {i[2]} | *Wickets*: {i[3]} | *Innings*: {i[4]}\n\
        *Average*: {i[5]} | *Conceded*: {i[6]} | *Economy*: {i[7]}\n*Balls*:{i[8]}", inline=False)
    embed.set_footer(text=".", icon_url=data[0][-1][1])
    return embed

def getinning_embed(sessionid):
    embed = discord.Embed(title=f"Select the inning")
    embed.set_footer(text=sessionid)
    return embed

def format_embed(rntype):
    name = "Select format:"
    formats = ["test", "odi", "t20i"]
    sessionid = f"FMTR-{rntype}-0"
    value = ""
    for i, j in enumerate(formats): value+=f"{i+1}. {j.upper()}\n"
    embed = discord.Embed()
    embed.add_field(name=name, value=value, inline=False)
    embed.set_footer(text=sessionid)
    return embed

def role_embed(format_index, rntype):
    name = "Select role:"
    roles = ["bowl", "bat", "allround"]
    sessionid = f"FMTR-{rntype}-1-{format_index}"
    value = ""
    for i, j in enumerate(roles):
        value += f"{i+1}. {j.upper()}\n"
    embed = discord.Embed()
    embed.add_field(name=name, value=value, inline=False)
    embed.set_footer(text=sessionid)
    return embed

def getrankingchoice_embed(data, limit):
    sessionid = f"RNKL-{limit}"
    embed = discord.Embed(title="Rankings", color=0x03f8fc)
    name = f"Select series to get ranking"
    value = "```py\n"
    sid_container = []
    for i, j in enumerate(data[:limit][-5:]):
        sid_container.append(j[0])
        value += f"{i+1}. {j[1]}\n"
    value += "\n```"
    embed.add_field(name=name, value=value, inline=False)
    embed.set_footer(text=sessionid)
    return embed, sid_container

def gettranking_embed(data):
    embed = discord.Embed(title=f"{data[0]} | {data[1]}", color=0x03f8fc)
    
    name = f'```RANK　TEAM　MATCH　WON　LOST　DRAW　POINT　　NRR```'
    
    value = "```py\n"
    for i in data[2:][0]:
        value += f'{i[3]:02}　{string_validator(i[0], 3)}　{i[4]:01}　　{i[5]:02}　　{i[6]:02}　　{i[7]:02} 　{i[8]:02}　{i[9]:04}\n'
    value += "```"
    embed.add_field(name=name,value=value, inline=False)
    return embed
