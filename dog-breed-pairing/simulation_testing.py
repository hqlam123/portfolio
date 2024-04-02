# majority of code is directly taken from "main.py"

import csv
import os
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_breed_data(file_path):
    # read breed data from csv file
    breed_data = []
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
    X = [preprocess_user_preferences(user_preferences['Fur Color'], user_preferences['Height (in)'], user_preferences['Character Traits'])]
    
    vectorizer = CountVectorizer()

    if user_preferences['Fur Color'].lower() == 'no preference':
        X_breed = vectorizer.fit_transform([' '.join(data['Character Traits']) + ' ' + str(data['Height Range (inches)']) for data in breed_data])
    else:
        X_breed = vectorizer.fit_transform([' '.join(data['Character Traits']) + ' ' + ' '.join(data['Fur Colors']) + ' ' + str(data['Height Range (inches)']) for data in breed_data])
    
    X_user = vectorizer.transform(X)

    similarities = cosine_similarity(X_user, X_breed)
    recommended_indices = similarities.argsort()[0][-num_recommendations:][::-1]

    return [(breed_data[index], similarities[0][index]) for index in recommended_indices]

def preprocess_user_preferences(fur_color_preference, height_preference, character_traits):
    return ' '.join([fur_color_preference, str(height_preference)] + character_traits)

def load_fur_colors(file_path):
    fur_colors = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            colors = [color.strip() for color in row['Fur Color'].split(',')]
            fur_colors.extend(colors)
    return fur_colors

def load_character_traits(file_path):
    traits_set = set()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            traits_set.update(trait.strip().lower() for trait in row['Character Traits'].replace("{", "").replace("}", "").split(','))
    return traits_set

def print_recommendations(recommendations):
    for i, (recommendation, similarity) in enumerate(recommendations, start=1):
        print(f"{i}. Breed: {recommendation['Breed']} (Cosine Similarity: {similarity:.2f})")
        print(f"   Fur Colors: {', '.join(recommendation['Fur Colors'])}")
        print(f"   Height Range (inches): {recommendation['Height Range (inches)']}")
        print(f"   Character Traits: {', '.join(recommendation['Character Traits'])}")
        print(f"   Common Health Problems: {', '.join(recommendation['Common Health Problems'])}")
        print()

def simulate_users(num_users):
    # initiate file path and data
    cwd = os.getcwd()
    file_path = cwd + "/dog-breed-pairing/dog_breeds_edited.csv"
    breed_data = load_breed_data(file_path)
    fur_colors = load_fur_colors(file_path)
    character_traits = list(load_character_traits(file_path))
    total_similarities = {i: 0 for i in range(1, 4)}

    # run simulation for each user
    for user_id in range(1, num_users + 1):
        print(f"User {user_id}:")

        # randomly select fur color
        fur_color_preference = random.choice(fur_colors)
        
        # randomly select height
        min_height = min(float(data['Height Range (inches)'].split('-')[0]) for data in breed_data)
        max_height = max(float(data['Height Range (inches)'].split('-')[1]) for data in breed_data)
        height_preference = random.uniform(min_height, max_height)
        
        # randomly select 3 traits
        user_character_traits = random.sample(character_traits, min(len(character_traits), 3))

        # aggregate user preferences
        user_preferences = {
            'Fur Color': fur_color_preference,
            'Height (in)': height_preference,
            'Character Traits': user_character_traits
        }

        # print user preferences
        print(f"Preferences: Fur Color - {fur_color_preference}, Height - {height_preference:.2f} inches, Character Traits - {', '.join(user_character_traits)}")

        # get and print recommendations
        recommended_breeds = recommend_breeds(user_preferences, breed_data, num_recommendations=3)
        print("Recommendations:")
        print_recommendations(recommended_breeds)
        
        # accumulate average cosine similarity scores
        for i, (recommendation, similarity) in enumerate(recommended_breeds, start=1):
            total_similarities[i] += similarity

        print()

    # calculate and display average cosine similarity scores
    print("Average Cosine Similarity Scores:")
    for i in range(1, 4):
        average_similarity = total_similarities[i] / num_users
        print(f"Top {i}: {average_similarity:.2f}")

if __name__ == "__main__":
    num_users = int(input("Enter the number of users to simulate: "))
    simulate_users(num_users)
