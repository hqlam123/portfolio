# Huy Lam WGU Student ID: 011087189
# Program written and intended for C964 Capstone project

import csv
import os
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_breed_data(file_path):
    # initiate breed data storage
    breed_data = []

    # read csv to parse for data
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            breed = row['Breed']
            fur_colors = [color.strip() for color in row['Fur Color'].split(',')]
            height = row['Height (in)']
            character_traits = [trait.strip().lower().title() for trait in row['Character Traits'].replace("{", "").replace("}", "").split(',')]
            health_problems = [problem.strip() for problem in row['Common Health Problems'].replace("{", "").replace("}", "").split(',')]
            breed_data.append({
                'Breed': breed,
                'Fur Colors': fur_colors,
                'Height Range (inches)': height,
                'Character Traits': character_traits,
                'Common Health Problems': health_problems
            })
    return breed_data

def recommend_breeds(user_preferences, breed_data, num_recommendations=3):
    # coded with aid of documentation from https://seaborn.pydata.org

    # preprocess user preferences to generate vector
    X = [preprocess_user_preferences(user_preferences['Fur Color'], user_preferences['Height (in)'], user_preferences['Character Traits'])]
    
    vectorizer = CountVectorizer()

    # handle case where fur color preference is "No Preference"
    if user_preferences['Fur Color'].lower() == 'no preference':
        X_breed = vectorizer.fit_transform([' '.join(data['Character Traits']) + ' ' + str(data['Height Range (inches)']) for data in breed_data])
    else:
        X_breed = vectorizer.fit_transform([' '.join(data['Character Traits']) + ' ' + ' '.join(data['Fur Colors']) + ' ' + str(data['Height Range (inches)']) for data in breed_data])
    
    X_user = vectorizer.transform(X)

    # calculate cosine similarily between user preference and breed data
    similarities = cosine_similarity(X_user, X_breed)
    recommended_indices = similarities.argsort()[0][-num_recommendations:][::-1]

    return [(breed_data[index], similarities[0][index]) for index in recommended_indices]

def preprocess_user_preferences(fur_color_preference, height_preference, character_traits):
    # join user preferences together for vector generation
    return ' '.join([fur_color_preference, str(height_preference)] + character_traits)

def load_fur_colors(file_path):
    # parse csv for fur colors
    fur_colors = set()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            colors = [color.strip() for color in row['Fur Color'].split(',')]
            fur_colors.update(colors)
    return fur_colors

def load_character_traits(file_path):
    # parse csv for character traits
    traits_set = set()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            traits_set.update(trait.strip().lower() for trait in row['Character Traits'].replace("{", "").replace("}", "").split(','))
    return traits_set

def print_items(items):
    # print paramaterized items alphabetically in a formatted display
    items_sorted = sorted(items, key=lambda x: x.lower())
    max_len = max(len(item) for item in items_sorted)
    num_cols = 3
    col_width = max_len + 4
    for i, item in enumerate(items_sorted, start=1):
        print(f"- {item.title().ljust(col_width)}", end="")
        if i % num_cols == 0:
            print()
    print()

def print_recommendations(recommendations):
    # display generated recommendations as well as cosine similarity score
    for i, (recommendation, similarity) in enumerate(recommendations, start=1):
        print(f"{i}. Breed: {recommendation['Breed']} (Cosine Similarity: {similarity:.2f})")
        print(f"   Fur Colors: {', '.join(recommendation['Fur Colors'])}")
        print(f"   Height Range (inches): {recommendation['Height Range (inches)']}")
        print(f"   Character Traits: {', '.join(recommendation['Character Traits'])}")
        print(f"   Common Health Problems: {', '.join(recommendation['Common Health Problems'])}")
        print()

def evaluate_recommendations(predicted_recommendations, actual_recommendations):
    # method used during debug and analysis; does not get called in actual program

    # compute evaluation metrics (e.g., precision, recall, accuracy)
    true_positives = len(set(predicted_recommendations) & set(actual_recommendations))
    false_positives = len(set(predicted_recommendations) - set(actual_recommendations))
    false_negatives = len(set(actual_recommendations) - set(predicted_recommendations))
    
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")

def run_program():
    # initiate file path and data
    cwd = os.getcwd()
    file_path = cwd + "/dog-breed-pairing/dog_breeds_edited.csv"
    breed_data = load_breed_data(file_path)
    fur_colors = load_fur_colors(file_path)
    character_traits = load_character_traits(file_path)

    # initiate UI
    os.system('clear')  
    print("Welcome to the Dog Breed Recommendation System!")
    print("Are you ready to get paired with your future best friend?")
    input("Press Enter to continue! ")

    # fur color preference
    os.system('clear')  
    print_items(fur_colors)
    print()
    print("Shown above are the different possible fur colors of dogs.")
    print("Please enter your preferred dog fur color as one (1) word (ex: ""Black"").")
    print("Press ENTER to continue.")
    print()
    fur_color_preference = input("Preferred fur color (leave blank for no preference): ").strip().lower()
    if fur_color_preference == "":
        fur_color_preference = "No Preference"

    # size preference
    os.system('clear')
    print("Size guide:")
    print("5-15 inches: Small (Chihuahua, Beagle)")
    print("16-24 inches: Medium (Boston Terrier, Border Collie)")
    print("24-35 inches: Large (Greyhound, Mastiff)")
    print()
    print("Shown above are the different height ranges of dog breed sizes.")
    print("Please enter your preferred dog size as one (1) number (ex: ""17"").")
    print("Press ENTER to continue.")
    print()
    height_preference = input("Preferred height (leave blank for no preference): ").strip()
    if height_preference == "":
        height_preference = "No Preference"
    else:
        height_preference = float(height_preference)

    # character trait preference(s)
    os.system('clear')
    print_items(character_traits)
    print("Shown above are the different character traits of dogs.")
    print("Please enter up to three (3) preferred traits as one (1) word each (ex: ""Loyal"").")
    print("Press ENTER to continue after each trait.")
    print()

    user_character_traits = []
    for i in range(3):
        trait = input(f"Enter character trait {i+1}/3 (leave blank to skip): ").strip().lower()
        if trait:
            user_character_traits.append(trait.title())
    
    # aggregate preferences
    user_preferences = {
        'Fur Color': fur_color_preference.title(),
        'Height (in)': height_preference,
        'Character Traits': user_character_traits
    }

    recommended_breeds = recommend_breeds(user_preferences, breed_data, num_recommendations=3)

    # display user preferences
    os.system('clear')
    print(f"Preferred Fur Color: {user_preferences['Fur Color']}")

    preferred_height = user_preferences['Height (in)']
    height_text = " inches" if preferred_height != "No Preference" else ""

    preferred_height_str = str(int(float(preferred_height))) if preferred_height != "No Preference" else ""

    print(f"Preferred Height: {preferred_height_str}{height_text}")

    preferred_traits = user_preferences['Character Traits']
    if preferred_traits:
        traits_text = ', '.join(preferred_traits)
    else:
        traits_text = "No Preference"
    print(f"Preferred Character Trait(s): {traits_text}")
    print()

    # show recommendations
    print("We recommend the following breeds based on your preferences:")
    print_recommendations(recommended_breeds)

if __name__ == "__main__":
    run_program()