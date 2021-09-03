import requests, json

BASE_URL = "https://hs-consumer-api.espncricinfo.com"
HEAD_URL = BASE_URL + "/v1/pages/matches/"

class URLS():
    lang="?lang=en"
    matches = ["scheduled", "live", "result"]
    home = "home"
    scorecard = "scorecard"
    statistics="statistics"
    team_players= "team-players"
    sid = "&seriesId="
    mid = "&matchId="

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

