from typing import get_args
import requests, json

BASE_URL = "https://hs-consumer-api.espncricinfo.com"
HEAD_URL = BASE_URL + "/v1/pages/matches/"

class URLS():
    lang="?lang=en"
    matches = ["scheduled", "live", "result"]
    home = "/home"
    scorecard = "/scorecard"
    statistics="/statistics"
    team_players= "/team-players"
    sid = "&seriesId="
    mid = "&matchId="
    imgProvSv = "https://p.imgci.com"

def get_schedules(type_index:int, limit:int):
    url=HEAD_URL + URLS.matches[type_index] + URLS.lang
    response = requests.get(url).json()
    matches = response["content"]["matches"][:limit]
    container = []
    for match in matches:
        mid = match["id"]
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
        sid = series["id"]
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
    mid = match["id"]
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
    sid = series["id"]
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
                    
