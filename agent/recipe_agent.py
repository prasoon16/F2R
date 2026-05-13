from langchain.agents import create_agent

from agent.tools import get_missing_ingredients, search_recipes


class RecipeAgent():
    SYSTEM_PROMPT = """You are a helpful cooking assistant.
        When given ingredients, respond in ONE single message with ALL of this:

        1. RECIPE NAME + brief description (2 lines)
        2. INGREDIENTS NEEDED (full list the recipe requires)
        3. MISSING INGREDIENTS (compare with what user has, list only what's missing)
        4. STEP-BY-STEP INSTRUCTIONS (numbered)
        5. PRO TIP (one quick tip)

        Do NOT ask follow-up questions.
        Do NOT say "let me check" or "first I'll...".
        Use the search_recipes tool once, then the get_missing_ingredients tool once,
        then respond with everything together immediately."""
    GEMINI_MODEL_NAME = "google_genai:gemini-2.5-flash-lite"
    def __init__(self):
        self.agent = create_agent(
            model=self.GEMINI_MODEL_NAME,
            system_prompt=self.SYSTEM_PROMPT,
            tools=[search_recipes, get_missing_ingredients]
        )
    def find_recipe(self, ingredients):
        msg = f"""I have exactly these ingredients: {ingredients}.
        Find me one great recipe, identify what I'm missing,
        and give me the full recipe with steps. All in one response."""
        inputs = {"messages": [{"role": "user", "content": msg}]}
        result = self.agent.invoke(
        input=inputs
        )
        print(result["messages"][-1].content_blocks)
        return result["messages"][-1].content_blocks[0]['text']