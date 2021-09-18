from cricbotlib2 import cricbotlib2 as cb2
from embedder import embedder

def refresher(args):
    sid, mid = int(args[2]), int(args[3])
    if args[0] == "SC":
        colorindex = int(args[4])
        data = cb2.get_score(sid, mid)
        if colorindex == 2: colorindex=1
        else:colorindex=2
        embed = embedder.score_embed(data, mid, sid, colorindex)

    if args[0] == "SCRD":
        inning_index = int(args[4])
        data = cb2.get_scorecard(sid, mid, inning_index)
        embed = embedder.scorecard_embed(data, sid, mid, inning_index)

    if args[0] == "CMTRY":
        limit = int(args[4])
        data = cb2.get_comments(sid, mid, limit)
        embed = embedder.comments_embed(data, sid, mid, limit)

    if args[0] == "PSP":
        inning_index = int(args[4])
        data = cb2.get_partnership(sid, mid, inning_index)
        embed = embedder.partnership_embed(data, sid, mid, inning_index)

    if args[0] == "PSPG":
        inning_index = int(args[4])
        data = cb2.get_partnershipGraph(sid, mid, inning_index)
        embed = embedder.partnershipGraph_embed(data, sid, mid, inning_index)

    if args[0] == "FOW":
        inning_index = int(args[4])
        data = cb2.get_fallofwicketsGraph(sid, mid, inning_index)
        embed = embedder.fallofwicketsGraph_embed(data, sid, mid, inning_index)

    return embed

def on_schedule_select(args:list, sid, mid):
    if args[0] == "SC":
        colorindex = 1
        data = cb2.get_score(sid, mid)
        embed = embedder.score_embed(data, mid, sid, colorindex)

    if args[0] == "SCRD":
        sessionid = f"INN-SCRD-{sid}-{mid}"
        embed = embedder.getinning_embed(sessionid)

    if args[0] == "CMTRY":
        limit = 5
        data = cb2.get_comments(sid, mid, limit)
        embed = embedder.comments_embed(data, sid, mid, limit)

    if args[0] == "PSP":
        sessionid = f"INN-PSP-{sid}-{mid}"
        embed = embedder.getinning_embed(sessionid)

    if args[0] == "PSPG":
        sessionid = f"INN-PSPG-{sid}-{mid}"
        embed = embedder.getinning_embed(sessionid)

    if args[0] == "FOW":
        sessionid = f"INN-FOW-{sid}-{mid}"
        embed = embedder.getinning_embed(sessionid)

    if args[0] == "BBT":
        sessionid = f"INN-BBT-{sid}-{mid}"
        embed = embedder.getinning_embed(sessionid)

    if args[0] == "BBL":
        sessionid = f"INN-BBL-{sid}-{mid}"
        embed = embedder.getinning_embed(sessionid)

    return embed

def on_inning_select(args:list, sid, mid, inning_index):

    if args[0] == "SCRD":
        data = cb2.get_scorecard(sid, mid, inning_index)
        embed = embedder.scorecard_embed(data, sid, mid, inning_index)

    if args[0] == "PSP":
        data = cb2.get_partnership(sid, mid, inning_index)
        embed = embedder.partnership_embed(data, sid, mid, inning_index)

    if args[0] == "PSPG":
        inning_index = int(args[4])
        data = cb2.get_partnershipGraph(sid, mid, inning_index)
        embed = embedder.partnershipGraph_embed(data, sid, mid, inning_index)

    if args[0] == "FOW":
        data = cb2.get_fallofwicketsGraph(sid, mid, inning_index)
        embed = embedder.fallofwicketsGraph_embed(data, sid, mid, inning_index)

    if args[0] == "BBT":
        data = cb2.get_bestbatsmen(sid, mid, inning_index-1)
        embed = embedder.bestbatsmen_embed(data)

    if args[0] == "BBL":
        data = cb2.get_bestbowlers(sid, mid, inning_index-1)
        embed = embedder.bestbowlers_embed(data)
    
    return embed

