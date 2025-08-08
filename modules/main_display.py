from colorama import Fore, Style
import random  # Import needed for random sampling of Digimon names

# Function to display the application banner at the start of the program
def application_Banner():
    # Multi-line string containing stylized banner with colors
    banner = f"""
{Fore.LIGHTCYAN_EX}{Style.BRIGHT}
◇═══════════════════════════════════════════════════◇
▕       Ultimate Digimon Classification Tool        ▏
▕───────────────────────────────────────────────────▏
▕ Tip: Search by Digimon name, stat, or manage team ▏
◇═══════════════════════════════════════════════════◇
{Style.RESET_ALL}
"""
    # Print the banner to the console
    print(banner)

# Function to suggest 5 random Digimon names from the dataset
def suggest_Digimon(stats_dict):
    # Print an introductory message in a distinct color
    print(f"{Fore.LIGHTBLUE_EX}Here are 5 potential Digimon you can type in:")
    # Use the random module to select 5 random Digimon names from the dataset keys
    sample = random.sample(list(stats_dict.keys()), 5)
    # Loop over the sampled names and display each
    for name in sample:
        print(f"  - {name}")
    print()  # Add an extra blank line for spacing