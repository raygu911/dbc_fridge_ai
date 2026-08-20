import os

import requests
import streamlit as st

API_URL = os.getenv(
    "FRIDGE_AI_API_URL",
    "http://127.0.0.1:8000",
)

st.set_page_config(
    page_title="FridgeAI",
    page_icon="🥗",
    layout="wide",
)

st.title("🥗 FridgeAI")
st.caption("Discover and add recipes using the FridgeAI API.")


def split_lines(value: str) -> list[str]:
    return [
        item.strip()
        for item in value.splitlines()
        if item.strip()
    ]


def split_tags(value: str) -> list[str]:
    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


def display_recipe(
    recipe: dict[str, object],
    score: float | None = None,
) -> None:
    title = (
        f"🍽️ {recipe['name']} "
        f"— {recipe['cooking_time_minutes']} minutes"
    )

    if score is not None:
        title += f" — {score:.0%} match"

    with st.expander(title):
        st.write(recipe["description"])

        st.markdown("**Ingredients**")
        for ingredient in recipe["ingredients"]:
            st.write(f"- {ingredient}")

        st.markdown("**Instructions**")
        for number, instruction in enumerate(
            recipe["instructions"],
            start=1,
        ):
            st.write(f"{number}. {instruction}")

        tags = recipe.get("dietary_tags", [])
        if tags:
            st.caption("Tags: " + ", ".join(tags))


with st.sidebar:
    st.header("System status")

    try:
        health_response = requests.get(
            f"{API_URL}/health",
            timeout=3,
        )
        health_response.raise_for_status()
        st.success("API connected")
    except requests.RequestException:
        st.error("API unavailable")

    st.code(API_URL, language=None)


browse_tab, search_tab, recommend_tab, add_tab = st.tabs(
    [
        "Browse recipes",
        "Semantic search",
        "AI recommendations",
        "Add a recipe",
    ]
)

with browse_tab:
    st.subheader("Available recipes")

    if st.button("Load recipes", type="primary"):
        try:
            response = requests.get(
                f"{API_URL}/api/v1/recipes",
                timeout=10,
            )
            response.raise_for_status()
            recipes = response.json()

            if not recipes:
                st.info("No recipes have been added yet.")

            for recipe in recipes:
                display_recipe(recipe)

        except requests.RequestException as error:
            st.error(f"Could not load recipes: {error}")

with search_tab:
    st.subheader("Find recipes by meaning")
    st.caption(
        "Describe what you want to eat. "
        "You do not need to use exact recipe names."
    )

    with st.form("semantic-search-form"):
        search_query = st.text_input(
            "What would you like to eat?",
            placeholder=(
                "For example: a fast meal made with leftover grains"
            ),
        )
        result_limit = st.slider(
            "Maximum results",
            min_value=1,
            max_value=10,
            value=5,
        )
        search_submitted = st.form_submit_button(
            "Search recipes",
            type="primary",
        )

    if search_submitted:
        if not search_query.strip():
            st.warning("Please describe the meal you want.")
        else:
            try:
                response = requests.get(
                    f"{API_URL}/api/v1/recipes/search",
                    params={
                        "query": search_query.strip(),
                        "limit": result_limit,
                    },
                    timeout=120,
                )
                response.raise_for_status()
                results = response.json()

                if not results:
                    st.info("No matching recipes were found.")

                for result in results:
                    display_recipe(
                        result["recipe"],
                        score=result["score"],
                    )

            except requests.RequestException as error:
                st.error(f"Could not search recipes: {error}")

with recommend_tab:
    st.subheader("Get a grounded recommendation")
    st.caption(
        "FridgeAI retrieves relevant recipes, then uses a local "
        "language model to explain the best match."
    )

    with st.form("recommendation-form"):
        recommendation_query = st.text_area(
            "Describe the meal you want",
            placeholder=(
                "For example: a quick vegan dinner with grains "
                "and fresh vegetables"
            ),
        )
        recommendation_limit = st.slider(
            "Recipes to use as context",
            min_value=1,
            max_value=5,
            value=3,
        )
        recommendation_submitted = st.form_submit_button(
            "Generate recommendation",
            type="primary",
        )

    if recommendation_submitted:
        if not recommendation_query.strip():
            st.warning("Please describe the meal you want.")
        else:
            try:
                with st.spinner("Retrieving recipes and asking Ollama..."):
                    response = requests.post(
                        f"{API_URL}/api/v1/recommendations",
                        json={
                            "query": recommendation_query.strip(),
                            "limit": recommendation_limit,
                        },
                        timeout=180,
                    )
                    response.raise_for_status()

                result = response.json()
                st.markdown("### Recommendation")
                st.markdown(result["recommendation"])
                st.caption(f"Generated locally with {result['model']}")

                st.markdown("### Retrieved sources")
                for source in result["sources"]:
                    display_recipe(
                        source["recipe"],
                        score=source["score"],
                    )

            except requests.RequestException as error:
                st.error(f"Could not generate a recommendation: {error}")

with add_tab:
    st.subheader("Create a recipe")

    with st.form("recipe-form"):
        name = st.text_input("Recipe name")
        description = st.text_area("Description")
        ingredients_text = st.text_area(
            "Ingredients",
            help="Enter one ingredient per line.",
        )
        instructions_text = st.text_area(
            "Instructions",
            help="Enter one instruction per line.",
        )
        cooking_time = st.number_input(
            "Cooking time in minutes",
            min_value=1,
            max_value=1_440,
            value=30,
        )
        tags_text = st.text_input(
            "Dietary tags",
            help="Separate tags with commas.",
        )

        submitted = st.form_submit_button(
            "Add recipe",
            type="primary",
        )

    if submitted:
        payload = {
            "name": name.strip(),
            "description": description.strip(),
            "ingredients": split_lines(ingredients_text),
            "instructions": split_lines(instructions_text),
            "cooking_time_minutes": cooking_time,
            "dietary_tags": split_tags(tags_text),
        }

        try:
            response = requests.post(
                f"{API_URL}/api/v1/recipes",
                json=payload,
                timeout=10,
            )

            if response.status_code == 422:
                st.error(
                    "Please provide a name, at least one "
                    "ingredient, and at least one instruction."
                )
            else:
                response.raise_for_status()
                created_recipe = response.json()
                st.success(
                    f"Added {created_recipe['name']} successfully."
                )

        except requests.RequestException as error:
            st.error(f"Could not add the recipe: {error}")
