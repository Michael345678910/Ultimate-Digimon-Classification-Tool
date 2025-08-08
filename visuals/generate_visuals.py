# Import libraries needed for generating the visuals.
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from colorama import Fore
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Ensure visuals directory exists.
os.makedirs("generated_Images", exist_ok=True)

# Loads the needed Digimon dataset.
df = pd.read_csv("../data/Digimon.csv", sep=';')

# Sets features columns specifically targeting the dataset's level 50 stats.
features = ['HP lvl 50', 'SP lvl 50', 'ATK lvl 50', 'DEF lvl 50', 'INT lvl 50', 'SPD lvl 50']
target = 'is_Ultimate'  # Makes sure this column exists; if not creates it if needed.

# Labels Digimon as 1 if 'Stage' is 'Ultimate', otherwise it labels it as 0, handling cases and spaces.
df['is_Ultimate'] = df['Stage'].apply(lambda s: 1 if isinstance(s, str) and s.strip().lower() == 'ultimate' else 0)

# Prepare and clean the data.
df_clean = df[features + [target]].dropna()
X = df_clean[features]
y = df_clean[target]

# 1. Histogram: Speed Distribution.
plt.figure(figsize=(10, 6))
plt.hist(df['SPD lvl 50'].dropna(), bins=25, color='orchid', edgecolor='darkblue', alpha=0.8)
plt.title("Distribution of Digimon Speed Stats", fontsize=14, fontweight='bold')
plt.xlabel("Speed Value", fontsize=12)
plt.ylabel("Number of Digimon", fontsize=12)
plt.grid(axis='y', color='gray', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("generated_Images/speed_Distribution_Histogram.png")
plt.close()

# 2. Scatterplot: Attack vs Defense by Stage.
plt.figure(figsize=(9, 6))
sns.scatterplot(
    data=df,
    x='ATK lvl 50',
    y='DEF lvl 50',
    hue='is_Ultimate',
    palette='Spectral',
    s=100,
    edgecolor='gray'
)
plt.title("Attack vs Defense - Stage Classification", fontsize=16, fontweight='bold')
plt.xlabel("Attack Power")
plt.ylabel("Defense Power")
plt.legend(title="Ultimate Status", fontsize=12, title_fontsize=12)
plt.figtext(0.5, 0.01, "In this plot, 1 = Ultimate, 0 = Non-Ultimate", ha="center", fontsize=10, style='italic') # Explains what 1 and 0 means in the diagram
plt.tight_layout()
plt.savefig("generated_Images/attack_Vs_Defense.png")
plt.close()

# 3. Confusion Matrix Classifier.
X_train_split, X_test_split, y_train_split, y_test_split = train_test_split(
    X, y, test_size=0.2, random_state=2024)

# Train the Random Forest classifier
rf_model = RandomForestClassifier(n_estimators=150, max_depth=10, random_state=2024)
rf_model.fit(X_train_split, y_train_split)

# Make predictions on test data
predictions = rf_model.predict(X_test_split)

# Compute the confusion matrix with labels
cmatrix = confusion_matrix(y_test_split, predictions, labels=[0, 1])

# Create an image with color mapping and labels
disp = ConfusionMatrixDisplay(confusion_matrix=cmatrix, display_labels=["Non-Ultimate", "Ultimate"])
disp.plot(cmap='pink')
plt.title("Classifier Performance: Stage Prediction")
plt.tight_layout()
plt.savefig("generated_Images/confusion_Matrix.png")
plt.close()

# Prints a confirmation to the user in the Command Line Interface to share that the application produced the visualizations, and they have been saved in the visual's folder.
print(f"{Fore.LIGHTGREEN_EX}Visualizations saved in the 'generated_Images/' folder.")

