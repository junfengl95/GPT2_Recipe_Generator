from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load your trained transformer model
model_name = "JunF1122/gpt2_finetuned_new_10000recipe_chicken"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Load the CSV file
fairprice_online = pd.read_csv('fairprice_shopping_list.csv')

def prepare_input_text(ingredients_list):
    if len(ingredients_list) > 10:
        ingredients_list = ingredients_list[:10]  # Truncate to the first 10 ingredients

    input_text = "<INPUT_START>"
    for ingredient in ingredients_list:
        input_text += f" {ingredient} <NEXT_INPUT>"
    input_text = input_text.rstrip(" <NEXT_INPUT>")
    input_text += " <INPUT_END><INGR_START>"
    return input_text

def recipe_sheet(generated_recipe):
    try:
        # Print the generated recipe for debugging
        logging.debug(f"Generated Recipe: {generated_recipe}")
        
        # Extract title
        title = generated_recipe.split("<TITLE_START>")[1].split("<TITLE_END>")[0].strip()

        if "<INPUT_START>" in generated_recipe and "<INPUT_END>" in generated_recipe:
            user_ingredients = generated_recipe.split("<INPUT_START>")[1].split("<INPUT_END>")[0].replace("<NEXT_INPUT>", ", ").strip()
        else:
            user_ingredients = "No input ingredients found"

        # Extract recipe ingredients
        if "<INGR_START>" in generated_recipe and "<INGR_END>" in generated_recipe:
            recipe_ingredients = generated_recipe.split("<INGR_START>")[1].split("<INGR_END>")[0].replace("<NEXT_INGR>", "\n").strip()
        else:
            recipe_ingredients = "No recipe ingredients found"

        # Extract instructions
        if "<INSTR_START>" in generated_recipe and "<INSTR_END>" in generated_recipe:
            instructions = generated_recipe.split("<INSTR_START>")[1].split("<INSTR_END>")[0].replace("<NEXT_INSTR>", "\n").strip()
        else:
            instructions = "No instructions found"

        # Prepare output
        recipe_output = {
            'title': title,
            'user_ingredients': user_ingredients,
            'recipe_ingredients': recipe_ingredients,
            'instructions': instructions
        }
        
        #Split user_ingredients and strip whitespace
        ingredients_list = [ingredient.strip() for ingredient in user_ingredients.split(', ')]

        # Matching the user ingredients to the CSV data
        matching_ingredients = fairprice_online[fairprice_online['Ingredient'].isin(ingredients_list)]

        matched_ingredients = [{'Ingredient': row['Ingredient'], 'Price': row['Price']} for _, row in matching_ingredients.iterrows()]

        total_price = matching_ingredients['Price'].sum()

        recipe_output['matched_ingredients'] = matched_ingredients
        recipe_output['total_price'] = round(total_price, 2)

        # Debugging output
        print("Processed User Ingredients:", user_ingredients)
        print("Ingredients List:", ingredients_list)
        print("Matched Ingredients:", matched_ingredients)
        print("Total Price:", total_price)

        return recipe_output

    except IndexError as e:
        logging.error(f"IndexError occurred: {e}")
        return {
            'error': 'Failed to parse generated recipe. Please try again.'
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    ingredients = data['ingredients']
    input_text = prepare_input_text(ingredients)
    
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    generated_sequence = model.generate(input_ids, max_length=512, num_return_sequences=1,
                                        no_repeat_ngram_size=3, pad_token_id=50266)

    generated_recipe = tokenizer.decode(generated_sequence[0])
    recipe_output = recipe_sheet(generated_recipe)
    
    return jsonify(recipe_output)

if __name__ == '__main__':
    app.run(debug=True)