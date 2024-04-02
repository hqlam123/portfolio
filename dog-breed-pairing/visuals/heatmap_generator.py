# coded with aid of documentation from https://seaborn.pydata.org

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_heatmap(file_path, breeds_per_image):
    # create the folder to store visualizations
    cwd = os.getcwd() + '/dog-breed-pairing/'
    output_folder = os.path.join(cwd, "visuals", "heatmap")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # load data into a DataFrame
    df = pd.read_csv(file_path)

    # convert height range to average height for simplicity and categorize into small, medium, and large sizes
    df['Height (inches)'] = df['Height (in)'].apply(lambda x: sum(map(int, x.split('-'))) / 2)
    df['Size'] = pd.cut(df['Height (inches)'], bins=[0, 15, 25, float('inf')], labels=['Small', 'Medium', 'Large'])

    # split health problems column into separate rows
    df['Common Health Problems'] = df['Common Health Problems'].apply(lambda x: x.split(', '))
    df = df.explode('Common Health Problems')

    # create a pivot table to represent the presence of each health problem for each breed
    pivot_table = df.pivot_table(index='Breed', columns='Common Health Problems', aggfunc='size', fill_value=0)

    # split breeds into groups
    breed_groups = [pivot_table.index[i:i+breeds_per_image] for i in range(0, len(pivot_table.index), breeds_per_image)]

    # create separate visualizations for each group of breeds
    for i, breed_group in enumerate(breed_groups, start=1):
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table.loc[breed_group], cmap='Blues', cbar=True)
        plt.title(f'Presence of Common Health Problems for Each Dog Breed (Group {i})')
        plt.xlabel('Common Health Problems')
        plt.ylabel('Dog Breed')
        plt.xticks(rotation=90, ha='center')
        plt.tight_layout()
        output_path = os.path.join(output_folder, f'heatmap_group_{i}.png')
        plt.savefig(output_path)
        plt.close()

if __name__ == "__main__":
    cwd = os.getcwd()
    file_path = cwd + "/dog-breed-pairing/dog_breeds_edited.csv"
    breeds_per_image = 30
    generate_heatmap(file_path, breeds_per_image)
