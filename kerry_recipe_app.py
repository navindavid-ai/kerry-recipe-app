import streamlit as st
import pandas as pd
import uuid


# Handle reset from previous run
if st.session_state.get("_trigger_reset", False):
    st.session_state.update({
        "form_name": "",
        "form_steps": "",
        "form_prep_time": "",
        "form_cook_time": "",
        "form_tags": "",
        "form_youtube": "",
        "ingredient_list": [],
        "ing_name": "",
        "ing_qty": "",
        "ing_unit": "",
        "edit_mode": False,
        "edit_index": None,
        "_trigger_reset": False
    })

# Initialize session state
if "recipes" not in st.session_state:
    st.session_state.recipes = []
if "ingredient_list" not in st.session_state:
    st.session_state.ingredient_list = []
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None
if "ing_name" not in st.session_state:
    st.session_state.ing_name = ""
if "ing_qty" not in st.session_state:
    st.session_state.ing_qty = ""
if "ing_unit" not in st.session_state:
    st.session_state.ing_unit = ""

st.sidebar.header("Add or Edit a Recipe")

if st.session_state.edit_mode:
    recipe_to_edit = st.session_state.recipes[st.session_state.edit_index]
    default_name = recipe_to_edit["name"]
    default_category = recipe_to_edit["category"]
    default_ingredients = recipe_to_edit["ingredients"]
    default_steps = recipe_to_edit["steps"]
    default_prep_time = recipe_to_edit["prep_time"]
    default_cook_time = recipe_to_edit["cook_time"]
    default_tags = ", ".join(recipe_to_edit["tags"])
    default_youtube = recipe_to_edit.get("youtube", "")
    if not st.session_state.ingredient_list:
        st.session_state.ingredient_list = default_ingredients
else:
    default_name = ""
    default_category = "Dinner"
    default_ingredients = []
    default_steps = ""
    default_prep_time = ""
    default_cook_time = ""
    default_tags = ""
    default_youtube = ""

# Ingredient adder (above form)
st.sidebar.markdown("### Ingredients")
cols = st.sidebar.columns([4, 2, 2])
with cols[0]:
    st.session_state.ing_name = st.text_input("Ingredient", value=st.session_state.ing_name)
with cols[1]:
    st.session_state.ing_qty = st.text_input("Quantity", value=st.session_state.ing_qty)
with cols[2]:
    st.session_state.ing_unit = st.selectbox("Unit", ["", "g", "kg", "ml", "l", "tsp", "tbsp", "cup", "pcs"], index=0 if not st.session_state.ing_unit else ["", "g", "kg", "ml", "l", "tsp", "tbsp", "cup", "pcs"].index(st.session_state.ing_unit))

if st.sidebar.button("+ Add Ingredient") and st.session_state.ing_name:
    st.session_state.ingredient_list.append({
        "name": st.session_state.ing_name,
        "qty": st.session_state.ing_qty,
        "unit": st.session_state.ing_unit
    })
    st.session_state.ing_name = ""
    st.session_state.ing_qty = ""
    st.session_state.ing_unit = ""
    st.rerun()

if st.session_state.ingredient_list:
    st.sidebar.write("Current Ingredients:")
    for idx, ing in enumerate(st.session_state.ingredient_list):
        col1, col2 = st.sidebar.columns([8, 2])
        with col1:
            st.sidebar.markdown(f"- {ing['qty']} {ing['unit']} {ing['name']}")
        with col2:
            if st.sidebar.button("🗑️", key=f"del_{idx}"):
                st.session_state.ingredient_list.pop(idx)
                st.rerun()

# Main form for recipe info
# Track form fields in session state
for key in ["form_name", "form_steps", "form_prep_time", "form_cook_time", "form_tags", "form_youtube"]:
    if key not in st.session_state:
        st.session_state[key] = ""

with st.sidebar.form("recipe_form") as form:
    st.text_input("Recipe Name", value=st.session_state.get("form_name", default_name), key="form_name")
    category = st.selectbox("Category", ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack"], index=["Breakfast", "Lunch", "Dinner", "Dessert", "Snack"].index(default_category))
    cuisine = st.selectbox("Cuisine", ["", "South Indian", "North Indian", "Italian", "Mexican", "English", "Thai", "Chinese", "French", "Other"])
    st.text_area("Cooking Steps", value=st.session_state.get("form_steps", default_steps), key="form_steps")
    st.text_input("Prep Time (e.g. 15 mins)", value=st.session_state.get("form_prep_time", default_prep_time), key="form_prep_time")
    st.text_input("Cook Time (e.g. 30 mins)", value=st.session_state.get("form_cook_time", default_cook_time), key="form_cook_time")
    st.text_input("Tags (comma-separated)", value=st.session_state.get("form_tags", default_tags), key="form_tags")
    st.text_input("YouTube Video Link (optional)", value=st.session_state.get("form_youtube", default_youtube), key="form_youtube")
    image = st.file_uploader("Upload a Photo (optional)", type=["jpg", "jpeg", "png"])
    col_submit, col_reset = st.columns([1, 1])
    with col_submit:
        submitted = st.form_submit_button("Update Recipe" if st.session_state.edit_mode else "Add Recipe")
    with col_reset:
        reset_clicked = st.form_submit_button("Reset")

    if submitted and st.session_state.form_name and st.session_state.ingredient_list and st.session_state.form_steps:
        recipe = {
            "id": str(uuid.uuid4()) if not st.session_state.edit_mode else st.session_state.recipes[st.session_state.edit_index]["id"],
            "name": st.session_state.form_name,
            "category": category,
            "cuisine": cuisine,
            "ingredients": st.session_state.ingredient_list,
            "steps": st.session_state.form_steps,
            "prep_time": st.session_state.form_prep_time,
            "cook_time": st.session_state.form_cook_time,
            "tags": [t.strip() for t in st.session_state.form_tags.split(",") if t.strip()],
            "image": image.getvalue() if image else (st.session_state.recipes[st.session_state.edit_index]["image"] if st.session_state.edit_mode else None),
            "youtube": st.session_state.form_youtube.strip() if st.session_state.form_youtube else None
        }
        if st.session_state.edit_mode:
            st.session_state.recipes[st.session_state.edit_index] = recipe
            st.success(f"Updated '{st.session_state.form_name}'")
        else:
            st.session_state.recipes.append(recipe)
            st.success(f"Added '{st.session_state.form_name}' to recipes!")
        st.session_state.ingredient_list = []
        st.session_state.edit_mode = False
        st.rerun()

    if 'reset_clicked' in locals() and reset_clicked:
        st.session_state._trigger_reset = True
        st.rerun()

# View and manage all saved recipes
search = st.text_input("🔍 Search recipes by name, tag, or category")

filtered = []
for i, r in enumerate(st.session_state.recipes):
    if search.lower() in r["name"].lower() or \
       search.lower() in r["category"].lower() or \
       any(search.lower() in tag.lower() for tag in r["tags"]):
        filtered.append((i, r))

recipes_to_show = filtered if search else list(enumerate(st.session_state.recipes))

st.subheader("📚 All Recipes")
if not recipes_to_show:
    st.info("No recipes found. Add one from the sidebar!")
else:
    for index, recipe in recipes_to_show:
        with st.expander(recipe["name"]):
            st.markdown(f"**Category**: {recipe['category']}")
            if 'cuisine' in recipe and recipe['cuisine']:
                st.markdown(f"**Cuisine**: {recipe['cuisine']}")
            st.markdown(f"**Prep Time**: {recipe['prep_time']} | **Cook Time**: {recipe['cook_time']}")
            st.markdown("**Tags**: " + ", ".join(recipe["tags"]))
            if recipe["image"]:
                st.image(recipe["image"], width=300)
            if recipe.get("youtube"):
                st.video(recipe["youtube"])
            st.markdown("### Ingredients")
            for ing in recipe["ingredients"]:
                st.markdown(f"- {ing['qty']} {ing['unit']} {ing['name']}")
            st.markdown("### Steps")
            st.markdown(recipe["steps"])
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"✏️ Edit {recipe['name']}", key=f"edit_{index}"):
                    st.session_state.edit_mode = True
                    st.session_state.edit_index = index
                    st.rerun()
            with col2:
                if st.button(f"🗑️ Delete {recipe['name']}", key=f"delete_{index}"):
                    st.session_state.recipes.pop(index)
                    st.success(f"Deleted '{recipe['name']}'")
                    st.rerun()

# Grocery list generator
if st.button("🛒 Generate Grocery List from All Recipes"):
    all_ingredients = []
    for recipe in st.session_state.recipes:
        all_ingredients.extend([f"{ing['qty']} {ing['unit']} {ing['name']}" for ing in recipe["ingredients"]])
    st.subheader("🧾 Grocery List")
    grocery_text = "\n".join(all_ingredients)
    st.text_area("Copy this list:", value=grocery_text, height=200)
