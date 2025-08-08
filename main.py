import os
import sys
import joblib
import pandas as pd

# Import custom modules from the 'modules' directory
from modules.main_display import application_Banner, suggest_Digimon
from modules.data_handling import retrieve_Stats_By_Name
from modules.model_utilities import classify_Stage
from modules.team_management import team_management_interface
from modules.utils import get_Input_Choice, get_stats_level_50

# Load the colorama module for colored terminal output
try:
    from colorama import Fore, Style, init
except ImportError:
    # If colorama isn't installed, attempt to install it automatically first
    print("Installing required package 'colorama'...")
    os.system(f"{sys.executable} -m pip install colorama")
    from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output, set to auto-reset colors after each print
init(autoreset=True)

# Paths for dataset, model, and team data storage
DATA_PATH = "data/Digimon.csv"
MODEL_PATH = "models/ultimate_Stage_Model.pkl"
TEAM_FILE = "data/team.json"

# Load the dataset containing Digimon stats and metadata
try:
    df = pd.read_csv(DATA_PATH, sep=';')  # Read CSV with semicolon separator
    # Convert the DataFrame into a dictionary keyed by Digimon name for quick lookup
    stats_dict = df.set_index('Digimon').to_dict(orient='index')
    # List of features/columns relevant for prediction
    features = ['HP lvl 50', 'SP lvl 50', 'ATK lvl 50', 'DEF lvl 50', 'INT lvl 50', 'SPD lvl 50']
    # Add a binary 'is_Ultimate' column: 1 if Stage string is 'Ultimate', else 0
    df['is_Ultimate'] = df['Stage'].apply(lambda s: 1 if isinstance(s, str) and s.strip().lower() == 'ultimate' else 0)
    # Keep only relevant features and the target for further analysis
    df_clean = df[features + ['is_Ultimate']].dropna()
except Exception as e:
    # If dataset fails to load, display error and exit program
    print(f"{Fore.LIGHTRED_EX}Error loading data: {e}")
    sys.exit(1)

def main():
    # Display the application banner at startup
    application_Banner()
    # Suggest 5 random Digimon to the user
    suggest_Digimon(stats_dict)

    # Check if the trained prediction model exists; if not, instruct user to train first
    if not os.path.exists(MODEL_PATH):
        print(f"{Fore.LIGHTRED_EX}Model file not found at: '{MODEL_PATH}'.")
        print(f"{Fore.LIGHTYELLOW_EX}Please train and save the model using the train_Model script before proceeding.")
        sys.exit(1)

    # Load the trained model from disk
    model = joblib.load(MODEL_PATH)

    # Main application loop to interact with user until they choose to exit
    while True:
        # Present options and get user choice
        choice = get_Input_Choice()

        # ===== Option 1: Manual stats input to predict if Digimon is Ultimate =====
        if choice == "1":
            while True:
                # Prompt user to input stats or return to main menu
                stats_input = get_stats_level_50()
                if stats_input is None:
                    break  # user chose to return
                # Use the model to predict Ultimate status based on input stats
                prediction = classify_Stage(model, stats_input)
                # Display prediction result with color
                result_str = f"{Fore.MAGENTA}✨ Ultimate!" if prediction == 1 else f"{Fore.LIGHTYELLOW_EX}Not Ultimate."
                print(f"Prediction outcome: {result_str}")

        # ===== Option 2: Search by Digimon name and classify =====
        elif choice == "2":
            while True:
                # Ask user for Digimon name or return to main menu
                user_input = input(f"{Fore.LIGHTBLUE_EX}Please Enter a Digimon's Name (or '0' to go back): ").strip()
                if user_input == '0':
                    break  # user wants to go back
                # Check if user input is a number; reject if so
                try:
                    int(user_input)
                    print(f"{Fore.LIGHTRED_EX}It appears your typed entry is a number. Please try again and enter a valid Digimon's name.")
                    continue
                except ValueError:
                    pass # input is not a number
                # Retrieve stats for the entered Digimon name from the dataset
                retrieved = retrieve_Stats_By_Name(user_input, stats_dict)
                if not retrieved:
                    print(f"{Fore.LIGHTRED_EX}Unable to locate the Digimon entered. Please try again.")
                    continue
                # Unpack retrieved data: stats list, primary type, secondary type
                stats, type1, type2 = retrieved
                # Classify the Digimon to predict if it's Ultimate
                prediction = classify_Stage(model, stats)
                # Display classification result with color
                result_str = f"{Fore.MAGENTA}✨ Ultimate!" if prediction == 1 else f"{Fore.LIGHTYELLOW_EX}Not Ultimate."
                print(f"{user_input}: {result_str}")
                break  # exit the loop after showing result

        # ===== Option 3: Access team management menu =====
        elif choice == "3":
            # Call the team management interface, passing the model and dataset info
            team_management_interface(model, stats_dict)

        # ===== Option 0: Exit program =====
        elif choice == "0":
            print(f"{Fore.LIGHTBLUE_EX}Goodbye, Tamer! Thanks for using the Digimon classifier.")
            break  # exit main loop and program

        # ===== Invalid input handling =====
        else:
            print(f"{Fore.LIGHTRED_EX}Invalid option. Please enter a number between 0 and 3.")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
