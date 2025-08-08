from colorama import Fore

# Function to display main options menu and get user's selection
def get_Input_Choice():
    # Print prompt message with a specific color for clarity
    print(f"{Fore.LIGHTBLUE_EX}\nWhat option would you like to do next?")
    # List available options for the user
    print(" - 1: Check if a Digimon is Classified as an Ultimate via stats")
    print(" - 2: Search for a Digimon by its Name and check if it's classified as an Ultimate")
    print(" - 3: Open the Team Management Menu")
    print(" - 0: Exit the Program\n")
    # Prompt user to input their choice, strip whitespace for safety
    user_choice = input("Please type the number that relates to your selection (from 0 to 3): ").strip()
    return user_choice

# Function to prompt user for level 50 stats of a Digimon or to go back
def get_stats_level_50():
    # Import Fore from colorama locally to avoid global dependencies
    from colorama import Fore
    # Loop until the user inputs valid data or decides to return
    while True:
        # Prompt user to enter stats or '0' to cancel/return
        print(f"{Fore.LIGHTBLUE_EX}Enter stats of a level 50 Digimon (or 0 to return to the main menu):")
        try:
            # Prompt for HP
            hp = input("  HP: ").strip()
            # If user inputs '0', return None to indicate cancellation
            if hp == '0':
                return None
            # Convert input to integer, will raise ValueError if invalid
            hp = int(hp)

            # Prompt for Attack stat
            attack = input("  Attack: ").strip()
            if attack == '0':
                return None
            attack = int(attack)

            # Prompt for Defense stat
            defense = input("  Defense: ").strip()
            if defense == '0':
                return None
            defense = int(defense)

            # Prompt for Special Attack stat
            sp_attack = input("  Special Attack: ").strip()
            if sp_attack == '0':
                return None
            sp_attack = int(sp_attack)

            # Prompt for Special Defense stat
            sp_defense = input("  Special Defense: ").strip()
            if sp_defense == '0':
                return None
            sp_defense = int(sp_defense)

            # Prompt for Speed stat
            speed = input("  Speed: ").strip()
            if speed == '0':
                return None
            speed = int(speed)

            # Return all collected stats as a list if all inputs are valid
            return [hp, attack, defense, sp_attack, sp_defense, speed]
        except ValueError:
            # Catch invalid (non-integer) input and prompt user again
            print(f"{Fore.LIGHTRED_EX}Invalid input. Please try again utilizing integers only.")