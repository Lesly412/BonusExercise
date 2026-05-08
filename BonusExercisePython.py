# AskMama: Python-based Meal Planning Chatbot
# Author: Lesly
# Date: 2026-05-07
# Description: Suggests Cameroonian dishes based on user ingredients


# AskMama Full Flexible Python Meal Planner
import random
import json
import os
# Recipe database
recipes_db = [
   {"name": "Poulet DG", "ingredients": ["chicken", "onion", "tomato", "carrot", "bell pepper"]},
   {"name": "Jollof Rice with Chicken", "ingredients": ["rice", "chicken", "tomato", "onion", "bell pepper"]},
   {"name": "Ndole", "ingredients": ["bitterleaf", "groundnuts", "beef", "onion", "shrimp"]},
   {"name": "Fried Plantains", "ingredients": ["plantains", "oil", "salt"]},
   {"name": "Tomato Chicken Stew", "ingredients": ["chicken", "tomato", "onion", "garlic"]},
   {"name": "Eru with Waterleaf", "ingredients": ["eru leaves", "waterleaf", "beef", "fish", "palm oil"]},
   {"name": "Afang Soup", "ingredients": ["afang leaves", "waterleaf", "beef", "fish", "crayfish"]},
   {"name": "Beans with Cassava", "ingredients": ["beans", "cassava", "oil", "onion", "tomato"]}
]
# File paths
HISTORY_FILE = "history.json"
WEEKLY_PLAN_FILE = "weekly_plan.json"
# Load history if exists
if os.path.exists(HISTORY_FILE):
   with open(HISTORY_FILE, "r") as f:
       weekly_history = json.load(f)
else:
   weekly_history = []
# Flexible matching for single-dish
def match_recipe_single(user_ingredients, recipe):
   matches = [i for i in recipe["ingredients"] if i in user_ingredients]
   if len(matches) >= 1 and recipe["name"] not in weekly_history:
       missing = [i for i in recipe["ingredients"] if i not in user_ingredients]
       return missing
   return None
# Flexible matching for weekly plan (allow missing <=2)
def match_recipe_weekly(user_ingredients, recipe):
   # Suggest even if user has only 1 matching ingredient
   matches = [i for i in recipe["ingredients"] if i in user_ingredients]
   if len(matches) >= 1 and recipe["name"] not in weekly_history:
       missing = [i for i in recipe["ingredients"] if i not in user_ingredients]
       return missing
   return None
def suggest_weekly_plan(user_ingredients):
   available_recipes = []
   for recipe in recipes_db:
       missing = match_recipe_weekly(user_ingredients, recipe)
       if missing is not None:
           available_recipes.append((recipe["name"], missing))
   if not available_recipes:
       return []  # No recipes found
   weekly_plan = random.sample(available_recipes, min(7, len(available_recipes)))
   weekly_history.extend([d[0] for d in weekly_plan])
   # Save weekly plan and history
   plan_dict = [{"day": f"Day {i+1}", "dish": d[0], "missing": d[1]} for i, d in enumerate(weekly_plan)]
   with open(WEEKLY_PLAN_FILE, "w") as f:
       json.dump(plan_dict, f, indent=4)
   with open(HISTORY_FILE, "w") as f:
       json.dump(weekly_history, f, indent=4)
   return weekly_plan
# Suggest single recipes
def suggest_single(user_ingredients):
   suggestions = []
   for recipe in recipes_db:
       missing = match_recipe_single(user_ingredients, recipe)
       if missing is not None:
           suggestions.append((recipe["name"], missing))
   return suggestions
# Generate shopping list
def generate_shopping_list(weekly_plan):
   shopping = set()
   for dish, missing in weekly_plan:
       for item in missing:
           shopping.add(item)
   return shopping
# Main interactive loop
def main():
   print("Welcome to AskMama Full Flexible Meal Planner! 🍲")
   print("Enter your ingredients separated by commas (e.g., chicken, rice, tomato).")
   while True:
       user_input = input("\nYour ingredients (or 'quit' to exit): ").lower()
       if user_input.strip() == "quit":
           print("Thanks for using AskMama! Enjoy your meals! 😋")
           break
       user_ingredients = [i.strip() for i in user_input.split(",")]
       # Single-dish suggestions
       single_suggestions = suggest_single(user_ingredients)
       if single_suggestions:
           print("\nSingle-dish suggestions:")
           for dish, missing in single_suggestions:
               if missing:
                   print(f"- {dish} (missing: {', '.join(missing)})")
               else:
                   print(f"- {dish} (all ingredients available!)")
       else:
           print("No single-dish matches found. Try adding more ingredients!")
       # Weekly plan option
       choice = input("\nDo you want a full 7-day weekly meal plan? (yes/no): ").lower()
       if choice == "yes":
           weekly_plan = suggest_weekly_plan(user_ingredients)
           print("\nHere’s your weekly meal plan:")
           for i, (dish, missing) in enumerate(weekly_plan, start=1):
               if missing:
                   print(f"Day {i}: {dish} (missing: {', '.join(missing)})")
               else:
                   print(f"Day {i}: {dish} (all ingredients available!)")
           # Shopping list
           shopping_list = generate_shopping_list(weekly_plan)
           if shopping_list:
               print("\nShopping list for missing ingredients:")
               for item in shopping_list:
                   print(f"- {item}")
           else:
               print("\nYou have all ingredients for the week! 🎉")
if __name__ == "__main__":
   main()