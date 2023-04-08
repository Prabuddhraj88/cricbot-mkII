import requests, io, base64
import matplotlib.pyplot as mp
import numpy as np

BASE_URL = base64.b64decode("aHR0cHM6Ly9ocy1jb25zdW1lci1hcGkuZXNwbmNyaWNpbmZvLmNvbQ==").decode("utf-8")
HEAD_URL = BASE_URL + "/v1/pages/matches/"

class URLS:
    lang="?lang=en"
    matches = ["scheduled", "live", "result"]
    home = "/home"
    scorecard = "/scorecard"
    statistics="/statistics"
    team_players= "/team-players"
    commentary= "/commentary"
    sid = "&seriesId="
    mid = "&matchId="
    imgProvSv = base64.b64decode("aHR0cHM6Ly9wLmltZ2NpLmNvbQ==").decode("utf-8")

def get_schedules(type_index:int, limit:int, searchby=None):
    url=HEAD_URL + URLS.matches[type_index] + URLS.lang
    response = requests.get(url).json()
    matches = response["content"]["matches"][:limit]
    container, idcontainer = [], []
    for match in matches:
        mid = match["objectId"]
        state = match["state"]
        datentime = match["startTime"].replace('T', ' ').replace('.000Z', '')
        title = match["title"]
        se=match["statusEng"]
        if match["statusText"] != None:
            if se == "{{MATCH_START_TIME}}":
                se = datentime
            status = se + ": " + match["statusText"]
        else: status = match["statusEng"]
        series = match["series"]
        sid = series["objectId"]
        series_name = series["longName"]
        if match["ground"] != None:
            ground = match["ground"]["name"]
        else: ground = "Not Available"
        teams = match["teams"]
        versus = ""
        for team in teams:
            versus += team["team"]["name"] + " vs "
        versus = versus[:-3]
        total_innings = match["liveInning"]
        idcontainer.append((sid, mid, total_innings))
        container.append((series_name, versus, ground, datentime, title, state, status))
    if searchby != None:
        xcontainer, xidcontainer = [], []
        for i in container:
            if searchby in i[0]:
                idx = container.index(i)
                xcontainer.append(container[idx])
                xidcontainer.append(idcontainer[idx])
        return xcontainer[-5:], xidcontainer[-5:]
    if container == []: return None
    return container[-5:], idcontainer[-5:]

def get_player(sid:int, mid:int, player_index:int, team_index:int):
    url = HEAD_URL[:-3] + URLS.home + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    team = response["content"]["matchPlayers"]["teamPlayers"][team_index]
    player = team["players"][player_index]
    team = team["team"]
    roles = {
        "P": "Player",
        "WK": "Wicket Keeper",
        "C": "Captain",
        "VC": "Vice Captain"        
    }
    role = roles[player["playerRoleType"]]
    team_name = team["longName"]
    team_color = team["primaryColor"]
    team_logo = URLS.imgProvSv + team["image"]["url"]
    player = player["player"]
    player_name = player["longName"]
    player_gender = player["gender"]
    player_playingRole = player["playingRole"]
    try:player_battingStyle = player["longBattingStyles"][0]
    except IndexError: player_battingStyle = "Not Available"
    try:player_bowlingStyles= player["longBowlingStyles"][0]
    except IndexError: player_bowlingStyles = "Not Available"
    player_image = URLS.imgProvSv + player["image"]["url"]
    return role, team_name, team_color, team_logo, player_name, player_gender, player_playingRole,\
    player_battingStyle, player_bowlingStyles, player_image

def get_score(sid:int, mid:int):
    url = HEAD_URL[:-3] + URLS.home + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    match = response["match"]
    state = match["state"]
    datentime = match["startTime"].replace('T', ' ').replace('.000Z', '')
    title = match["title"]
    se=match["statusEng"]
    if match["statusText"] != None:
        if se == "{{MATCH_START_TIME}}":
            se = datentime
        status = se + ": " + match["statusText"]
    else: status = match["statusEng"]
    series = match["series"]
    series_name = series["longName"]
    if match["ground"] != None:
        ground = match["ground"]["name"]
    else: ground = "Not Available"
    teams = match["teams"]
    versus, score = "", ""
    team_colors, team_logos = [], []
    for team in teams:
        a=""
        versus += team["team"]["name"] + " vs "
        if team["isLive"]:a="*"
        if team["score"] != None: 
            score += f"***{team['team']['name']}:***\n{team['score']}{a}"
        if team["scoreInfo"] != None:
            score += " (" + team["scoreInfo"] + ")"
        score += "\n"
        team_colors.append(team["team"]["primaryColor"])
        team_logos.append(URLS.imgProvSv + team["team"]["image"]["url"])
    versus = versus[:-2]
    strikers, bowlerssr = None, None
    livePerformance = response["content"]["livePerformance"]
    if livePerformance is not None:
        batsmen = livePerformance["batsmen"]
        bowlers = livePerformance["bowlers"]
        strikers, bowlerssr = "", ""
        for batsman in batsmen:
            strikers += batsman["player"]["longName"] + "- " + str(batsman["runs"]) + \
                " in " + str(batsman["balls"]) + " (S.R- " + str(batsman["strikerate"]) + ")\n"
        for bowler in bowlers:
            bowlerssr += bowler["player"]["longName"] + "- " + str(bowler["conceded"]) + "-" + str(bowler["wickets"]) +\
                " in " + str(bowler["overs"]) + " overs (E.R- " + str(bowler["economy"]) + ")\n"
    return series_name, versus, ground, datentime, title, state, status, score, strikers, bowlerssr, team_colors, team_logos

def get_scorecard(sid:int, mid:int, inning_index:int):
    batcontainer = []
    bowlcontainer = []
    url = HEAD_URL[:-3] + URLS.scorecard + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    state = response["match"]["state"]
    scorecard = response["content"]["scorecard"]
    inning = scorecard["innings"][inning_index]
    team_name = inning["team"]["longName"]
    team_color = inning["team"]["primaryColor"]
    team_logo = URLS.imgProvSv + inning["team"]["image"]["url"]
    if inning["isBatted"]:
        runs = inning["runs"]
        wickets = inning["wickets"]
        overs = inning["overs"]
        teamdet = [team_name, team_color, team_logo, runs, wickets, overs, state]
        inningBatsmen = inning["inningBatsmen"]
        inningBowlers = inning["inningBowlers"]
        for batsman in inningBatsmen:
            if batsman["battedType"] == "yes":
                stts = ""
                if not batsman["isOut"]: stts = "*"
                outinfo = "-"
                if batsman["isOut"]:
                    outinfo = batsman["dismissalText"]["long"]
                batcontainer.append((stts + batsman["player"]["fieldingName"], batsman["runs"], batsman["balls"],
                                    batsman["fours"], batsman["sixes"], batsman["strikerate"], outinfo))
        for bowler in inningBowlers:
            bowlcontainer.append((bowler["player"]["fieldingName"], bowler["conceded"], bowler["overs"], bowler["wickets"], bowler["maidens"], bowler["economy"]))
        return teamdet, batcontainer, bowlcontainer

def get_comments(sid: int, mid: int, limit:int):
    container = []
    url = HEAD_URL[:-3] + URLS.commentary + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    comments = response["content"]["comments"][:limit]
    state = response["match"]["state"]
    for comment in comments:
        try:
            time = "00.00.00 00:00"
            if comment["timestamp"] != None:
                time = comment["timestamp"].split('.')[0].replace('T', ' ')
            title = comment["title"]
            if comment["commentTextItems"] != None:
                description = comment["commentTextItems"][0]["html"]
            else: description = "Not available"
        except IndexError:pass
        container.append((time, title, description))
    return (container[-5:])[::-1], state

def get_partnership(sid: int, mid: int, inning_index:int):
    container, subcontainer = [], []
    url = HEAD_URL[:-3] + URLS.statistics + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    try:inning = response["content"]["innings"][inning_index]
    except IndexError: return None
    team_name = inning["team"]["name"]
    team_color = inning["team"]["primaryColor"]
    team_logo = URLS.imgProvSv + inning["team"]["image"]["url"]
    state = response["match"]["state"]
    container.append((state, team_name, team_color, team_logo))
    for partnership in inning["inningPartnerships"]:
        subcontainer.append([partnership["runs"], partnership["overs"], partnership["player1"]["longName"],
        partnership["player1Runs"], partnership["player1Balls"],partnership["player2"]["longName"],
        partnership["player2Runs"], partnership["player2Balls"]])
    container.append(subcontainer)
    return container 

def get_partnershipGraph(sid: int, mid: int, inning_index:int):
    url = HEAD_URL[:-3] + URLS.statistics + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    print(url)
    response = requests.get(url).json()
    try:inning = response["content"]["innings"][inning_index]
    except IndexError: return None
    state = response["match"]["state"]
    team_name = inning["team"]["name"]
    team_color = inning["team"]["primaryColor"]
    team_logo = URLS.imgProvSv + inning["team"]["image"]["url"]
    partnerships = inning["inningPartnerships"]
    x, runs, balls = [], [], []
    for partnership in partnerships:
        x.append(partnership["player1"]["fieldingName"]+"\n"+partnership["player2"]["fieldingName"])
        runs.append(partnership["runs"])
        balls.append(partnership["balls"])
    x_pos = [i for i, _ in enumerate(x)]
    mp.bar(x_pos, runs, color=team_color, width=0.7)
    mp.xlabel("Partners")
    mp.ylabel("Runs")
    mp.title("Partnerships: "+team_name)
    mp.xticks(x_pos, x, fontsize=7)
    r = sorted(runs)
    highest_score = int(r[len(runs)-1])
    mp.yticks(np.arange(0, highest_score+10, step=15))
    for i in range(len(runs)):
        mp.annotate(str(runs[i])+' in ' +
                    str(balls[i]), (x_pos[i]-0.3, runs[i]+1), fontsize=8)
    fig = mp.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    mp.cla()
    return buf, state, team_name, team_color, team_logo

def get_fallofwicketsGraph(sid: int, mid: int, inning_index:int):
    url = HEAD_URL[:-3] + URLS.statistics + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    try:inning = response["content"]["innings"][inning_index]
    except IndexError: return None
    state = response["match"]["state"]
    team_name = inning["team"]["name"]
    team_color = inning["team"]["primaryColor"]
    team_logo = URLS.imgProvSv + inning["team"]["image"]["url"]
    inningWickets = inning["inningWickets"]
    x, o, s = [], [], []
    for wicket in inningWickets:
        x.append(wicket["player"]["fieldingName"])
        o.append(float(wicket['fowOvers']))
        s.append(int(wicket['fowRuns']))
    mp.xticks(np.arange(0, int(o[len(o)-1]+100), step=5))
    mp.yticks(np.arange(0, int(s[len(s)-1]+100), step=15))
    mp.title('Fall of wicket: '+team_name, fontsize=14)
    mp.xlabel('Overs', fontsize=14)
    mp.ylabel('Runs', fontsize=14)
    mp.plot(o, s, color='red', marker='o', linewidth=3,
            markerfacecolor='red', markersize=8, label='Wickets')
    for i in range(len(o)):
        mp.annotate(x[i] + '\n('+str(s[i])+'-'+str(o[i])+')',
                    (o[i]+2, s[i]-2), fontsize=7)
    mp.plot(o, s, color=team_color, label='Runs')
    mp.legend(loc='lower right')
    fig = mp.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    mp.cla()
    return buf, state, team_name, team_color, team_logo

def get_bestbatsmen(sid: int, mid: int, inning_index:int):
    container = []
    url = HEAD_URL[:-3] + URLS.team_players + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    players = response["content"]["matchPlayers"]["teamPlayers"][inning_index]
    team_name = players["team"]["name"]
    team_color = players["team"]["primaryColor"]
    team_logo = URLS.imgProvSv + players["team"]["image"]["url"]
    for player in players["bestBatsmen"]:
        name = player["player"]["longName"]
        image = URLS.imgProvSv + player["player"]["image"]["url"]
        matches = player["matches"]
        runs = player["runs"]
        innings = player["innings"]
        average = player["average"]
        notouts = player["notouts"]
        strikerate = player["strikerate"]
        container.append((name, image, matches, runs, innings, average, notouts, strikerate))
    return container, team_name, team_color, team_logo

def get_bestbowlers(sid: int, mid: int, inning_index:int):
    container = []
    url = HEAD_URL[:-3] + URLS.team_players + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    players = response["content"]["matchPlayers"]["teamPlayers"][inning_index]
    team_name = players["team"]["name"]
    team_color = players["team"]["primaryColor"]
    team_logo = URLS.imgProvSv + players["team"]["image"]["url"]
    for player in players["bestBowlers"]:
        name = player["player"]["longName"]
        image = URLS.imgProvSv + player["player"]["image"]["url"]
        matches = player["matches"]
        wickets = player["wickets"]
        innings = player["innings"]
        average = player["average"]
        runs = player["conceded"]
        economy = player["economy"]
        balls = player["balls"]
        container.append((name, image, matches, wickets, innings, average, runs, economy, balls))
    return container, team_name, team_color, team_logo

def get_activity(sid:int, mid:int):
    url = HEAD_URL[:-3] + URLS.home + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    match = response["match"]
    teams = match["teams"]
    string = teams[0]['team']['abbreviation'][:3] + " v " + teams[1]['team']['abbreviation'][:3] + " | "
    team = teams[-1]
    if team["score"] != None: 
        string += team['score']
    if team["scoreInfo"] != None:
        string += "(" + team["scoreInfo"] + ")"
    return string

def get_series4rankings():
    container = []
    url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/series/standings?lang=en&seriesId=1022345"
    response = requests.get(url).json()
    seriesGroups = response["content"]["standingSeriesGroups"]["seriesGroups"]
    for i in seriesGroups:
        sid = i["series"]["objectId"]
        name = i["series"]["longName"]
        container.append((sid, name))
    return container

def get_team_rankings(sid:int):
    container = []
    url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/series/standings?lang=en&seriesId={sid}"
    response = requests.get(url).json()
    standings = response["content"]["standings"]
    series = standings["series"]
    teamStats = standings["groups"][0]["teamStats"]
    container.append(series["longName"])
    container.append(series["year"])
    team_container = []
    for i in teamStats:
        name = i["teamInfo"]["longName"]
        image = i["teamInfo"]["imageUrl"]
        color = i["teamInfo"]["primaryColor"]
        rank = i["rank"]
        played = i["matchesPlayed"]
        won = i["matchesWon"]
        lost = i["matchesLost"]
        draw = i["matchesDrawn"]
        points = i["points"]
        nrr = i["nrr"]
        team_container.append((
            name, image, color, rank, played,
            won, lost, draw, points, nrr
        ))
    container.append(team_container)
    return container
