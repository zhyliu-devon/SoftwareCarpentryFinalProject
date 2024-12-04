"""
# Intelligent Calorie Tracker

## Overview
This app helps track food calories and nutrients. 
It uses GPT for natural language input.

## Features
- Log food with plain text.
- Convert data for servings or weight.
- GPT processes user input.
- Save food data in files.

## Install

### Requirements
- Python 3.8 or higher
- pip
- OpenAI API key

### Steps
1. Clone the project:
   git clone https://github.com/zhyliu-devon/SoftwareCarpentryFinalProject.git
   cd SoftwareCarpentryFinalProject

2. Install libraries:
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt

3. Add API key:
   - Create a `.env` file.
   - Add this to `.env`: 
     OPENAI_API_KEY=your_key_here

## Usage

### Start App
Run this:
   python main.py

### Add Food
Example:
   "Add: pizza, 285 cal, 1 slice, 12g protein, 10g fat, 36g carbs."

The app saves it.

### Edit Data
Manually edit `data/food_database.csv`:
   food,calories,serving_size,weight_unit,protein,fat,carbohydrates
   apple,52,100,gram,0.3,0.2,14

## Structure
.
├── .env                # Stores API key
├── README.md           # Instructions
├── main.py             # Start app
├── llm_handler.py      # Handles GPT
├── data_handler.py     # Food data tools
├── data/               # Stores food data
│   ├── food_database.csv

## Development
1. Fork project.
2. Make a new branch.
3. Commit and push changes.
4. Open a pull request.

## Security
- Do not share `.env` or API key.
- `.env` is ignored by Git.

## License
MIT License.
"""
