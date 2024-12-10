import base64
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# encode image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def process_image(image_path):
    try:
        # Encode the image to base64
        base64_image = encode_image(image_path)

        # Send request to OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "If there is a nutrition table available, extract it. Otherwise, try to estimate the nutrition table for this (Calorie, Protein, Fat, Carbs, Sodium)."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                    ],
                }
            ],
            max_tokens=100
        )
        print(response.choices[0].message.content) 
        # print response
        print(response)
        # Extract and return the result
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing image: {e}"

