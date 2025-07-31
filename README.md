# Ultimate-Digimon-Classification-Tool

# Overview:

I developed this project for my friend, who is very interested and big into the Digimon Story: Cyber Sleuth game. He wanted a team management tool for the game that he could have open simultaneously as he played the game; all of the additional uses the program has, such as the machine learning aspect to guess if a Digimon is Ultimate or not, the visuals, or the user_guide.txt file, I added for fun to build onto the existing projects core idea and structure.

This project is a comprehensive application designed for Digimon enthusiasts, data scientists, and developers interested in data classification and visualization. It leverages data science techniques and machine learning algorithms to accurately classify Digimon stages, specifically predicting whether a Digimon is at the Ultimate stage based on its level-50 stats.

The application offers an intuitive command-line interface (CLI) that enables users to input Digimon stats manually or search by name to receive predictions about their stage. Beyond individual predictions, users can build and manage a team of up to six Digimon, view their details, and classify each team member's stage. To deepen understanding of the data and modeling process, the application also has the ability to generate insightful visualizations such as histograms, scatter plots, and confusion matrices, which help analyze data distributions found within the Digimon, along with showing the performance of the classification model.

Designed with ease of use in mind, this project combines data handling, machine learning, user interaction, and visualization tools within a single, accessible platform. Whether you wish to explore Digimon data, apply machine learning models, or experiment with data visualization, this project provides a flexible and educational experience.

# Features:

Trains a Random Forest classifier model to predict if a Digimon's stage is Ultimate, utilizing each Digimon's stats at level 50.
Uses the command-line interface (CLI) as the interface between the user and the program, allowing the user to input stats, name-based queries, enter the Team Management Menu, or enter any other entry into the program's console.
Allows the user to manage a team of up to six Digimon: add by name or manually input stats, view the team, classify whether the Digimon in a team are Ultimate or not, and clear the user's team.
Generate data visualizations, including a histogram, scatter plot, and confusion matrices, to visualize data distributions and model performance.
Easy setup and execution for data analysis, modeling, and predictions.

# First-Time Setup & Installation For The Application:

Clone this repository.
Ensure that Python 3.11 is installed inside of a runable IDE (Such as PyCharm).

- To start this program and download all the files and libraries needed, you will need to have the requirements.txt and the other files in this program downloaded to your personal PC and ready for use.
- Make sure the dataset (Digimon.csv), model, and scripts are in the correct directories as specified in the user_Guide.txt document.
- Once that is done, you will need to open the terminal in PyCharm, after selecting the folder Digimon_Tournament.
- Then, once in the terminal, for Windows, you will enter: venv\Scripts\activate
- OR for Mac/Linux, you will enter: source venv/bin/activate
- Next, you will type into the terminal: pip install -r requirements.txt
- Then you will wait until you start to see "Successfully installed package1, package2, package3, ..."; once that is done, move on to the next step.

# Usage Instructions:

## First-Time Setup - Model:

Train the model by running the train_Model.py file.
This will generate and save a trained classifier (ultimate_stage_model.pkl) into a new folder titled "models" within the Digimon_Tournament folder.

## Running the Main Program:

Start the application by running the main.py file.

Use the menu options:
1. To input stats manually and predict the Ultimate status.
2. To search for a Digimon by name and view the Ultimate status prediction.
3. To access the team management menu (add, view, classify, clear).
0. To exit the application or go back to a menu.

**For a more detailed and in-depth walkthrough of each of the menu options, please view the user_Guide.txt file and begin reading from the **Using the Main Application (`main.py`):** section.**

## Visualizations:
Generate the visuals by running the generate_Visuals.py file.
Then, a new folder inside the "visuals" folder will be generated, titled "generated_Images". Inside this new folder, there will be 3 visual outputs, including a histogram, scatter plot, and confusion matrices.

# Notes Regarding Contributing To The Code:
Contributions are welcome! Please feel free to fork the repository, make your modifications or add new features, and submit a pull request.

# Licensing and Trademarks:
This project is for educational purposes and is not intended for commercial use.

Note: Digimon is a registered trademark of Kabushiki Kaisha Bandai, or Bandai Co., Ltd., and all rights are reserved by Kabushiki Kaisha Bandai/Bandai Co., Ltd.

The dataset used in this project is the "Digimon Cyber Sleuth Dataset" authored by Liane Brisebois, available on Kaggle: https://www.kaggle.com/datasets/lianebrisebois/digimon-cyber-sleuth-dataset/data  || Or the Excel file utilized in this project can be downloaded from the data folder.
