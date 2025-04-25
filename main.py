from src.preprocess import build_dataset_from_match_ids
from src.riot_api import get_match_history, get_summoner_puuid, summoner_from_puuid

gameName = "C9 Loki"
tagLine = "kr3"

puuid = get_summoner_puuid(gameName, tagLine)
summoner_id = summoner_from_puuid(puuid)
matches = get_match_history(puuid, total_matches=1000)

build_dataset_from_match_ids(matches, save_path="data/raw_matches.csv")