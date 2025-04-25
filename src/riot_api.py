import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")
HEADERS = {
    "X-Riot-Token": API_KEY}
if not API_KEY:
    raise EnvironmentError("Please set the RIOT_API_KEY environment variable.")

# Account-V1
def get_summoner_puuid(gameName: str, tagLine: str, region="americas") -> str:
    "Get the PUUID of a summoner by their Riot ID."
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()["puuid"]
    else:
        raise Exception(f"Error fetching summoner data: {res.status_code} - {res.text}")

# Summoner-V4
def summoner_from_puuid(puuid: str, region="na1") -> dict:
    "Get the summoner ID from a PUUID."
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()["accountId"]
    else:
        raise Exception(f"Error fetching summoner data: {res.status_code} - {res.text}")

# Match-V5
def get_match_history(puuid: str, region="americas", count=10) -> list:
    "Get the match history of a summoner by their PUUID."
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception(f"Error fetching match history: {res.status_code} - {res.text}")

def get_match_details(match_id: str, region="americas") -> dict:
    "Get the match details by match ID."
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception(f"Error fetching match details: {res.status_code} - {res.text}")