# Recipe Generator App

This project is a Recipe Generator App that generates recipes based on user-inputted ingredients. The app uses a pre-trained language model to create recipes and matches the ingredients with prices from a CSV file.

## Features

- User can input up to 10 ingredients.
- Generates a recipe based on the provided ingredients.
- Matches ingredients with prices from a CSV file.
- Displays the total cost of the recipe.

## Requirements

- Python 3.7+
- Flask
- pandas
- transformers
- torch

## Setup and Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/IOD_CapStone.git
    cd "Recipe Generator App"
    ```

2. **Create and Activate Virtual Environment**:

   If your system does not allow the creation of a virtual environment run the code below in the terminal of the folder before creating the virtual environment
   ```
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

    

4. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Download the Pre-trained Model**:
    Ensure you have the necessary pre-trained model downloaded or specify it in your `app.py`.

6. **Run the Flask App**:
    ```bash
    python app.py
    ```

## Usage

1. Open your web browser and go to `http://127.0.0.1:5000`.
2. Enter up to 10 ingredients in the provided input fields or select from the available buttons.
3. Click the "Generate Recipe" button.
4. View the generated recipe, matched ingredients, and the total price.
