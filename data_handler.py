import pandas as pd

def load_food_data(filepath="data/food_database.csv"):
    return pd.read_csv(filepath)

def save_logs(data, filepath="data/logs.csv"):
    data.to_csv(filepath, index=False)
