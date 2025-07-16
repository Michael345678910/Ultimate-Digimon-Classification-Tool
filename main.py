# Import libraries needed to run the application.
import joblib  # Loads the trained machine learning model.
import pandas as pd  # Data handling.
import os  # File system checks.
import sys  # System exit and pip installation.
import random  # Utilized to suggest Digimon.
import json  # Used to save and load team data.

# This function prompts the user to input level 50 stats for a Digimon, re-prompting if the user inputs an invalid input or returning to main menu if '0' is entered.
# This function will be called later when the user inputs '1'.
def get_stats_level_50():
    while True:
        print(f"{Fore.LIGHTBLUE_EX}Enter stats of a level 50 Digimon (or 0 to return to the main menu):")
        try:
            hp = input("  HP: ").strip()
            if hp == '0':
                return None
            hp = int(hp)

            attack = input("  Attack: ").strip()
            if attack == '0':
                return None
            attack = int(attack)

            defense = input("  Defense: ").strip()
            if defense == '0':
                return None
            defense = int(defense)

            sp_attack = input("  Special Attack: ").strip()
            if sp_attack == '0':
                return None
            sp_attack = int(sp_attack)

            sp_defense = input("  Special Defense: ").strip()
            if sp_defense == '0':
                return None
            sp_defense = int(sp_defense)

            speed = input("  Speed: ").strip()
            if speed == '0':
                return None
            speed = int(speed)

            return [hp, attack, defense, sp_attack, sp_defense, speed]
        #Value error check, to ensure that the user is only entering an integer, otherwise show error message.
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Invalid input. Please try again utilizing integers only.")

# This code attempts to import colorama for adding color to terminal output; if unavailable, it installs colorama and then imports it.
# Colorama is used to add color to the terminal, which, in turn should make it a more user appealing experience.
try:
    from colorama import Fore, Style, init
except ImportError:
    print("Installing required package 'colorama'...")
    os.system(f"{sys.executable} -m pip install colorama")
    from colorama import Fore, Style, init

init(autoreset=True)  # Automatically resets colors to the normal white-text after each print, allowing for a detail focused command line application.

# Defines variables for file paths for dataset, trained model, and team data.
DATA_PATH = "data/Digimon.csv"
MODEL_PATH = "models/ultimate_Stage_Model.pkl"
TEAM_FILE = "data/team.json"

# Load and clean the dataset for use; set index for quick lookup and define column mappings.
try:
    df = pd.read_csv(DATA_PATH, sep=';')
    stats_dict = df.set_index('Digimon').to_dict(orient='index')
    name_col = 'Digimon'
    type1_col = 'Type'
    type2_col = 'Attribute'
    features = ['HP lvl 50', 'SP lvl 50', 'ATK lvl 50', 'DEF lvl 50', 'INT lvl 50', 'SPD lvl 50']

    # Create a label for the 'Ultimate' stage found from the Excel file.
    df['is_Ultimate'] = df['Stage'].apply(lambda s: 1 if isinstance(s, str) and s.strip().lower() == 'ultimate' else 0)
    target = 'is_Ultimate'
    df_clean = df[features + [target]].dropna()
except Exception as e:
    print(f"{Fore.LIGHTRED_EX}Error loading data: {e}")
    sys.exit(1)

# Creates a function to display the application start banner.
def application_Banner_Function():
    banner = f"""
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}
◇═══════════════════════════════════════════════════◇
▕       Ultimate Digimon Classification Tool        ▏
▕───────────────────────────────────────────────────▏
▕ Tip: Search by Digimon name, stat, or manage team ▏
◇═══════════════════════════════════════════════════◇
{Style.RESET_ALL}
"""
    print(banner)

# Function that suggests 5 random Digimon upon loading the program.
def suggest_Digimon():
    print(f"{Fore.LIGHTBLUE_EX}Here are 5 potential Digimon you can type in:")
    sample = random.sample(list(stats_dict.keys()), 5)
    for name in sample:
        print(f"  - {name}")
    print()

# Function to display the main menu options and receive user input.
def get_Input_Choice():
    print(f"{Fore.LIGHTBLUE_EX}\nWhat option would you like to do next?")
    print(f" - 1: Check if a Digimon is Classified as an Ultimate via stats")
    print(f" - 2: Search for a Digimon by its Name and check to see if it's classified as an Ultimate")
    print(f" - 3: Open the Team Management Menu")
    print(f" - 0: Exit the Program\n\n")
    user_choice = input("Please type the number that relates to your selection (from 0 to 3): ").strip()
    return user_choice

# This function prompts the user to manually input stats (HP, Attack, Defense, etc.), ensuring all entries are integers;
# looping until the user enters all valid inputs or enters 0 in the HP field to go back to the Team Manager.
def get_Stats_Manually():
    # Prompts the user for HP of the Digimon, if '0' is entered it returns the user to the Team Manager Main Menu; otherwise it records the HP for the Digimon.
    while True:
        hp_input = input("  HP: (enter 0 to return to the enter a nickname or placeholder option): ").strip()
        if hp_input == '0':
            return None
        try:
            hp = int(hp_input)
            break
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Invalid input. Please enter an integer.")

    # Continuation of the get_Stats_Manually function, this will get the other integers for the Digimon, but if 0 is entered, it does not go back to the Team Manager Main Menu.
    def get_Other_Stats_Manually(prompt):
        while True:
            val = input(f"{prompt}: ").strip()
            try:
                return int(val)
            except ValueError:
                print(f"{Fore.LIGHTRED_EX}Invalid input. Please enter an integer.")

    attack = get_Other_Stats_Manually("  Attack")
    defense = get_Other_Stats_Manually("  Defense")
    sp_attack = get_Other_Stats_Manually("  Special Attack")
    sp_defense = get_Other_Stats_Manually("  Special Defense")
    speed = get_Other_Stats_Manually("  Speed")

    return [hp, attack, defense, sp_attack, sp_defense, speed]

# The following function takes the users entered Digimon name, and retrieves the level 50 stats and determines the type of the Digimon
# to see if the Digimon is an Ultimate type based on the datasets attributes. If the name was not able to be found, it prompts the user to try again.
def retrieve_Stats_By_Name(digimon_name):
    # Attempt to find stats in the dataset using the provided name.
    entry = stats_dict.get(digimon_name)
    if not entry:
        print(f"{Fore.LIGHTRED_EX}Unable to locate the specified Digimon. Please provide a valid name.")
        return None, None, None
    print(f"{Fore.GREEN}Successfully retrieved stats for {digimon_name}.")

    # stats_list compiles the stats into a list for further analysis and easier readability.
    stats_list = [
        entry['HP lvl 50'],
        entry['SP lvl 50'],
        entry['ATK lvl 50'],
        entry['DEF lvl 50'],
        entry['INT lvl 50'],
        entry['SPD lvl 50']
    ]
    # Get the type designation, defaulting to an empty string if nothing is present.
    primary_type = entry.get('type1', '').lower()
    secondary_type = entry.get('type2', '').lower()

    return stats_list, primary_type, secondary_type

# Uses the trained model to predict if a level 50 Digimon based on its stats is at the Ultimate stage or not.
def classify_Stage(trained_model, level_stats):
    # Ensures that level_stats is a list of 6 numbers or fewer.
    if not isinstance(level_stats, list) or len(level_stats) != 6:
        print(f"{Fore.LIGHTRED_EX}Error: stats data is invalid: {level_stats}")
        return None
    feature_columns = ['HP lvl 50', 'SP lvl 50', 'ATK lvl 50', 'DEF lvl 50', 'INT lvl 50', 'SPD lvl 50']
    input_data = pd.DataFrame([level_stats], columns=feature_columns)     # Creates a DataFrame, that includes the columns and the stats for the prediction.
    # Performs the prediction and returns the result.
    prediction_result = trained_model.predict(input_data)
    return prediction_result[0]

# Loads the user's Digimon team to the TEAM_FILE.
def load_Team():
    if os.path.exists(TEAM_FILE):
        with open(TEAM_FILE, "r") as f:
            return json.load(f)
    return []

# Saves the user's Digimon team to the TEAM_FILE.
def save_Team(team):
    with open(TEAM_FILE, "w") as f:
        json.dump(team, f, indent=2)

# Command Line Interface menu for the Team Manager Menu. This menu shows options for the user to add Digimon, view their team, classify Digimon based on if they are Ultimate or not, clear their team, or return to the main menu.
def team_management_interface(model):
    global stats
    team_list = load_Team()
    while True:
        print(f"""
{Fore.LIGHTBLUE_EX}Team Manager Menu:{Style.RESET_ALL}
  1. Add a Digimon To The Team By Their Name
  2. Add a Digimon To The Team By Entering Stats Manually
  3. View Your Current Team And The Digimon's Stats
  4. Determine How Many Digimon Are Classified As Ultimates' Within Your Team
  5. Clear Your Entire Team
  0. Return To The Applications Main Menu
""")
        selection = input("Please Select An Option From The Team Manager Menu (Enter a number 0-5): ").strip()

        # Option 1 Within the Team Manager Menu: User inputs the name of a Digimon that they want to add to their team, then the application fetches the stats from the dataset, and adds it to the users team.
        if selection == "1":
            while True:
                digimon_name = input("Type the name of the Digimon (or '0' to go back): ").strip()
                if digimon_name == '0':
                    break
                # Attempts to retrieve the Digimon's stats
                retrieved = retrieve_Stats_By_Name(digimon_name)
                if not retrieved:
                    print(f"{Fore.RED}Unable to locate the specified Digimon. Please provide a valid name.")
                    continue
                # Unpack retrieved data
                stats, type1, type2 = retrieved

                # Saves to the team
                team_list.append({"name": digimon_name, "stats": stats, "type1": type1, "type2": type2})
                save_Team(team_list)
                print(f"{Fore.GREEN}Successfully added {digimon_name} to your team.")
                break

        # Option 2 Within the Team Manager Menu: The user is prompted to enter a nickname and then manually input stats for a Digimon, afterward, it is added to the team.
        elif selection == "2":
            while True:
                nickname = input("Enter a nickname or placeholder (or '0' to go back to the Team Manager Menu): ").strip()
                if nickname == '0':
                    break  # Exit to the team manager menu without adding the Digimon to the team.
                exists_in_dataset = nickname in stats_dict  # Checks if the nickname matches a pre-existing Digimon in the dataset.
                print("Please input the stats:")
                stats = get_Stats_Manually()
                if stats:
                    team_list.append({"name": nickname, "stats": stats, "is_known_digimon": exists_in_dataset})
                    save_Team(team_list)
                    print(f"{Fore.GREEN}Added {nickname} to your team.")
                    break

        # Option 3 Within the Team Manager Menu: This shows the user their current Digimon team and their correlated stats. If no Digimon are present in the team, it tells the user that the team is empty.
        elif selection == "3":
            if not team_list:
                print(f"{Fore.LIGHTYELLOW_EX}Your team currently has no assigned Digimon.")
            else:
                print(f"{Fore.LIGHTBLUE_EX}Current Team Members:")
                for index, member in enumerate(team_list, 1):
                    print(f" {index}. {member['name']} - Stats: {member['stats']}")

        # Option 4 Within the Team Manager Menu: Utilizes the prediction model to classify each Digimon within the users team as either 'Ultimate' or not and display the results to the user.
        # If there are no Digimon in the users team, it informs the user.
        elif selection == "4":
            if not team_list:
                print(f"{Fore.LIGHTYELLOW_EX}No Digimon are currently saved to your team; thus at this time, their classification of Ultimate or not cannot be checked.")
            else:
                # Double checks that the number of Digimon in the list does not exceed 6.
                if len(team_list) > 6:
                    print(f"{Fore.LIGHTRED_EX}Your team has {len(team_list)} Digimon, which exceeds the maximum of 6.")
                    print(f"{Fore.LIGHTYELLOW_EX}Please remove some Digimon before classifying.")
                    continue  # Skips the classification steps because the team member is marked as invalid or unfound in the dataset.
                for member in team_list:
                    if not member.get("is_known_digimon", True):
                        print(f"{Fore.LIGHTRED_EX}{member['name']} is not recognized in the dataset; thus, we cannot check the classification at this time.")
                    else:
                        # Begins the classification of the Digimon.
                        print(f"Classifying {member['name']}...")
                        result_label = classify_Stage(model, member['stats'])
                        classification = f"{Fore.MAGENTA}✨ Ultimate!" if result_label == 1 else f"{Fore.LIGHTYELLOW_EX}Not Ultimate"
                        print(f"{member['name']} is classified as: {classification}")

        # Option 5 Within the Team Manager Menu: Asks the user for to confirm if they want to clear their team, if 'y' is entered, it clears the team, otherwise if anything else is entered, it does not clear the team; informing the user of either outcome.
        elif selection == "5":
            confirm_reset = input("Are you sure you want to reset your team? (This action cannot be undone). Enter 'y' to confirm or any other character/integer to go back to the previous menu: ").strip().lower()
            if confirm_reset == 'y':
                team_list.clear()
                save_Team(team_list)
                print(f"{Fore.GREEN}Your team has successfully been cleared.")
            else:
                print(f"{Fore.LIGHTYELLOW_EX}No changes were made; your team remains unchanged.")

        # Exits the user from the Team Manager Menu returning the user to the main menu of the application.
        elif selection == "0":
            break
        # Handles invalid input while on the Team Manager Menu.
        else:
            print(f"{Fore.LIGHTRED_EX}Invalid choice. Please select a number between 0 and 5.")

# This function displays the application banner and suggests random Digimon upon the function being called.
def main():
    global stats
    application_Banner_Function()
    suggest_Digimon()

    # Checks to see that the Machine Learning Model is present and saved as required, if not, informing the user to train it. Once the Model has been found, it loads it.
    if not os.path.exists(MODEL_PATH):
        print(f"{Fore.LIGHTRED_EX}Model file not found at: '{MODEL_PATH}'.")
        print(f"{Fore.LIGHTYELLOW_EX}Please train and save the model using the train_Model script before proceeding.")
        sys.exit(1)

    # Load the trained Machine Learning Model for predictions.
    model = joblib.load(MODEL_PATH)

    # Start of the main loop handling the users choices to perform various functions.
    while True:
        user_option = get_Input_Choice()

        # Main Menu Option 1: Prompts the user to manually input stats to predict if a Digimon is 'Ultimate'.
        if user_option == "1":
            while True:
                stats_input = get_stats_level_50()
                if stats_input is None:
                    break # If the user enters '0' return to the applications main menu.
                prediction_result = classify_Stage(model, stats_input)
                prediction_label = f"{Fore.MAGENTA}✨ Ultimate!" if prediction_result == 1 else f"{Fore.LIGHTYELLOW_EX}Not Ultimate."
                print(f"Prediction outcome: {prediction_label}")

        # Main Menu Option 2: Prompts the user to enter a Digimon's name, then it fetches the Digimon's stats, and classifies if the Digimon is 'Ultimate' or not.
        elif user_option == "2":
            while True:
                user_input = input(f"{Fore.LIGHTBLUE_EX}Please Enter a Digimon's Name (or '0' to go back): ").strip()
                if user_input == '0':
                    break

                # Check if the users input is a number, if so, inform the user to try again.
                try:
                    num = int(user_input)
                    print(f"{Fore.LIGHTRED_EX}It appears your typed entry is a number. Please try again and enter a valid Digimon's name.")
                    continue
                except ValueError:
                    pass

                # Attempt to retrieve the stats of the entered Digimon, if unable to, inform the user to try again.
                retrieved = retrieve_Stats_By_Name(user_input)
                if not retrieved:
                    print(f"{Fore.LIGHTRED_EX}Unable to locate the Digimon entered. Please try again and provide a valid Digimon's name.")
                    continue

                # Unpack retrieved data and validate the stats length.
                stats, type1, type2 = retrieved

                if not stats or len(stats) != 6:
                    continue

                #Classification of the Digimon; is it Ultimate or not.
                prediction = classify_Stage(model, stats)
                result_text = f"{Fore.MAGENTA}✨ Ultimate!" if prediction == 1 else f"{Fore.LIGHTYELLOW_EX}Not Ultimate."
                print(f"{user_input}: {result_text}")
                break

        # Main Menu Option 3: Access team management menu for adding/viewing/classifying Digimon.
        elif user_option == "3":
            team_management_interface(model)

        # Option 0: Exits the program, leaving the user with a friendly Digimon relative message.
        elif user_option == "0":
            print(f"{Fore.LIGHTBLUE_EX}Goodbye, Tamer! Thanks for using the Digimon classifier.")
            break
        # Handles invalid user input from a user on the applications main menu.
        else:
            print(f"{Fore.LIGHTRED_EX}Invalid option. Please enter a number between 0 and 3.")

# This calls the main function and starts the application.
if __name__ == "__main__":
    main()