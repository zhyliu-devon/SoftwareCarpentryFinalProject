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

image_path = "E:\\Desktop\\SoftwareCarp\\Final\\code\\SoftwareCarpentryFinalProject\\images\\image1.png"

# get base64 string
base64_image = encode_image(image_path)

# send request
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this image?"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
            ],
        }
    ],
    max_tokens=100
)
print(response.choices[0].message.content) 
# print response
print(response)
