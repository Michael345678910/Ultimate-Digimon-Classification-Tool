# Import libraries needed to train the model.
import os
import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# This will import or install (if not available to import) colorama, which is utilized to add flair within the Command Line Terminal's output.
try:
    from colorama import Fore, Style, init
except ImportError:
    print("Installing required package 'colorama'...")
    os.system(f"{sys.executable} -m pip install colorama")
    from colorama import Fore, Style, init

init(autoreset=True)  # Automatically reset colors after each print

# Loads the needed Digimon dataset.
df = pd.read_csv("data/digimon.csv", sep=';')

# Shows the user what columns are available in the Excel sheet.
print(f"{Fore.LIGHTBLUE_EX}Columns available to utilize for Digimon data comparison: \n\n", df.columns)

# Creates a binary label: 1 if stage = 'Ultimate', otherwise it turns it to a 0.
def is_Ultimate(stage):
    if isinstance(stage, str):
        return 1 if stage.strip().lower() == 'ultimate' else 0
    return 0

df['is_Ultimate'] = df['Stage'].apply(is_Ultimate)

# Targets the Ultimate variable for use later.
target = 'is_Ultimate'

# Features all needed Digimon stats at level 50.
features = ['HP lvl 50', 'SP lvl 50', 'ATK lvl 50', 'DEF lvl 50', 'INT lvl 50', 'SPD lvl 50']

# Prepares and clean up data.
df_clean = df[features + [target]].dropna()

X = df_clean[features]
y = df_clean[target]

# Train and save the RandomForest model.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Saves the model under 'ultimate_Stage_Model.pkl' to be called later.
joblib.dump(model, "models/ultimate_Stage_Model.pkl")

# Prints a confirmation to the user in the Command Line Interface to share that the application produced the trained model, and they have been saved in the model's folder.
print(f"{Fore.GREEN}\nModel has been trained to predict 'Ultimate' stage, and is saved under the 'Models/' folder.")