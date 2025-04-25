from src.riot_api import get_summoner_puuid, summoner_from_puuid, get_match_history

gameName = "Chen"
tagLine = "44444"

try:
    puuid = get_summoner_puuid(gameName, tagLine)
    print(f"PUUID for {gameName}#{tagLine}: {puuid}")
    summoner_id = summoner_from_puuid(puuid)
    print(f"Summoner ID for PUUID {puuid}: {summoner_id}")
    matches = get_match_history(puuid, count=5)
    print(f"Match history for {gameName}#{tagLine}: {matches}")
except Exception as e:
    print("Error:", e)