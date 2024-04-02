# coded with aid of documentation from https://seaborn.pydata.org

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_histogram(file_path, attribute):
    # load data into a DataFrame
    df = pd.read_csv(file_path)

    # split the attribute column into separate rows for each breed
    df[attribute] = df[attribute].apply(lambda x: x.split(', '))
    df = df.explode(attribute)

    # create the folder to store histogram
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(script_dir, "histogram")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # plot the histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=attribute, bins=len(df[attribute].unique()), discrete=True)
    plt.title(f'Distribution of {attribute} Across Dog Breeds')
    plt.xlabel(attribute)
    plt.ylabel('Frequency')
    plt.xticks(rotation=90)
    plt.tight_layout()
    output_path = os.path.join(output_folder, 'furcolor_distribution.png')
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    cwd = os.getcwd()
    file_path = cwd + "/dog-breed-pairing/dog_breeds_edited.csv"
    attribute = "Fur Color"
    generate_histogram(file_path, attribute)
