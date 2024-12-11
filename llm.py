import os
from openai import OpenAI
from dotenv import load_dotenv
import data_handler

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_messages = {
    "Extract": (
        "You are an assistant that extracts structured data from prompts. "
        "Given a natural language description, output a dictionary with fields: "
        "'food', 'calories', 'serving_size', 'weight_unit', 'protein', 'fat', 'carbohydrates'. "
        "Ensure numeric values are properly parsed."
    ),
    "Estimate": (
        "You are an assistant that extimate structured data from prompts. "
        "Given a food, estimate its nutrition based on your feeling and output a dictionary with fields: "
        "'food', 'calories', 'serving_size', 'weight_unit', 'protein', 'fat', 'carbohydrates'. "
        "Ensure numeric values are properly parsed."
    ),
}
def process_prompt_with_llm(prompt, system_message):
    """
    Send the prompt to an LLM to extract structured food data.
    """
    # System instructions for the LLM

    # Send prompt to the LLM using new API structure
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
        return result  # Convert string response to dictionary
    except Exception as e:
        print("Error in LLM processing:", e)
        return None

def add_food_from_prompt(prompt, filepath="data/food_database.csv"):
    """
    Process natural language prompt, extract data, and add to database.
    """
    food_data = process_prompt_with_llm(prompt)
    if not food_data:
        print("Failed to process prompt.")
        return

    # Add the extracted data to the database
    try:
        data_handler.add_food_entry(
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

# Example usage
if __name__ == "__main__":
    user_prompt = "Add a food item: one cup of pizza cupcake has 285 calories, 12g protein, 10g fat, and 36g carbohydrates."
    add_food_from_prompt(user_prompt)