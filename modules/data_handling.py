import os  # Provides functions to interact with the operating system
import json  # Handles JSON serialization and deserialization

# Path to the JSON file where the team data is stored
TEAM_FILE = "data/team.json"

# Function to load the team data from the JSON file
def load_Team():
    # Check if the team file exists at the specified path
    if os.path.exists(TEAM_FILE):
        # Open the file in read mode
        with open(TEAM_FILE, "r") as f:
            # Load and return the JSON data as a Python list/dictionary
            return json.load(f)
    # If the file does not exist, return an empty list (no team saved yet)
    return []

# Function to save the current team data to the JSON file
def save_Team(team):
    # Open the team file in write mode
    with open(TEAM_FILE, "w") as f:
        # Dump the team list/dictionary into the JSON file with indentation for readability
        json.dump(team, f, indent=2)

# Function to retrieve a Digimon's stats and types by name
def retrieve_Stats_By_Name(name, stats_dict):
    # Attempt to get the entry from stats_dict using the provided name
    entry = stats_dict.get(name)
    # If entry is not found, inform the user and return None values
    if not entry:
        print("Unable to locate the specified Digimon. Please provide a valid name.")
        return None, None, None
    # Confirm successful retrieval
    print(f"Successfully retrieved stats for {name}.")
    # Create a list of the stats for this Digimon, matching the model's expected order
    stats_list = [
        entry['HP lvl 50'],        # HP at level 50
        entry['SP lvl 50'],        # Special Points at level 50
        entry['ATK lvl 50'],       # Attack at level 50
        entry['DEF lvl 50'],       # Defense at level 50
        entry['INT lvl 50'],       # Intelligence/Special Attack at level 50
        entry['SPD lvl 50']        # Speed at level 50
    ]
    # Retrieve primary and secondary types, defaulting to empty string and converting to lowercase
    type1 = entry.get('type1', '').lower()
    type2 = entry.get('type2', '').lower()
    # Return the stats list and types
    return stats_list, type1, type2