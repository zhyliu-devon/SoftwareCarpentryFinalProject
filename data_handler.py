import pandas as pd

# Load food database
def load_food_data(filepath="data/food_database.csv"):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print("File not found. Creating.")
        return pd.DataFrame(columns=["food", "calories", "serving_size", "weight_unit", "protein", "fat", "carbohydrates"])

# Convert calories to custom weight
def convert_calories(food, weight, food_data):
    """
    Calculate calories for weight.
    """
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
    new_data = pd.DataFrame([{
        "food": food,
        "calories": calories,
        "serving_size": serving_size,
        "weight_unit": weight_unit,
        "protein": protein,
        "fat": fat,
        "carbohydrates": carbohydrates
    }])
    
    try:
        food_data = pd.read_csv(filepath)
    except FileNotFoundError:
        food_data = pd.DataFrame(columns=["food", "calories", "serving_size", "weight_unit", "protein", "fat", "carbohydrates"])
    
    updated_data = pd.concat([food_data, new_data], ignore_index=True)
    updated_data.to_csv(filepath, index=False)

# Example usage
if __name__ == "__main__":
    # Load data
    food_data = load_food_data()
    
    # Add food
    add_food_entry("pasta", 350, 100, "gram", 7.0, 1.3, 70.0)
    
    # Convert calories
    result = convert_calories("apple", 150, food_data)
    print(result)
