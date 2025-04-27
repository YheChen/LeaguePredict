import pandas as pd
from src.riot_api import get_match_data, get_match_history
from collections import Counter

def extract_team_stats_and_champions(match_data: dict) -> dict:
    "Extracts team stats and champions from match data."
    info = match_data["info"]
    participants = info["participants"]

    team1 = [p for p in participants if p["teamId"] == 100]
    team2 = [p for p in participants if p["teamId"] == 200]

    team1_kills = sum(p["kills"] for p in team1)
    team1_deaths = sum(p["deaths"] for p in team1)
    team1_assists = sum(p["assists"] for p in team1)
    team1_champions = [p["championId"] for p in team1]

    team2_kills = sum(p["kills"] for p in team2)
    team2_deaths = sum(p["deaths"] for p in team2)
    team2_assists = sum(p["assists"] for p in team2)
    team2_champions = [p["championId"] for p in team2]

    features = {}

    for champ_id in team1_champions:
        features[f"team1_champ_{champ_id}"] = 1

    for champ_id in team2_champions:
        features[f"team2_champ_{champ_id}"] = 1

    features.update({
        "team1_kills": team1_kills,
        "team1_deaths": team1_deaths,
        "team1_assists": team1_assists,
        "team2_kills": team2_kills,
        "team2_deaths": team2_deaths,
        "team2_assists": team2_assists,
    })

    team1_win = team1[0]["win"]
    features["winner"] = 1 if team1_win else 0

    return features

def build_dataset_from_match_ids(match_ids: list, save_path="data/raw_matches.csv") -> None:
    "Builds a dataset from a list of match IDs and saves it to a CSV."
    all_features = []

    for match_id in match_ids:
        try:
            match_data = get_match_data(match_id)
            features = extract_team_stats_and_champions(match_data)
            all_features.append(features)
        except Exception as e:
            print(f"Skipping match {match_id} due to error: {e}")
            continue

    df = pd.DataFrame(all_features)
    df = df.fillna(0)  # fill missing champion columns with 0
    df.to_csv(save_path, index=False)
    print(f"Saved {len(df)} matches to {save_path}")

def get_player_winrate(puuid: str, num_matches=20) -> float:
    "Compute the winrate of a player based on their last num_matches."
    match_ids = get_match_history(puuid, total_matches=num_matches)

    if not match_ids:
        return 0.5  # No matches found, return neutral winrate
    
    wins = 0
    for match_id in match_ids:
        match_data = get_match_data(match_id)
        for p in match_data["info"]["participants"]:
            if p["puuid"] == puuid:
                if p["win"]:
                    wins += 1
                break

    return wins / len(match_ids)

def get_player_preferred_role(puuid: str, num_matches=30) -> str:
    "Compute the preferred role of a player based on their last num_matches."
    match_ids = get_match_history(puuid, total_matches=num_matches)

    if not match_ids:
        return "UNKNOWN"  # No matches found, return unknown role

    role_counter = Counter()

    for match_id in match_ids:
        try:
            match_data = get_match_data(match_id)
            for participant in match_data["info"]["participants"]:
                if participant["puuid"] == puuid:
                    position = participant.get("teamPosition", "UNKNOWN")
                    if position != "NONE" and position != "":
                        role_counter[position] += 1
                    break  # Found our player, stop looping
        except Exception as e:
            print(f"Error processing match {match_id}: {e}")
            continue

    if not role_counter:
        return "UNKNOWN"

    # Return the most common role
    return role_counter.most_common(1)[0][0]

def get_player_champion_winrate(puuid: str, champion_id, num_matches=30) -> float:
    "Compute the winrate of a player's champion based on their last num_matches."
    match_ids = get_match_history(puuid, total_matches=num_matches)

    if not match_ids:
        return 0.5  # No matches found, return neutral winrate
    
    champ_matches = 0
    champ_wins = 0

    for match_id in match_ids:
        try:
            match_data = get_match_data(match_id)
            for participant in match_data["info"]["participants"]:
                if participant["puuid"] == puuid:
                    if participant["championId"] == champion_id:
                        champ_matches += 1
                        if participant["win"]:
                            champ_wins += 1
                    brea
        except Exception as e:
            print(f"Error processing match {match_id}: {e}")
            continue

    if champ_matches == 0:
        return 0.5  # If no recent games on that champ, assume neutral 50% winrate

    return champ_wins / champ_matches