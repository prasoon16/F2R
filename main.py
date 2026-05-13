from agent import RecipeAgent, IngredientAgent
from dotenv import load_dotenv

def main():
    load_dotenv()
    recipe_agent = RecipeAgent()
    ingrdient_agent = IngredientAgent()
    print("🍳 Fridge to Recipe Agent")
    print("-" * 30)

    image_path = input("Enter fridge image path: ").strip()
    ext        = image_path.split(".")[-1].lower()

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    print("\n🔍 Scanning ingredients...")
    ingredients = ingrdient_agent.extract_ingredients_from_image_groq(image_bytes, ext)
    print(f"✅ Detected: {ingredients}")

    print("\n👨‍🍳 Finding recipe...")
    recipe = recipe_agent.find_recipe(ingredients)

    print("\n🍽️ Result:")
    print(recipe)

if __name__ == "__main__":
    main()
