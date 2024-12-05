import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import requests
from typing import Dict, List
import csv
from pathlib import Path

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenFoodAPI:
    def __init__(self):
        self.base_url = "https://world.openfoodfacts.org/api/v0"

    def search_food(self, query: str, page_size: int = 5) -> List[Dict]:
        endpoint = f"{self.base_url}/search"
        params = {
            "search_terms": query,
            "page_size": page_size,
            "json": 1
        }
        
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        
        return response.json().get("products", [])

def ensure_database_exists(filepath):
    """Create the database file if it doesn't exist"""
    if not os.path.exists(filepath):
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Create the CSV file with headers
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['food', 'calories', 'serving_size', 'weight_unit', 
                           'protein', 'fat', 'carbohydrates'])

def add_food_entry(food: str, calories: float, serving_size: float, 
                  weight_unit: str, protein: float, fat: float, 
                  carbohydrates: float, filepath: str = "data/food_database.csv"):
    """Add a food entry to the database"""
    ensure_database_exists(filepath)
    
    # Read existing data
    df = pd.read_csv(filepath)
    
    # Create new entry
    new_entry = pd.DataFrame({
        'food': [food],
        'calories': [calories],
        'serving_size': [serving_size],
        'weight_unit': [weight_unit],
        'protein': [protein],
        'fat': [fat],
        'carbohydrates': [carbohydrates]
    })
    
    # Append new entry
    df = pd.concat([df, new_entry], ignore_index=True)
    
    # Save updated database
    df.to_csv(filepath, index=False)

def process_prompt_with_llm(prompt):
    """Send the prompt to an LLM to extract structured food data"""
    system_message = (
        "You are an assistant that extracts structured data from prompts. "
        "Given a natural language description, output a dictionary with fields: "
        "'food', 'calories', 'serving_size', 'weight_unit', 'protein', 'fat', 'carbohydrates'. "
        "Ensure numeric values are properly parsed. Return only the dictionary, no other text."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Extract response content
        result = response.choices[0].message.content
        return eval(result)  # Convert string response to dictionary
    except Exception as e:
        print("Error in LLM processing:", e)
        return None

def summarize_nutrition_with_llm(nutrition_data: Dict):
    """Send raw nutrition data to LLM for summarization"""
    system_message = (
        "You are a nutrition expert. Given raw nutrition data, create a clear summary "
        "of a single serving. Format it like: 'Add a food item: one serving of [food] "
        "has [X] calories, [X]g protein, [X]g fat, and [X]g carbohydrates.'"
    )
    
    # Convert nutrition data to string format
    nutrition_str = str(nutrition_data)
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Please summarize this nutrition data: {nutrition_str}"}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Error in LLM processing:", e)
        return None

def add_food_from_prompt(prompt, filepath="data/food_database.csv"):
    """Process natural language prompt, extract data, and add to database"""
    food_data = process_prompt_with_llm(prompt)
    if not food_data:
        print("Failed to process prompt.")
        return

    try:
        add_food_entry(
            food=food_data["food"],
            calories=food_data["calories"],
            serving_size=food_data["serving_size"],
            weight_unit=food_data["weight_unit"],
            protein=food_data["protein"],
            fat=food_data["fat"],
            carbohydrates=food_data["carbohydrates"],
            filepath=filepath
        )
        print(f"Added '{food_data['food']}' successfully.")
    except Exception as e:
        print("Error adding food:", e)

def add_big_mac_to_database(filepath="data/food_database.csv"):
    """Add Big Mac nutrition information to database using API and LLM"""
    # Get Big Mac data from API
    api = OpenFoodAPI()
    results = api.search_food("Big Mac McDonald's")
    
    if not results:
        print("No results found for Big Mac")
        return
    
    # Get raw nutrition data
    raw_nutrition = results[0].get("nutriments", {})
    
    # Get LLM to summarize it
    nutrition_prompt = summarize_nutrition_with_llm(raw_nutrition)
    
    if nutrition_prompt:
        print(f"Generated prompt: {nutrition_prompt}")
        # Use existing function to add to database
        add_food_from_prompt(nutrition_prompt, filepath)

def list_database(filepath="data/food_database.csv"):
    """Display all entries in the database"""
    if not os.path.exists(filepath):
        print("Database does not exist yet.")
        return
    
    df = pd.read_csv(filepath)
    print("\nCurrent database contents:")
    print(df.to_string(index=False))

# Example usage
if __name__ == "__main__":
    # Add Big Mac using API data and LLM
    add_big_mac_to_database()
    
    # Example of adding food via direct prompt
    user_prompt = "Add a food item: one cup of pizza cupcake has 285 calories, 12g protein, 10g fat, and 36g carbohydrates."
    add_food_from_prompt(user_prompt)
    
    # Display database contents
    list_database()