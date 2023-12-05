import urllib.parse
from tkinter import *
import requests
from tkhtmlview import HTMLScrolledText, HTMLLabel

# Creating a main window
root = Tk()
root.title("Search recipes")
root.minsize(700, 400)
root.option_add('*Font', 'Calibri')
root.configure(background='#3C3B3B')

# Create a Frame with search navigation
search_frame = LabelFrame(root, padx=5, pady=5, background='#3C3B3B', borderwidth=0)
search_frame.pack(padx=10, pady=10, fill=BOTH)

# Create a Frame with results
result_frame = LabelFrame(root, padx=5, pady=5)
result_frame.pack(padx=10, pady=10, fill=BOTH, expand=1)

# Global variables
api_results = []
hits_number = ""
ingredient = ""


# Creating recipe URL and getting data from JSON
def getData():
    global api_results, hits_number, ingredient
    ingredient = input_field.get()
    meal = chosen_meal.get()
    main_api_url = "https://api.edamam.com/search?&app_id=7f86dfaa&app_key=8b372748045f4b035416c6e8e04105f7&"

    if meal == "Choose a meal type..." or meal == "all":
        search_result_url = main_api_url + urllib.parse.urlencode({'q': ingredient})
    else:
        search_result_url = main_api_url + urllib.parse.urlencode({'q': ingredient}) + "&mealType=" + meal

    # getting JSON data
    result_data = requests.get(search_result_url).json()
    api_results = result_data['hits']
    hits_number = len(api_results)


# Searching the recipes and listing them in HTML
def search_recipe():
    # Clearing the frames before another search
    for widget in result_frame.winfo_children():
        widget.destroy()

    # Getting data from JSON
    getData()
    # loop for getting recipes and creating HTML description in one line
    if hits_number > 0:
        recipes_list = ""
        for result in range(hits_number):
            result_label = str(api_results[result]['recipe']['label'])
            result_url = str(api_results[result]['recipe']['url'])
            result_calories = int(api_results[result]['recipe']['calories'])
            result_ingredients = len(api_results[result]['recipe']['ingredients'])
            result_img = str(api_results[result]['recipe']['image'])

            result_description = f"""<p>
                                <td><img src='{result_img}'width="150" height="150"><br>
                                <h3><a href='{result_url}'>{result_label}</a></h3>
                                <b>Calories: </b>{result_calories}<br>
                                <b>Number of ingredients: </b>{result_ingredients}<br>
                                <img src='line.png' width="170"><br>                                
                                </p>"""
            recipes_list += result_description

        # showing results
        searched_recipe_title = HTMLScrolledText(result_frame, html=recipes_list)
        searched_recipe_title.pack(fill=BOTH, expand=True)

    # if nothing is given in input field
    elif ingredient == "":
        searched_recipe_title = HTMLLabel(result_frame, html="You must enter an ingredient")
        searched_recipe_title.pack(fill=BOTH)

    # if there is no results for given ingredient
    else:
        searched_recipe_title = HTMLLabel(result_frame, html="There is no recipe with such ingredient")
        searched_recipe_title.pack(fill=BOTH)


# Saving search result to .txt
def save_recipe():
    # Getting data from JSON
    getData()

    recipes_list = ""
    for result in range(hits_number):
        result_label = str(api_results[result]['recipe']['label'])
        result_url = str(api_results[result]['recipe']['url'])
        result_calories = int(api_results[result]['recipe']['calories'])
        result_ingredients = len(api_results[result]['recipe']['ingredients'])

        # Recipes description in .txt
        result_description = f"""LABEL = {result_label}
LINK = {result_url}
Calories: {result_calories}
Number of ingredients: {result_ingredients}
____________________\n"""
        recipes_list += result_description

    my_recipes = recipes_list

    # Creating .txt file
    with open('my_recipes.txt', 'w') as my_recipes_file:
        my_recipes_file.write(my_recipes)

    import os
    os.system("my_recipes.txt")


# Changing Save button from disabled to normal after clicking in "Search button"
def changeState():
    if save_button['state'] == NORMAL:
        save_button['state'] = DISABLED
    else:
        save_button['state'] = NORMAL


# Title Label
title = Label(search_frame, text="SEARCH RECIPES", font='20', background='#3C3B3B', fg='#ffffff')
title.grid(row=0, column=1, padx=5, pady=5)

# Instruction
instruction_text = Label(search_frame, text="Search an ingredient: ", background='#3C3B3B', fg='#ffffff')
instruction_text.grid(row=1, column=0, padx=5, pady=10)

# Input
input_field = Entry(search_frame, width=30, borderwidth=4)
input_field.grid(row=1, column=1, padx=5, pady=10)

# Drop Down ,meal menu
mealtype_list = [
    "all",
    "breakfast",
    "lunch",
    "dinner",
    "snack"
]
chosen_meal = StringVar()
chosen_meal.set("Choose a meal type...")
mealtype_menu = OptionMenu(search_frame, chosen_meal, *mealtype_list)
mealtype_menu.configure(width=17, borderwidth=0)
mealtype_menu.grid(row=1, column=2, padx=5, pady=10, sticky=E)

# Search button
loop_img = PhotoImage(file="loop.png")
search_button = Button(search_frame, text="Search", command=lambda: [search_recipe(), changeState()],
                       background='#ffffff', image=loop_img, compound=RIGHT)
search_button.grid(row=2, column=1)

# Save button
save_img = PhotoImage(file="save.png")
save_button = Button(search_frame, text="Save recipes ", command=save_recipe, background='#ffffff', state=DISABLED,
                     image=save_img, compound=RIGHT)
save_button.grid(row=2, column=2, padx=5, pady=5, sticky=E)

# looping the main window
root.mainloop()
