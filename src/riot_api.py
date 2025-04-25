import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")
HEADERS = {"X-Riot-Token": API_KEY}

if not API_KEY:
    raise EnvironmentError("Please set the RIOT_API_KEY environment variable.")

def riot_get(url: str) -> dict:
    """Make a GET request to Riot API with rate limit handling."""
    while True:
        res = requests.get(url, headers=HEADERS)

        if res.status_code == 200:
            return res.json()
        elif res.status_code == 429:
            retry_after = int(res.headers.get("Retry-After", 1))
            print(f"Rate limited. Retrying after {retry_after} seconds...")
            time.sleep(retry_after + 1)
            continue
        else:
            raise Exception(f"API Error: {res.status_code} - {res.text}")

# Account-V1
def get_summoner_puuid(gameName: str, tagLine: str, region="americas") -> str:
    """Get the PUUID of a summoner by their Riot ID."""
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    data = riot_get(url)
    return data["puuid"]

# Summoner-V4
def summoner_from_puuid(puuid: str, region="na1") -> str:
    """Get the summoner ID (accountId) from a PUUID."""
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    data = riot_get(url)
    return data["accountId"]

def get_player_rank(summoner_id: str, region="na1") -> dict:
    """Get the rank of a summoner by their summoner ID."""
    url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    data = riot_get(url)
    if not data:
        return "UNRANKED"
    for entry in data:
        if entry["queueType"] == "RANKED_SOLO_5x5":
            return entry["tier"], entry["rank"]
    return "UNRANKED"

# Match-V5
def get_match_history(puuid: str, region="americas", total_matches=100) -> list:
    """Get up to total_matches match IDs for a summoner by their PUUID."""
    all_match_ids = []
    start = 0
    batch_size = 100  # Riot max batch size

    while len(all_match_ids) < total_matches:
        count = min(batch_size, total_matches - len(all_match_ids))
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
        match_ids = riot_get(url)

        if not match_ids:
            # No more matches available
            break

        all_match_ids.extend(match_ids)
        start += count

    return all_match_ids


def get_match_data(match_id: str, region="americas") -> dict:
    """Get the match details by match ID."""
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    data = riot_get(url)
    return data
