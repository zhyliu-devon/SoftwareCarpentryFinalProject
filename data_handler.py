import pandas as pd
from datetime import datetime
# Load food database
def load_food_data(filepath="data/food_database.csv"):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print("File not found. Creating.")
        return pd.DataFrame(columns=["food", "calories", "serving_size", "weight_unit", "protein", "fat", "carbohydrates"])

# Convert calories to custom weight
def convert_calories(food, weight, food_data):
    item = food_data[food_data["food"].str.lower() == food.lower()]
    if item.empty:
        raise ValueError("Food not in database.")
    
    item = item.iloc[0]
    factor = weight / float(item["serving_size"])
    return {
        "food": item["food"],
        "calories": round(float(item["calories"]) * factor, 2),
        "protein": round(float(item["protein"]) * factor, 2),
        "fat": round(float(item["fat"]) * factor, 2),
        "carbohydrates": round(float(item["carbohydrates"]) * factor, 2)
    }

# Add new food entry
def add_food_entry(food, calories, serving_size, weight_unit, protein, fat, carbohydrates, filepath="data/food_database.csv"):
    try:
        food_data = pd.read_csv(filepath)
    except FileNotFoundError:
        food_data = pd.DataFrame(columns=["food", "calories", "serving_size", "weight_unit", "protein", "fat", "carbohydrates"])
    
    # Check if food exists
    existing_item = food_data[food_data["food"].str.lower() == food.lower()]
    if not existing_item.empty:
        print(f"Food '{food}' exists.")
        action = input("Replace or cancel? (r/c): ").strip().lower()
        if action == "c":
            print("Addition canceled.")
            return
        elif action == "r":
            food_data = food_data[food_data["food"].str.lower() != food.lower()]
            print(f"Replacing '{food}' entry.")
        else:
            print("Invalid input. Canceled.")
            return

    # Add new entry
    new_data = pd.DataFrame([{
        "food": food,
        "calories": calories,
        "serving_size": serving_size,
        "weight_unit": weight_unit,
        "protein": protein,
        "fat": fat,
        "carbohydrates": carbohydrates
    }])
    updated_data = pd.concat([food_data, new_data], ignore_index=True)
    updated_data.to_csv(filepath, index=False)
    print(f"'{food}' added successfully.")

# Load food database
def load_food_data(filepath="data/food_database.csv"):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print("Food database not found. Creating a new one.")
        return pd.DataFrame(columns=["food", "calories", "serving_size", "weight_unit", "protein", "fat", "carbohydrates"])

# Load daily data
def load_daily_data(filepath="data/daily_data.csv"):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print("Daily data not found. Creating a new one.")
        return pd.DataFrame(columns=["date", "food", "weight", "calories", "protein", "fat", "carbohydrates"])

# Write daily calorie data
def write_daily_data(date, food, weight, food_data, daily_data_filepath="data/daily_data.csv"):
    daily_data = load_daily_data(daily_data_filepath)

    # Calculate values for the food
    try:
        result = convert_calories(food, weight, food_data)
    except ValueError as e:
        print(str(e))
        return

    # Add to daily data
    new_entry = {
        "date": date,
        "food": result["food"],
        "weight": weight,
        "calories": result["calories"],
        "protein": result["protein"],
        "fat": result["fat"],
        "carbohydrates": result["carbohydrates"]
    }
    daily_data = pd.concat([daily_data, pd.DataFrame([new_entry])], ignore_index=True)
    daily_data.to_csv(daily_data_filepath, index=False)
    print(f"Added {result['food']} to daily data for {date}.")

# Get daily summary
def get_daily_summary(date, daily_data_filepath="data/daily_data.csv"):
    daily_data = load_daily_data(daily_data_filepath)
    day_data = daily_data[daily_data["date"] == date]

    if day_data.empty:
        print(f"No data for {date}.")
        return {}

    summary = day_data[["calories", "protein", "fat", "carbohydrates"]].sum()
    summary["date"] = date
    return summary

# Example usage
if __name__ == "__main__":
    # Load the food database
    food_data = load_food_data()
    
    # Add some daily entries
    write_daily_data("2024-12-08", "pasta", 150, food_data)
    write_daily_data("2024-12-08", "apple", 200, food_data)
    write_daily_data("2024-12-08", "apple", 200, food_data)
    add_food_entry("pasta", 350, 100, "gram", 7.0, 1.3, 70.0)
    # Get summary for a specific date
    summary = get_daily_summary("2024-12-09")
    print("Daily Summary:")
    print(summary)

    # food_data = load_food_data()

    # # Convert calories
    # result = convert_calories("apple", 150, food_data)
    # print(result)
