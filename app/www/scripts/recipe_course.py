# Practice: a terminal recipe menu using a list of dicts. Run directly; not an API endpoint.
recipes = []

def menu_func():
    menu = input("Enter 1 to see the recipes 2 to add a recipe an 3 to delete a recipe and 4 to exit ")
    return menu


def print_recipes():
    if not recipes:
        print("no recipes yet!")
        return
    for recipe in recipes:
        print(f"{recipe['id']}.{recipe['name']}")
        print (f"    Ingredients: {recipe['ingredients']}")
        print()

def add_recipe():
    name = input("enter recipe name: ")
    ingredients = input("Enter Ingredients: ")

    if (recipes):
        recipe_id = len(recipes) + 1
    else: recipe_id = 1

    recipes.append({
        "id": recipe_id,
        "name" : name,
        "ingredients" : ingredients
    })

def delete_recipe():
    recipe_id = int(input("ID of recipe to delete "))
    for recipe in recipes:
        if recipe_id == recipe['id']:
            recipes.remove(recipe)
            print ("Deleted!")
            break
        else: print("Recipe not found!")



while True:
    menu = menu_func()

    if menu == "1":
        print_recipes()

    if menu == "2":
        add_recipe()

    if menu == "3":
        delete_recipe()

    if menu == "4":
        break







