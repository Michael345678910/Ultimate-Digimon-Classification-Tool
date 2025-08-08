from colorama import Fore, Style

# Import functions for handling team data and statistics from other modules
from .data_handling import load_Team, save_Team, retrieve_Stats_By_Name
from .model_utilities import classify_Stage


# Function to manually get stats input from user
def get_Stats_Manually():
    from colorama import Fore  # Import Fore locally to color the prompt outputs
    while True:
        # Prompt for HP stat; allow user to cancel by entering '0'
        hp_input = input("  HP: (enter 0 to cancel): ").strip()
        if hp_input == '0':
            return None  # User chose to cancel, signal with None
        try:
            # Convert HP input to integer; catch invalid entries
            hp = int(hp_input)
            break  # Valid input received, exit the loop
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Invalid input. Please enter an integer.")

    # Helper function to get other stats with similar validation
    def get_other_stat(prompt):
        while True:
            val = input(prompt + ": ").strip()
            try:
                return int(val)
            except ValueError:
                print(f"{Fore.LIGHTRED_EX}Invalid input. Please enter an integer.")

    # Sequentially prompt for other stats
    attack = get_other_stat("  Attack")
    defense = get_other_stat("  Defense")
    sp_attack = get_other_stat("  Special Attack")
    sp_defense = get_other_stat("  Special Defense")
    speed = get_other_stat("  Speed")

    # Return the collected stats as a list
    return [hp, attack, defense, sp_attack, sp_defense, speed]


# Function to handle team management menu loop
def team_management_interface(model, stats_dict):
    # Load current team data (list of dicts)
    team_list = load_Team()

    while True:
        # Display the menu options for team management
        print(f"""
{Fore.LIGHTBLUE_EX}Team Manager Menu:{Style.RESET_ALL}
  1. Add a Digimon To The Team By Their Name
  2. Add a Digimon To The Team By Entering Stats Manually
  3. View Your Current Team And The Digimon's Stats
  4. Determine How Many Digimon Are Classified As Ultimates' Within Your Team
  5. Clear Your Entire Team
  0. Return To The Applications Main Menu
""")
        # Prompt user for menu selection
        selection = input("Please Select An Option From The Team Manager Menu (Enter a number 0-5): ").strip()

        if selection == "1":
            # Adding a team member by name (existing in dataset)
            while True:
                digimon_name = input("Type the name of the Digimon (or '0' to go back): ").strip()
                if digimon_name == '0':
                    break  # User chooses to go back from this menu
                # Retrieve stats and types from dataset
                retrieved = retrieve_Stats_By_Name(digimon_name, stats_dict)
                if not retrieved:
                    print(f"{Fore.RED}Unable to locate the specified Digimon. Please provide a valid name.")
                    continue
                stats, type1, type2 = retrieved
                # Append new digimon info to team list
                team_list.append({"name": digimon_name, "stats": stats, "type1": type1, "type2": type2})
                # Save updated team to persistent storage
                save_Team(team_list)
                print(f"{Fore.GREEN}Successfully added {digimon_name} to your team.")
                break

        elif selection == "2":
            # Manually add a team member by inputting stats
            while True:
                nickname = input("Enter a nickname or placeholder (or '0' to go back): ").strip()
                if nickname == '0':
                    break  # Exit to previous menu
                # Check if entered name exists in dataset
                exists_in_dataset = nickname in stats_dict
                print("Please input the stats:")
                stats = get_Stats_Manually()
                if stats:
                    # Store the manually entered data
                    team_list.append({"name": nickname, "stats": stats, "is_known_digimon": exists_in_dataset})
                    save_Team(team_list)
                    print(f"{Fore.GREEN}Added {nickname} to your team.")
                    break

        elif selection == "3":
            # Display the current team members and their stats
            if not team_list:
                # If team is empty, notify the user
                print(f"{Fore.LIGHTYELLOW_EX}Your team currently has no assigned Digimon.")
            else:
                # List each team member with their stats
                print(f"{Fore.LIGHTBLUE_EX}Current Team Members:")
                for index, member in enumerate(team_list, 1):
                    print(f" {index}. {member['name']} - Stats: {member['stats']}")

        elif selection == "4":
            # Classify each team member as 'Ultimate' or 'Not Ultimate'
            if not team_list:
                # Cannot classify if team is empty
                print(f"{Fore.LIGHTYELLOW_EX}No Digimon are currently saved to your team; thus, classification cannot be performed.")
            else:
                # Enforce team size limit; typically max 6 members in many games
                if len(team_list) > 6:
                    print(f"{Fore.LIGHTRED_EX}Your team has {len(team_list)} Digimon, which exceeds the maximum of 6.")
                    print(f"{Fore.LIGHTYELLOW_EX}Please remove some Digimon before classifying.")
                    continue  # Skip classification if team size exceeds limit

                # Loop through each team member for classification
                for member in team_list:
                    # Check if member is recognized in the dataset
                    if not member.get("is_known_digimon", True):
                        # If not recognized, skip classification
                        print(f"{Fore.LIGHTRED_EX}{member['name']} is not recognized in the dataset; cannot classify.")
                    else:
                        # Indicate classification process
                        print(f"Classifying {member['name']}...")
                        # Use the ML model to predict if the Digimon is Ultimate
                        result_label = classify_Stage(model, member['stats'])
                        # Output the classification result with color
                        classification = f"{Fore.MAGENTA}✨ Ultimate!" if result_label == 1 else f"{Fore.LIGHTYELLOW_EX}Not Ultimate"
                        print(f"{member['name']} is classified as: {classification}")

        elif selection == "5":
            # Reset the team after user confirmation
            confirm_reset = input("Are you sure you want to reset your team? (This action cannot be undone). Enter 'y' to confirm or any other key to cancel: ").strip().lower()
            if confirm_reset == 'y':
                # Clear the team list and save the empty team
                team_list.clear()
                save_Team(team_list)
                print(f"{Fore.GREEN}Your team has successfully been cleared.")
            else:
                # Cancel reset action
                print(f"{Fore.LIGHTYELLOW_EX}No changes were made; your team remains unchanged.")

        elif selection == "0":
            # Exit the team management menu and return to the main menu
            break
        else:
            # Handle invalid inputs
            print(f"{Fore.RED}Invalid choice. Please select a number between 0 and 5.")
