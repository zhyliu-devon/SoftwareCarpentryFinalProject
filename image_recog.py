import torch
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image

# Load the feature extractor and model
extractor = AutoFeatureExtractor.from_pretrained("Kaludi/Food-Classification")
model = AutoModelForImageClassification.from_pretrained("Kaludi/Food-Classification")

def recognize_food(image_path):
    # Open and preprocess the image
    image = Image.open(image_path).convert("RGB")
    inputs = extractor(images=image, return_tensors="pt")

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get the predicted class
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    predicted_class = model.config.id2label[predicted_class_idx]
    
    return predicted_class

# Test the function
if __name__ == "__main__":
    image_path = "E:\\Desktop\\SoftwareCarp\\Final\\code\\SoftwareCarpentryFinalProject\\images\\image1.png"  # Replace with your image path
    food_item = recognize_food(image_path)
    print(f"Recognized food item: {food_item}")
