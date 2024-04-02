# coded with aid of documentation from https://seaborn.pydata.org

import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

def generate_wordcloud(file_path, attribute):
    # load data into a DataFrame
    df = pd.read_csv(file_path)

    # split the attribute column into separate rows for each breed
    df[attribute] = df[attribute].apply(lambda x: x.lower().split(', '))
    df = df.explode(attribute)

    # count the frequency of each word
    word_freq = df[attribute].value_counts().to_dict()

    # normalize the frequencies
    max_freq = max(word_freq.values())
    normalized_freq = {word: freq / max_freq * 10 for word, freq in word_freq.items()}

    # generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(normalized_freq)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title("Common Health Problems", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    
    # create the folder to store word cloud
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(script_dir, "wordcloud")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, 'wordcloud.png')
    plt.savefig(output_path, bbox_inches='tight')  # Save the plot as a PNG file

if __name__ == "__main__":
    cwd = os.getcwd()
    file_path = cwd + "/dog-breed-pairing/dog_breeds_edited.csv"
    attribute = "Common Health Problems"
    generate_wordcloud(file_path, attribute)
