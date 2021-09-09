import requests, io
import matplotlib.pyplot as mp
import numpy as np

BASE_URL = "https://hs-consumer-api.espncricinfo.com"
HEAD_URL = BASE_URL + "/v1/pages/matches/"

class URLS():
    lang="?lang=en"
    matches = ["scheduled", "live", "result"]
    home = "/home"
    scorecard = "/scorecard"
    statistics="/statistics"
    team_players= "/team-players"
    commentary= "/commentary"
    sid = "&seriesId="
    mid = "&matchId="
    imgProvSv = "https://p.imgci.com"

def get_schedules(type_index:int, limit:int):
    url=HEAD_URL + URLS.matches[type_index] + URLS.lang
    response = requests.get(url).json()
    matches = response["content"]["matches"][:limit]
    container = []
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
            versus += team["team"]["slug"] + " v "
        versus = versus[:-2]
        container.append((mid, sid, series_name, versus, ground, datentime, title, state, status))
    return container[-5:]


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
    versus, score = "", ""
    for team in teams:
        versus += team["team"]["slug"] + " v "
        score += team["score"] 
        if team["scoreInfo"] != None:
            score += " (" + team["scoreInfo"] + ")"
        score += "\n"
    versus = versus[:-2]
    livePerformance = response["content"]["livePerformance"]
    batsmen = livePerformance["batsmen"]
    bowlers = livePerformance["bowlers"]
    strikers = ""
    bowlerssr = ""
    for batsman in batsmen:
        strikers += batsman["player"]["longName"] + "- " + str(batsman["runs"]) + \
            " in " + str(batsman["balls"]) + " (S.R- " + str(batsman["strikerate"]) + ")\n"
    for bowler in bowlers:
        bowlerssr += bowler["player"]["longName"] + "- " + str(bowler["conceded"]) + "-" + str(bowler["wickets"]) +\
            " in " + str(bowler["overs"]) + " overs (E.R- " + str(bowler["economy"]) + ")\n"
    return mid, sid, series_name, versus, ground, datentime, title, state, status, score, strikers, bowlerssr


def get_scorecard(sid:int, mid:int, inning_index:int):
    batcontainer = []
    bowlcontainer = []
    url = HEAD_URL[:-3] + URLS.scorecard + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    scorecard = response["content"]["scorecard"]
    inning = scorecard["innings"][inning_index]
    innNum = inning["inningNumber"]
    team_name = inning["team"]["longName"]
    team_color = inning["team"]["primaryColor"]
    team_logo = URLS.imgProvSv + inning["team"]["image"]["url"]
    if inning["isBatted"]:
        runs = inning["runs"]
        wickets = inning["wickets"]
        overs = inning["overs"]
        teamdet = [innNum, team_name, team_color, team_logo, runs, wickets, overs]
        inningBatsmen = inning["inningBatsmen"]
        inningBowlers = inning["inningBowlers"]
        for batsman in inningBatsmen:
            if batsman["battedType"] == "yes":
                outinfo = "-"
                if batsman["isOut"]:
                    outinfo = batsman["dismissalText"]["long"]
                batcontainer.append((batsman["player"]["name"], batsman["runs"], batsman["balls"], batsman["fours"], batsman["sixes"], batsman["strikerate"], outinfo))
        for bowler in inningBowlers:
            bowlcontainer.append((bowler["player"]["name"], bowler["conceded"], bowler["overs"], bowler["wickets"], bowler["dots"],
                             bowler["fours"], bowler["sixes"], bowler["wides"], bowler["noballs"], bowler["maidens"], bowler["economy"]))
        return teamdet, batcontainer, bowlcontainer


def get_comments(sid: int, mid: int, limit:int):
    container = []
    url = HEAD_URL[:-3] + URLS.commentary + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    comments = response["content"]["comments"]
    for comment in comments:
        try:
            cid = comment["id"]
            time = comment["timestamp"]
            title = comment["title"]
            if comment["commentTextItems"] != None:
                description = comment["commentTextItems"][0]["html"]
            else: description = "Not available"
        except IndexError:pass
        container.append((cid, time, title, description))
    return (container[:-limit])[::-1]

def get_statistics(sid: int, mid: int, limit:int):
    url = HEAD_URL[:-3] + URLS.statistics + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).content
    return response.decode('utf-8')

def get_partnership(sid: int, mid: int, inning_index:int, partnership_index:int):
    url = HEAD_URL[:-3] + URLS.statistics + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    inning = response["content"]["inningsPerformance"]["innings"][inning_index]
    team_name = inning["team"]["name"]
    team_color = inning["team"]["primaryColor"]
    partnership = inning["inningPartnerships"][partnership_index]

    return team_name, team_color, partnership["runs"], partnership["overs"], (partnership["player1"]["longName"],
        partnership["player1Runs"], partnership["player1Balls"]),(partnership["player2"]["longName"],
        partnership["player2Runs"], partnership["player2Balls"])

def get_partnershipGraph(sid: int, mid: int, inning_index:int):
    url = HEAD_URL[:-3] + URLS.statistics + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    inning = response["content"]["inningsPerformance"]["innings"][inning_index]
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
    return buf, team_name, team_color, team_logo

def get_fallofwicketGraph(sid: int, mid: int, inning_index:int):
    url = HEAD_URL[:-3] + URLS.statistics + URLS.lang + URLS.sid + str(sid) + URLS.mid + str(mid)
    response = requests.get(url).json()
    inningWickets = response["content"]["inningsPerformance"]["innings"][inning_index]["inningWickets"]
    team = response["content"]["inningsPerformance"]["innings"][inning_index]["team"]
    team_name = team["longName"]
    team_color = team["primaryColor"]
    team_logo = URLS.imgProvSv + team["image"]["url"]
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
                    (o[i]+0.1, s[i]-2), fontsize=7)
    mp.plot(o, s, color=team_color, label='Runs')
    mp.legend(loc='lower right')
    fig = mp.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    mp.cla()
    return buf, team_name, team_color, team_logo
