from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

@tool
def search_recipes(ingredients: str) -> str:
    """Search for recipes using the given ingredients. 
    Args:
        ingredients: comma-separated list of ingredients
    """
    query = f"simple recipe using {ingredients} no other ingredients needed"
    return search.run(query)

@tool
def get_missing_ingredients(have: str, need: str) -> str:
    """Compare ingredients you have vs what a recipe needs.
    Returns a shopping list of missing items.

    Args:
        'have': comma-separated ingredient lists which user have
        'need': comma-separated ingredient lists which is required by recipe
    """
    have_list = {i.strip().lower() for i in have.split(",")}
    need_list = {i.strip().lower() for i in need.split(",")}
    missing = need_list - have_list
    if not missing:
        return "You have everything! No shopping needed."
    return "Shopping list: " + ", ".join(sorted(missing))
