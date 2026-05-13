from dotenv import load_dotenv
import streamlit as st
from agent import RecipeAgent, IngredientFinder

load_dotenv()
recipe_agent = RecipeAgent()
ingrdient_finder = IngredientFinder()

st.set_page_config(page_title="Fridge to Recipe", page_icon="🍳")
st.markdown("## 🍳 Fridge → Recipe")
st.caption("Snap your fridge · Get a recipe · Skip the grocery run")
st.divider()

uploaded = st.file_uploader("📷 Upload fridge photo", type=["jpg", "jpeg", "png"])

if uploaded:
    st.image(uploaded, use_column_width=True)
    ext = uploaded.name.split(".")[-1].lower()

    if st.button("🔍 Scan Ingredients"):
        with st.spinner("Scanning with Groq Vision..."):
            ingredients = ingrdient_finder.extract_ingredients_from_image_groq(uploaded.read(), ext)
            st.session_state["ingredients"] = ingredients

    if "ingredients" in st.session_state:
        st.markdown("### 🥦 Detected Ingredients")
        edited = st.text_area(
            "✏️ Edit if needed",
            value=st.session_state["ingredients"],
            height=80
        )

        if st.button("👨‍🍳 Find Recipe"):
            with st.spinner("Finding recipe..."):
                recipe = recipe_agent.find_recipe(edited)
                st.session_state["recipe"] = recipe

    if "recipe" in st.session_state:
        st.markdown("### 🍽️ Your Recipe")
        st.markdown(st.session_state["recipe"])
        st.download_button(
            "📥 Download Recipe",
            data=st.session_state["recipe"],
            file_name="recipe.txt"
        )
        if st.button("🔄 Try Another"):
            st.session_state.clear()
            st.rerun()