# Practice: the recipe menu again, using a Recipe class. Run directly; not an API endpoint.
recipes = []

class Recipe:
    def __init__(self, recipe_id, name, ingredients):
        self.id = recipe_id
        self.name = name
        self.ingredients = ingredients


def menu_func():
    return input("Enter 1 to see the recipes, 2 to add a recipe, 3 to delete a recipe, 4 to exit: ")


def print_recipes():
    if not recipes:
        print("No recipes yet!")
        return
    for recipe in recipes:
        print(f"{recipe.id}. {recipe.name}")
        print(f"    Ingredients: {recipe.ingredients}")
        print()


def add_recipe():
    name = input("Enter recipe name: ")
    ingredients = input("Enter ingredients: ")

    if recipes:
        recipe_id = max(r.id for r in recipes) + 1
    else:
        recipe_id = 1

    recipes.append(Recipe(recipe_id, name, ingredients))


def delete_recipe():
    recipe_id = int(input("ID of recipe to delete: "))
    for recipe in recipes:
        if recipe.id == recipe_id:
            recipes.remove(recipe)
            print("Deleted!")
            break
    else:
        print("Recipe not found!")


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