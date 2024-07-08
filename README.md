# IOD_Capstone_Project Recipe Generator

## Overview
- The Recipe Generator is an AI-powered tool that creates cooking recipes based on the user preferences and ingredients.
- This project leverages on the HuggingFace GPT2LMHeadModel.from_pretrained("gpt2") to train and generate the recipes
- The model is trained on only 10, 000 chicken recipes due to limited resources
- The trained model can be accesed from HuggingFace [10,000-chickenRecipes](https://huggingface.co/JunF1122/gpt2_finetuned_new_10000recipe_chicken)

## Features
- Visualization: Visualize ingredient usage and recipe trends with Matplotlib
- Generate Recipes: Create recipes based on a list of ingredients or specified 

## Key Functions
Assuming the trained model have been loaded,
`prepare_input_text(ingredient_list)` 
This function prepares the input text for the recipe generation model by formatting the list of ingredients into a structured input string.
```
def prepare_input_text(ingredients_list):
    if len(ingredients_list) > 10:
        ingredients_list = ingredients_list[:10]  # Truncate to the first 10 ingredients

    input_text = "<INPUT_START>"
    for ingredient in ingredients_list:
        input_text += f" {ingredient} <NEXT_INPUT>"
    input_text = input_text.rstrip(" <NEXT_INPUT>")  # Remove the last <NEXT_INPUT>
    input_text += " <INPUT_END><INGR_START>"  # Add the <INPUT_END><INSTR_START> tokens 
    return input_text
```
- Parameters: `ingredients_list` (list of str): A list of ingredient names.
- Returns: `input_text`: A formatted input text string.
___
`input_ingredients()`
This function prompts the user to enter up to 10 ingredients and returns the formatted input text using `prepare_input_text`
```
def input_ingredients():
    ingredients_list = []

    for i in range(10):
        ingredient = input(f"Enter ingredient {i+1} (or 'stop' to finish): ").strip()
        if ingredient.lower() == 'stop':
            break
        ingredients_list.append(ingredient)

    return prepare_input_text(ingredients_list)
```
___
`generate_recipe`
This function will use the pre-trained model to generate recipes based on the test input from the user such that it matches the format of the dataset used for training.
```
input_sequence = tokenizer_hug.encode(test_input, return_tensors="pt")

generated_sequence = model_hug.generate(input_sequence, max_length=512, num_return_sequences=1, temperature=0.7,
                                        no_repeat_ngram_size=3, pad_token_id=50266) # token_id 50266 is <RECIPE_END>

generated_recipe = tokenizer_hug.decode(generated_sequence[0]) # Do not skip_special_tokens will use for post-processing
generated_recipe
```
___
`recipe_sheet(generated_recipe`
This function styles the produced recipes to a more User friendly format as a Recipe sheet as well as calculate the total cost of ingredients
```
def recipe_sheet(generated_recipe):
    user_ingredients = generated_recipe.split("<INPUT_START>")[1].split("<INPUT_END>")[0].replace("<NEXT_INPUT>", ", ").strip()
    recipe_ingredients = generated_recipe.split("<INGR_START>")[1].split("<INGR_END>")[0].replace("<NEXT_INGR>", "\n").strip()
    instructions = generated_recipe.split("<INSTR_START>")[1].split("<INSTR_END>")[0].replace("<NEXT_INSTR>", "\n").strip()
    title = generated_recipe.split("<TITLE_START>")[1].split("<TITLE_END>")[0].strip()
    
    print(title)
    print('')
    print('Input')
    print(user_ingredients)
    print('')
    print('Ingredients')
    print(recipe_ingredients)
    print('')
    print('Directions')
    print(instructions)
    
    print('-' * 100)
    
    for index, row in matching_ingredients.iterrows():
        print(f'Ingredient: {row["Name"]}, Price: {row["Price"]}')
    
    print()

    total_price = matching_ingredients['Price'].sum()
    print(f'Total price: ${round(total_price, 2)}')
```

An example is as below
```
Chicken With Brocolli And Onions

Input
chicken breast ,  pepper ,  salt ,  oil ,  garlic ,  paprika ,  onion ,  brocolli

Ingredients
1 lb chicken breast
1/2 tsp pepper
1 tsp salt
1 tbsp oil
1 garlic clove
1 1/2 tbsp paprika
1 None onion, finely chopped
1 lb brocollini, cut into 1 inch pieces
None None Poultry seasoning

Directions
Preheat oven to 400°F. Line a baking tray with parchment paper.
Sprinkle chicken with pepper and salt. Heat oil in a large frying pan over medium heat. Cook chicken, turning once, until browned all over and cooked through, about 5 mins. Transfer to a plate.
Add garlic and onion to pan and cook, stirring, until fragrant, about 1 min. Add brocollis and cook until crisp-tender, about 3 mins. Add paprika and cook for 1 min, stirring.
Stir in onion and cook 1 min more. Add chicken and cook 2 mins, until cooked through.
Transfer to serving platter. Top with chicken and serve.
----------------------------------------------------------------------------------------------------
Ingredient: FairPrice Salt - Fine, Price: 0.25
Ingredient: Chef China Old Garlic, Price: 1.9
Ingredient: Chef Yellow Onion - Large, Price: 1.93
Ingredient: Sadia Skinless Chicken Breast, Price: 8.23
Ingredient: GWS Black Pepper Ground (Bottle), Price: 6.0
Ingredient: MasterFoods Spices - Paprika Ground, Price: 4.44

Total price: $22.75
```

## DataSource
This project utilizes the RecipeNLG dataset from :
Bień, M., Gilski, M., Maciejewska, M., Taisner, W., Wisniewski, D., & Lawrynowicz, A. (2020). [RecipeNLG: A Cooking Recipes Dataset for Semi-Structured Text Generation](https://www.aclweb.org/anthology/2020.inlg-1.4.pdf). In Proceedings of the 13th International Conference on Natural Language Generation (pp. 22–28). Association for Computational Linguistics. 

The prices for the ingredients taken from FairPrice Singapore was obtained manually and recorded in excel as of September 2023.


## Citation
@inproceedings{bien-etal-2020-recipenlg,
    title = "{R}ecipe{NLG}: A Cooking Recipes Dataset for Semi-Structured Text Generation",
    author = "Bie{\'n}, Micha{\l}  and
      Gilski, Micha{\l}  and
      Maciejewska, Martyna  and
      Taisner, Wojciech  and
      Wisniewski, Dawid  and
      Lawrynowicz, Agnieszka",
    booktitle = "Proceedings of the 13th International Conference on Natural Language Generation",
    month = dec,
    year = "2020",
    address = "Dublin, Ireland",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.inlg-1.4",
    pages = "22--28",
}
