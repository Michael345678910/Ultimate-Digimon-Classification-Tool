import pandas as pd

# Function to classify whether a Digimon is at the 'Ultimate' stage based on its stats
def classify_Stage(model, stats):
    # Define the list of feature columns that the model was trained on
    feature_cols = [
        'HP lvl 50',    # Hit Points at level 50
        'SP lvl 50',    # Special Points at level 50
        'ATK lvl 50',   # Attack stat at level 50
        'DEF lvl 50',   # Defense stat at level 50
        'INT lvl 50',   # Special Attack (Intelligence) at level 50
        'SPD lvl 50'    # Speed stat at level 50
    ]
    # Convert the input stats list into a DataFrame with appropriate column names
    input_data = pd.DataFrame([stats], columns=feature_cols)
    # Use the trained model to predict the class (Ultimate or not)
    prediction = model.predict(input_data)
    # Return the predicted class label (e.g., 1 for Ultimate, 0 for not)
    return prediction[0]