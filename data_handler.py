import pandas as pd

# Conversion factors
CONVERSION_FACTORS = {
    "lb_to_gram": 453.592
}

# Add new food 
def add_food_entry(
    food, calories, weight=None, weight_unit=None, serving_size=None, serving_description=None, protein=0, fat=0, carbohydrates=0, filepath="data/food_database.csv"
):
    """
    Add a new food entry to the database, or replace an existing entry.
    """

    try:
        food_data = pd.read_csv(filepath)
    except FileNotFoundError:
        # Create an empty database if the file doesn't exist
        food_data = pd.DataFrame(columns=["food", "calories", "weight", "weight_unit", "serving_size", "serving_description", "protein", "fat", "carbohydrates"])
    
    # Check if the food already exists
    existing_item = food_data[food_data["food"].str.lower() == food.lower()]
    if not existing_item.empty:
        print(f"Food '{food}' already exists.")
        action = input("Do you want to replace it? (y/n): ").strip().lower()
        if action != "y":
            print("Operation canceled.")
            return
    
        # Remove the existing entry
        food_data = food_data[food_data["food"].str.lower() != food.lower()]
        print(f"Replacing '{food}' entry.")
    
    # Validation: Ensure consistency if both weight and serving size are provided
    if weight is not None and serving_size is not None:
        print(f"Ensuring consistency for '{food}' with both weight and serving size.")
        print(f"1 serving will be assumed as {weight} {weight_unit}.")
        confirm = input("Is this correct? (y/n): ").strip().lower()
        if confirm != "y":
            print("Operation canceled. Please re-enter with correct details.")
            return
    
    # Add the new entry
    new_entry = {
        "food": food,
        "calories": calories,
        "weight": weight,
        "weight_unit": weight_unit,
        "serving_size": serving_size,
        "serving_description": serving_description,
        "protein": protein,
        "fat": fat,
        "carbohydrates": carbohydrates
    }
    food_data = pd.concat([food_data, pd.DataFrame([new_entry])], ignore_index=True)
    food_data.to_csv(filepath, index=False)
    print(f"Food '{food}' has been successfully added to the database.")


# Load food
def load_food_data(filepath="data/food_database.csv"):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print("Food database not found. Creating a new one.")
        return pd.DataFrame(columns=["food", "calories", "weight", "weight_unit", "serving_size", "serving_description", "protein", "fat", "carbohydrates"])

# Load daily data
def load_daily_data(filepath="data/daily_data.csv"):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print("Daily data not found. Creating a new one.")
        return pd.DataFrame(columns=["date", "food", "quantity", "unit", "calories", "protein", "fat", "carbohydrates"])

# Convert 
def convert_to_grams(quantity, unit):
    if unit.lower() == "gram":
        return quantity
    elif unit.lower() == "lb":
        return quantity * CONVERSION_FACTORS["lb_to_gram"]
    else:
        raise ValueError(f"Unsupported weight unit: {unit}")

# Calculate nutrition
def calculate_nutrition(food, quantity, unit, food_data):
    item = food_data[food_data["food"].str.lower() == food.lower()]
    if item.empty:
        raise ValueError("Food not in database.")
    
    item = item.iloc[0]

    # Case 1: Food has only weight information
    if pd.notna(item["weight"]) and pd.isna(item["serving_size"]):
        if unit.lower() in ["gram", "lb"]:
            weight_in_grams = convert_to_grams(quantity, unit)
            factor = weight_in_grams / float(item["weight"])
        else:
            return "Unit mismatch: This food only supports weight-based calculations (e.g., grams, lb)."

    # Case 2: Food has only serving information
    elif pd.notna(item["serving_size"]) and pd.isna(item["weight"]):
        if unit.lower() == "serving":
            factor = quantity / float(item["serving_size"])
        else:
            return "Unit mismatch: This food only supports serving-based calculations."

    # Case 3: Food has both weight and serving information
    elif pd.notna(item["weight"]) and pd.notna(item["serving_size"]):
        if unit.lower() == "gram" or unit.lower() == "lb":
            weight_in_grams = convert_to_grams(quantity, unit)
            factor = weight_in_grams / float(item["weight"])
        elif unit.lower() == "serving":
            factor = quantity / float(item["serving_size"])
        else:
            return "Unit mismatch: Unsupported unit."

    # Case 4: No valid data for this food
    else:
        return "Data mismatch: No valid weight or serving data for this food."

    # Calculate nutrition
    return {
        "food": item["food"],
        "calories": round(float(item["calories"]) * factor, 2),
        "protein": round(float(item["protein"]) * factor, 2),
        "fat": round(float(item["fat"]) * factor, 2),
        "carbohydrates": round(float(item["carbohydrates"]) * factor, 2)
    }

# Write daily 
def write_daily_data(date, food, quantity, unit, food_data, daily_data_filepath="data/daily_data.csv"):
    daily_data = load_daily_data(daily_data_filepath)

    # Calculate nutrition
    try:
        result = calculate_nutrition(food, quantity, unit, food_data)
        if isinstance(result, str):  # If result is an error message
            print(result)
            return
    except ValueError as e:
        print(str(e))
        return

    # Add to daily data
    new_entry = {
        "date": date,
        "food": result["food"],
        "quantity": quantity,
        "unit": unit,
        "calories": result["calories"],
        "protein": result["protein"],
        "fat": result["fat"],
        "carbohydrates": result["carbohydrates"]
    }
    daily_data = pd.concat([daily_data, pd.DataFrame([new_entry])], ignore_index=True)
    daily_data.to_csv(daily_data_filepath, index=False)
    print(f"Added {result['food']} to daily data for {date}.")

if __name__ == "__main__":
    food_data = load_food_data()
    
    # Add  daily 
    write_daily_data("2024-12-09", "pasta", 150, "gram", food_data)
    write_daily_data("2024-12-09", "pasta", 1, "serving", food_data)
    write_daily_data("2024-12-09", "pasta", 1, "lb", food_data)

    add_food_entry(
        food="Pasta",
        calories=350,
        weight=100,
        weight_unit="gram",
        serving_size=1,
        serving_description="1 cup",
        protein=7.0,
        fat=1.3,
        carbohydrates=70.0
    )
